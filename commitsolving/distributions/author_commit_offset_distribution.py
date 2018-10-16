from commitsolving.distributions.commit_offset_distribution import \
  CommitOffsetDistribution


##
# A commit time offset distribution based on the history of a particular commit
# author.
#
class AuthorCommitOffsetDistribution(CommitOffsetDistribution):
  def __init__(self, git_client, author_name, commit_offset_windows_span,
               max_commit_offset, min_commit_offset=0):
    commits = self._get_commits(git_client, author_name)

    super().__init__(
      commits,
      commit_offset_windows_span,
      max_commit_offset,
      min_commit_offset
    )

  def _get_commits(self, git_client, author_name):
    return git_client.get_commits_by_author(author_name)
