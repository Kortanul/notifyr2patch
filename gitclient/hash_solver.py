import tempfile
from datetime import timedelta
from os import path

from decorators.gitpatch.commit_decorator import CommitDecorator
from gitclient.hashsolving.author_commit_time_distribution import \
    AuthorCommitTimeDistribution
from gitclient.hashsolving.author_distribution import AuthorDistribution
from gitclient.hashsolving.committer_distribution import CommitterDistribution
from gitclient.hashsolving.global_commit_time_distribution import \
    GlobalCommitTimeDistribution
from gitclient.hashsolving.hazelcast_client import HazelcastClient
from gitclient.hashsolving.incremental_commit_time_picker import IncrementalCommitTimePicker

TEMP_PATCH_FILENAME = "temp.patch"


class CommitSolver:
  def __init__(self, git_client, base_ref, notification):
    self.git_client = git_client
    self.base_ref = base_ref
    self.notification = notification

    self.committer_distributions = dict()
    self.commit_time_distributions = dict()
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

      offset = author_commit_time_distribution.pick_commit_timezone_offset()
      offset_value = offset.utcoffset(None)

      author_date = notification_commit.date.astimezone(offset)

      commit_date = \
        self.incremental_time_picker_for(author_name, offset_value) \
            .next_simple_commit_date(author_date)

      # commit_date = \
      #   self.incremental_time_picker_for(author_name, offset_value) \
      #       .next_probable_commit_date(author_date)

      # commit_date = \
      #   author_commit_time_distribution.pick_commit_date(author_date)

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
    distribution = GlobalCommitTimeDistribution(self.git_client)

    print(
      f"Global commit time distribution:\n"
      f"{distribution}"
    )

    print()

    return distribution

  def commit_time_distribution_for(self, author_name):
    if author_name not in self.commit_time_distributions:
      distribution = AuthorCommitTimeDistribution(self.git_client, author_name)
      self.commit_time_distributions[author_name] = distribution

      print(
        f"Commit time distribution for {author_name}:\n"
        f"{distribution}"
      )

      print()

    return self.commit_time_distributions[author_name]

  def incremental_time_picker_for(self, author_name, tz_offset):
    if author_name not in self.commit_time_pickers:
      self.commit_time_pickers[author_name] = dict()

    if tz_offset not in self.commit_time_pickers[author_name]:
      distribution = self.commit_time_distribution_for(author_name)
      self.commit_time_pickers[author_name][tz_offset] = \
        IncrementalCommitTimePicker(
          distribution,
          min_commit_offset=timedelta(days=3).total_seconds(),
          max_commit_offset=timedelta(days=4).total_seconds()
        )

    return self.commit_time_pickers[author_name][tz_offset]
