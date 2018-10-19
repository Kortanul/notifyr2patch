from commit.solving.distributions.committer_distribution import \
  CommitterDistribution


class AuthorCommitterDistributionFactory:
  def __init__(self, git_client):
    self.git_client = git_client
    self.distributions = {}

  def get_distribution_for(self, author_name):
    if author_name not in self.distributions:
      distribution = CommitterDistribution(self.git_client, author_name)
      self.distributions[author_name] = distribution

      print(
        f"Committer distribution for {author_name}:\n"
        f"{distribution.committer_frequencies}"
      )

      print()

    return self.distributions[author_name]
