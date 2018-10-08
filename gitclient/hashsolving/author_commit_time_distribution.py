from datetime import timedelta

from gitclient.hashsolving.commit_time_distribution import \
  CommitTimeDistribution

LAG_WINDOW_CUTOFF = timedelta(days=14).total_seconds()
LAG_WINDOW_LENGTH = timedelta(minutes=5).total_seconds()


##
# A commit time distribution based on the history of a particular commit author.
#
class AuthorCommitTimeDistribution(CommitTimeDistribution):
  def __init__(self, git_client, author_name):
    commits = self.get_commits(git_client, author_name)

    super().__init__(commits, LAG_WINDOW_LENGTH, LAG_WINDOW_CUTOFF)

  def get_commits(self, git_client, author_name):
    return git_client.get_commits_by_author_or_committer(author_name)
