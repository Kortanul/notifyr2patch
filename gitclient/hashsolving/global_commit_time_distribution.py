from datetime import timedelta

from gitclient.hashsolving.commit_time_distribution import \
    CommitTimeDistribution


LAG_WINDOW_CUTOFF = timedelta(days=30).total_seconds()
LAG_WINDOW_LENGTH = timedelta(minutes=30).total_seconds()


##
# A commit time distribution based on all commits in the repository.
#
class GlobalCommitTimeDistribution(CommitTimeDistribution):
  def __init__(self, git_client):
    commits = self.get_commits(git_client)

    super().__init__(commits, LAG_WINDOW_LENGTH, LAG_WINDOW_CUTOFF)

  def get_commits(self, git_client):
    return git_client.get_all_commits()
