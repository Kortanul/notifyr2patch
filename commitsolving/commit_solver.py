from commitsolving.commit_solution import CommitSolution


class CommitSolver:
  def __init__(self, git_client, author_distribution_factory,
               committer_distribution_factory,
               timezone_distribution_factory,
               time_picker_factory, solution_storage, temp_path):
    self.git_client = git_client

    self.author_distribution_factory = author_distribution_factory
    self.committer_distribution_factory = committer_distribution_factory
    self.timezone_distribution_factory = timezone_distribution_factory
    self.time_picker_factory = time_picker_factory

    self.solution_storage = solution_storage
    self.temp_path = temp_path

  def solve_all(self, base_ref, notification):
    for notification_commit in notification.commits:
      # NOTE: Each commit forms the base ref for the next commit in the
      # notification
      base_ref = self.solve_commit(base_ref, notification, notification_commit)

  def solve_commit(self, base_ref, notification, notification_commit):
    author_distribution = \
      self._get_author_distribution(notification, notification_commit)

    target_commit_id = notification_commit.id
    attempt_index = 1

    while True:
      commit_solution = \
        self.pick_solution(author_distribution, notification_commit)

      if self.solution_storage.has_seen(target_commit_id, commit_solution):
        print(".", end='', flush=True)
      elif self.is_correct_solution(base_ref, target_commit_id, attempt_index,
                                    commit_solution):
        break
      else:
        attempt_index += 1

        self.solution_storage.mark_seen(target_commit_id, commit_solution)

    return target_commit_id

  def pick_solution(self, author_distribution, notification_commit):
    author_name = author_distribution.pick_author()

    committer_distribution = \
      self.committer_distribution_factory.get_distribution_for(author_name)

    committer_name = committer_distribution.pick_committer()

    author_timezone_distribution = \
      self.timezone_distribution_factory.get_distribution_for(author_name)

    offset = author_timezone_distribution.pick_timezone_offset()
    offset_value = offset.utcoffset(None)

    time_picker = \
      self.time_picker_factory.get_time_picker_for(author_name, offset_value)

    author_date = notification_commit.date.astimezone(offset)
    commit_date = time_picker.pick_commit_date(author_date)

    commit_solution = \
      CommitSolution(
        notification_commit,
        author_name,
        committer_name,
        offset,
        author_date,
        commit_date
      )

    return commit_solution

  def is_correct_solution(self, base_ref, target_commit_id, attempt_index,
                          commit_solution):
    print('')
    print(f"Attempt #{attempt_index} - Trying:")

    commit_solution.print_inputs()

    current_commit_id = \
      commit_solution.apply_to(self.git_client, base_ref, self.temp_path)

    attempted_solutions = \
      self.solution_storage.get_solution_set_size_for(target_commit_id)

    print(f"Target: {target_commit_id}")
    print(f"Current: {current_commit_id}")
    print(f"Total Attempted Solutions: {attempted_solutions}")
    print()
    print()

    if current_commit_id == target_commit_id:
      print("Solution found!")
      return True
    else:
      return False

  def _get_author_distribution(self, notification, notification_commit):
    author_name_pool = [notification.pusher, notification_commit.author]

    distribution = \
      self.author_distribution_factory.get_distribution_for(author_name_pool)

    return distribution
