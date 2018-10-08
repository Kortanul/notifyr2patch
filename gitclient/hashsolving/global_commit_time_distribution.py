from gitclient.hashsolving.commit_time_distribution import \
    CommitTimeDistribution


##
# A commit time distribution based on all commits in the repository.
#
class GlobalCommitTimeDistribution(CommitTimeDistribution):
  def __init__(self, git_client):
    super().__init__(self.get_commits(git_client))

  def get_commits(self, git_client):
    return git_client.get_all_commits()
