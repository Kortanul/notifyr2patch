import itertools
from datetime import timedelta

import git
from dateutil import tz
from git import Actor

from decorators.gitpatch.commit_decorator import CommitDecorator
from gitclient.hashsolving.author_distribution import AuthorDistribution
from gitclient.hashsolving.commit_time_distribution import \
  CommitTimeDistribution

TEMP_PATCH_FILENAME = "temp.patch"


class CommitSolver:
  def __init__(self, git_client, base_ref, notification):
    self.git_client = git_client
    self.base_ref = base_ref
    self.notification = notification

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

      for _ in range(1000):
        author_name = author_distribution.pick_author()

        commit_time_distribution = \
          self.commit_time_distribution_for(author_name)

        offset = commit_time_distribution.pick_commit_timezone_offset()

        author_date = notification_commit.date.astimezone(offset)

        commit_lag_range = \
          commit_time_distribution.pick_author_commit_time_lag_range()

        for author_to_commit_lag in commit_lag_range:
          commit_date = author_date + timedelta(seconds=author_to_commit_lag)

          combination = (
            author_name, offset.utcoffset(None), author_date, commit_date
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
          print(f" - Offset: {offset}")
          print(f" - Author Date: {author_date}")
          print(f" - Commit Date: {commit_date}")
          print("")

          self.dump_patch(notification_commit, author_name, author_date)

          self.git_client.apply_mailbox_patch(
            TEMP_PATCH_FILENAME,
            committer=author_name,
            commit_date=commit_date,
          )

          current_commit_id = self.git_client.head_revision

          print(f"Target: {target_commit_id}")
          print(f"Current: {current_commit_id}")

          if current_commit_id == target_commit_id:
            print("Solution found!")
            return

          attempt += 1

      print("Failed to find a solution after 1,000 attempts.")

  def dump_patch(self, commit, author_name, author_date):
    with open(TEMP_PATCH_FILENAME, "w") as patch_file:
      decorator = \
        CommitDecorator(
          commit,
          commit_author=author_name,
          commit_date=author_date
        )

      patch_file.write(str(decorator))

  def commit_time_distribution_for(self, author_name):
    if author_name not in self.commit_time_distributions:
      self.commit_time_distributions[author_name] = \
        CommitTimeDistribution(self.git_client, author_name)

    return self.commit_time_distributions[author_name]
