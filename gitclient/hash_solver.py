import itertools
import tempfile
from os import path

from decorators.gitpatch.commit_decorator import CommitDecorator
from gitclient.hashsolving.author_distribution import AuthorDistribution
from gitclient.hashsolving.commit_time_distribution import \
  CommitTimeDistribution
from gitclient.hashsolving.committer_distribution import CommitterDistribution

TEMP_PATCH_FILENAME = "temp.patch"


class CommitSolver:
  def __init__(self, git_client, base_ref, notification):
    self.git_client = git_client
    self.base_ref = base_ref
    self.notification = notification

    self.committer_distributions = dict()
    self.commit_time_distributions = dict()
    
  def run(self):
    for notification_commit in self.notification.commits:
      target_commit_id = notification_commit.id

      author_name_pool = [
        self.notification.pusher,
        notification_commit.author
      ]

      author_distribution = \
        AuthorDistribution(self.git_client, author_name_pool)

      attempt = 1
      seen_combinations = set()

      while True:
        author_name = author_distribution.pick_author()

        committer_distribution = self.committer_distribution_for(author_name)

        committer_name = committer_distribution.pick_committer()

        commit_time_distribution = \
          self.commit_time_distribution_for(author_name)

        offset = commit_time_distribution.pick_commit_timezone_offset()

        author_date = notification_commit.date.astimezone(offset)

        commit_date = \
          commit_time_distribution.pick_commit_date(author_date)

        combination = (
          author_name,
          committer_name,
          offset.utcoffset(None),
          author_date,
          commit_date
        )

        if combination in seen_combinations:
          print("Skipping ahead...")
          continue
        else:
          seen_combinations.add(combination)

        self.git_client.checkout_detached(self.base_ref)
        self.git_client.abort_mailbox_patch()

        print(f"Attempt #{attempt} - Trying:")
        print(f" - Author: {author_name}")
        print(f" - Committer: {committer_name}")
        print(f" - Offset: {offset}")
        print(f" - Author Date: {author_date}")
        print(f" - Commit Date: {commit_date}")
        print("")

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
        print()
        print()

        if current_commit_id == target_commit_id:
          print("Solution found!")
          self.git_client.export_head_as_patch()
          return

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
      self.committer_distributions[author_name] = \
        CommitterDistribution(self.git_client, author_name)

    return self.committer_distributions[author_name]

  def commit_time_distribution_for(self, author_name):
    if author_name not in self.commit_time_distributions:
      self.commit_time_distributions[author_name] = \
        CommitTimeDistribution(self.git_client, author_name)

    return self.commit_time_distributions[author_name]
