import itertools

from dateutil import tz

from decorators.gitpatch.commit_decorator import CommitDecorator
from gitclient.hashsolving.author_distribution import AuthorDistribution
from gitclient.hashsolving.commit_time_distribution import \
  CommitTimeDistribution


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

      for _ in itertools.repeat(None, 100):
        author_pick = author_distribution.pick_author()

        commit_time_distribution = \
          self.commit_time_distribution_for(author_pick)

        commit_lag_range_pick = \
          commit_time_distribution.pick_author_commit_time_lag_range()

        offset_pick = commit_time_distribution.pick_commit_timezone_offset()

        print(offset_pick)
        print(notification_commit.header.date)

        offset = tz.tzoffset(None, offset_pick)
        print(notification_commit.header.date.astimezone(offset))

        # self.dump_patch(notification_commit)

  def dump_patch(self, commit):
    print(CommitDecorator(commit))

  def commit_time_distribution_for(self, author_name):
    if author_name not in self.commit_time_distributions:
      self.commit_time_distributions[author_name] = \
        CommitTimeDistribution(self.git_client, author_name)

    return self.commit_time_distributions[author_name]
