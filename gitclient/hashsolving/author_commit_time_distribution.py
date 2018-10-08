from gitclient.hashsolving.commit_time_distribution import \
  CommitTimeDistribution


##
# A commit time distribution based on the history of a particular commit author.
#
class AuthorCommitTimeDistribution(CommitTimeDistribution):
  def __init__(self, git_client, author_name):
    super().__init__(self.get_commits(git_client, author_name))

  def get_commits(self, git_client, author_name):
    return git_client.get_commits_by_author_or_committer(author_name)
