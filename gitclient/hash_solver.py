import tempfile
from datetime import timedelta
from os import path

from decorators.gitpatch.commit_decorator import CommitDecorator
from gitclient.hashsolving.author_commit_offset_distribution import \
  AuthorCommitOffsetDistribution
from gitclient.hashsolving.author_distribution import AuthorDistribution
from gitclient.hashsolving.author_timezone_distribution import \
  AuthorTimezoneDistribution
from gitclient.hashsolving.committer_distribution import CommitterDistribution
from gitclient.hashsolving.global_commit_offset_distribution import \
  GlobalCommitOffsetDistribution
from gitclient.hashsolving.hazelcast_client import HazelcastClient
from gitclient.hashsolving.probabilistic_incremental_commit_time_picker import \
  ProbabilisticIncrementalCommitTimePicker
from gitclient.hashsolving.simple_incremental_commit_time_picker import \
  SimpleIncrementalCommitTimePicker

TEMP_PATCH_FILENAME = "temp.patch"

MIN_COMMIT_OFFSET = timedelta(days=3,hours=12).total_seconds()
MAX_COMMIT_OFFSET = timedelta(days=4).total_seconds()

COMMIT_WINDOWS_SPAN = timedelta(minutes=15).total_seconds()


class CommitSolver:
  def __init__(self, git_client, base_ref, notification):
    self.git_client = git_client
    self.base_ref = base_ref
    self.notification = notification

    self.committer_distributions = dict()
    self.commit_time_distributions = dict()
    self.timezone_distributions = dict()
    self.commit_time_pickers = dict()
    
  def run(self):
    for notification_commit in self.notification.commits:
      return self.solve_commit(notification_commit)

  def solve_commit(self, notification_commit):
    target_commit_id = notification_commit.id

    author_name_pool = [
      self.notification.pusher,
      notification_commit.author
    ]

    author_distribution = AuthorDistribution(self.git_client, author_name_pool)

    attempt = 1

    hazelcast_client = HazelcastClient(target_commit_id)
    seen_combinations = hazelcast_client.solution_attempt_set

    while True:
      author_name = author_distribution.pick_author()

      committer_distribution = self.committer_distribution_for(author_name)
      committer_name = committer_distribution.pick_committer()

      author_commit_time_distribution = \
        self.commit_time_distribution_for(author_name)

      author_timezone_distribution = \
        self.author_timezone_distribution_for(author_name)

      offset = author_timezone_distribution.pick_timezone_offset()
      offset_value = offset.utcoffset(None)

      author_date = notification_commit.date.astimezone(offset)

      # commit_date = \
      #   self.probabilistic_incremental_time_picker_for(
      #     author_name, offset_value
      #   ).pick_commit_date(author_date)
      #
      # commit_date = \
      #   self.simple_incremental_time_picker_for(author_name, offset_value) \
      #       .pick_commit_date(author_date)

      commit_date = \
        author_commit_time_distribution.pick_commit_date(author_date)

      combination = str(
        (
          author_name,
          committer_name,
          offset_value,
          author_date,
          commit_date
        )
      )

      if seen_combinations.contains(combination).result():
        print(".", end='', flush=True)
        continue

      self.git_client.checkout_detached(self.base_ref)
      self.git_client.abort_mailbox_patch()

      print('')
      print(f"Attempt #{attempt} - Trying:")
      print(f" - Author: {author_name}")
      print(f" - Committer: {committer_name}")
      print(f" - Offset: {offset}")
      print(f" - Author Date: {author_date}")
      print(f" - Commit Date: {commit_date}")
      print('')

      # FIXME: Hard-coded temp folder path
      with tempfile.TemporaryDirectory(dir="Z:/") as tmp_dir:
        tmp_patch_filename = path.join(tmp_dir, TEMP_PATCH_FILENAME)

        self.dump_patch(
          notification_commit, author_name, author_date, tmp_patch_filename
        )

        self.git_client.apply_mailbox_patch(
          tmp_patch_filename,
          committer=committer_name,
          commit_date=commit_date,
        )

      current_commit_id = self.git_client.head_revision

      print(f"Target: {target_commit_id}")
      print(f"Current: {current_commit_id}")
      print(f"Total Attempted Combos: {seen_combinations.size().result()}")
      print()
      print()

      if current_commit_id == target_commit_id:
        print("Solution found!")
        self.git_client.export_head_as_patch()

        return
      else:
        seen_combinations.add(combination)
        attempt += 1

  def dump_patch(self, commit, author_name, author_date, tmp_patch_filename):
    with open(tmp_patch_filename, "w") as patch_file:
      decorator = \
        CommitDecorator(
          commit,
          commit_author=author_name,
          commit_date=author_date
        )

      patch_file.write(str(decorator))

  def committer_distribution_for(self, author_name):
    if author_name not in self.committer_distributions:
      distribution = CommitterDistribution(self.git_client, author_name)
      self.committer_distributions[author_name] = distribution

      print(
        f"Committer distribution for {author_name}:\n"
        f"{distribution.committer_frequencies}"
      )

      print()

    return self.committer_distributions[author_name]

  def build_global_commit_time_distribution(self):
    distribution = \
      GlobalCommitOffsetDistribution(
        self.git_client,
        commit_offset_windows_span=COMMIT_WINDOWS_SPAN,
        min_commit_offset=MIN_COMMIT_OFFSET,
        max_commit_offset=MAX_COMMIT_OFFSET
    )

    print(
      f"Global commit time distribution:\n"
      f"{distribution}"
    )

    print()

    return distribution

  def commit_time_distribution_for(self, author_name):
    if author_name not in self.commit_time_distributions:
      distribution = \
        AuthorCommitOffsetDistribution(
          self.git_client,
          author_name,
          commit_offset_windows_span=COMMIT_WINDOWS_SPAN,
          min_commit_offset=MIN_COMMIT_OFFSET,
          max_commit_offset=MAX_COMMIT_OFFSET
        )

      self.commit_time_distributions[author_name] = distribution

      print(
        f"Commit time distribution for {author_name}:\n"
        f"{distribution}"
      )

      print()

    return self.commit_time_distributions[author_name]

  def author_timezone_distribution_for(self, author_name):
    if author_name not in self.timezone_distributions:
      distribution = AuthorTimezoneDistribution(self.git_client, author_name)

      self.timezone_distributions[author_name] = distribution

      print(
        f"Author timezone distribution for {author_name}:\n"
        f"{distribution}"
      )

      print()

    return self.timezone_distributions[author_name]

  def simple_incremental_time_picker_for(self, author_name, tz_offset):
    if author_name not in self.commit_time_pickers:
      self.commit_time_pickers[author_name] = dict()

    if tz_offset not in self.commit_time_pickers[author_name]:
      distribution = self.commit_time_distribution_for(author_name)
      self.commit_time_pickers[author_name][tz_offset] = \
        ProbabilisticIncrementalCommitTimePicker(distribution)

    return self.commit_time_pickers[author_name][tz_offset]

  def probabilistic_incremental_time_picker_for(self, author_name, tz_offset):
    if author_name not in self.commit_time_pickers:
      self.commit_time_pickers[author_name] = dict()

    if tz_offset not in self.commit_time_pickers[author_name]:
      self.commit_time_pickers[author_name][tz_offset] = \
        SimpleIncrementalCommitTimePicker(MIN_COMMIT_OFFSET, MAX_COMMIT_OFFSET)

    return self.commit_time_pickers[author_name][tz_offset]
