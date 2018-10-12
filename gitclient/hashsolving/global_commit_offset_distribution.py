from gitclient.hashsolving.commit_offset_distribution import \
    CommitOffsetDistribution


##
# A commit time distribution based on all commits in the repository.
#
class GlobalCommitOffsetDistribution(CommitOffsetDistribution):
  def __init__(self, git_client, commit_offset_windows_span, max_commit_offset,
               min_commit_offset=0):
    commits = self._get_commits(git_client)

    super().__init__(
      commits,
      commit_offset_windows_span,
      max_commit_offset,
      min_commit_offset
    )

  def _get_commits(self, git_client):
    return git_client.get_all_commits()
