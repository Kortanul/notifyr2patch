import itertools
from datetime import timedelta

import git
from dateutil import tz

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
      author_name_pool = [
        self.notification.pusher,
        notification_commit.author
      ]

      author_distribution = \
        AuthorDistribution(self.git_client, author_name_pool)

      self.dump_patch(notification_commit)

      for _ in itertools.repeat(None, 1):
        author_name = author_distribution.pick_author()

        commit_time_distribution = \
          self.commit_time_distribution_for(author_name)

        offset = commit_time_distribution.pick_commit_timezone_offset()

        author_date = notification_commit.header.date.astimezone(offset)

        commit_lag_range = \
          commit_time_distribution.pick_author_commit_time_lag_range()

        for author_to_commit_lag in commit_lag_range:
          commit_date = author_date + timedelta(seconds=author_to_commit_lag)

          self.git_client.checkout_detached(self.base_ref)
          self.git_client.abort_mailbox_patch()

          print("Trying:")
          print(f" - Author: {author_name}")
          print(f" - Offset: {offset}")
          print(f" - Author Date: {author_date}")
          print(f" - Commit Date: {commit_date}")

          try:
            self.git_client.apply_mailbox_patch(TEMP_PATCH_FILENAME)
            self.git_client.reset_head_softly()
          except git.exc.GitCommandError as err:
            if err.status != 128:
              raise

  def dump_patch(self, commit):
    with open(TEMP_PATCH_FILENAME, "w") as patch_file:
      patch_file.write(str(CommitDecorator(commit)))

  def commit_time_distribution_for(self, author_name):
    if author_name not in self.commit_time_distributions:
      self.commit_time_distributions[author_name] = \
        CommitTimeDistribution(self.git_client, author_name)

    return self.commit_time_distributions[author_name]
