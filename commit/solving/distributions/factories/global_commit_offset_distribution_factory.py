from commit.solving.distributions.global_commit_offset_distribution import \
  GlobalCommitOffsetDistribution


class GlobalCommitOffsetDistributionFactory:
  def __init__(self, git_client, min_commit_offset, max_commit_offset,
               offset_windows_span):
    self.distribution = \
      GlobalCommitOffsetDistribution(
        git_client,
        min_commit_offset=min_commit_offset,
        max_commit_offset=max_commit_offset,
        commit_offset_windows_span=offset_windows_span
      )

    print(f"Global commit time distribution:\n{self.distribution}")
    print()

  def get_distribution_for(self, _author_name):
    return self.distribution
