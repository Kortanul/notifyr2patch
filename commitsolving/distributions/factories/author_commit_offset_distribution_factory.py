from commitsolving.distributions.author_commit_offset_distribution import \
  AuthorCommitOffsetDistribution


class AuthorCommitOffsetDistributionFactory:
  def __init__(self, git_client, min_commit_offset, max_commit_offset,
               offset_windows_span):
    self.git_client = git_client
    self.min_commit_offset = min_commit_offset
    self.max_commit_offset = max_commit_offset
    self.offset_windows_span = offset_windows_span

    self.distributions = {}

  def get_distribution_for(self, author_name):
    if author_name not in self.distributions:
      distribution = \
        AuthorCommitOffsetDistribution(
          self.git_client,
          author_name,
          min_commit_offset=self.min_commit_offset,
          max_commit_offset=self.max_commit_offset,
          commit_offset_windows_span=self.offset_windows_span
        )

      self.distributions[author_name] = distribution

      print(
        f"Commit time distribution for {author_name}:\n"
        f"{distribution}"
      )

      print()

    return self.distributions[author_name]
