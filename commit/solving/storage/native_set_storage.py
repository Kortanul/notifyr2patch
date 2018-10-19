from commit.solving.storage.solution_storage import SolutionStorage


class NativeSetStorage(SolutionStorage):
  def __init__(self):
    self.sets_by_commit = {}

  def get_all_solutions_for(self, commit_id):
    attempt_set = self._commit_solution_set_for(commit_id)

    return list(attempt_set)

  def get_solution_set_size_for(self, commit_id):
    attempt_set = self._commit_solution_set_for(commit_id)

    return len(attempt_set)

  def clear_solution_set_for(self, commit_id):
    attempt_set = self._commit_solution_set_for(commit_id)

    attempt_set.clear()

  def has_seen(self, commit_id, commit_solution):
    attempt_set = self._commit_solution_set_for(commit_id)
    attempt_as_str = str(commit_solution)

    return attempt_as_str in attempt_set

  def mark_seen(self, commit_id, commit_solution):
    attempt_set = self._commit_solution_set_for(commit_id)
    attempt_as_str = str(commit_solution)

    attempt_set.add(attempt_as_str)

  def _commit_solution_set_for(self, commit_id):
    if commit_id not in self.sets_by_commit:
      self.sets_by_commit[commit_id] = set()

    return self.sets_by_commit[commit_id]

