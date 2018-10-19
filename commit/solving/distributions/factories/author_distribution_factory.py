from commit.solving.distributions.author_distribution import AuthorDistribution


class AuthorDistributionFactory:
  def __init__(self, git_client):
    self.git_client = git_client

    self.distributions = {}

  def get_distribution_for(self, author_name_pool):
    pool_as_tuple = tuple(author_name_pool)

    if pool_as_tuple not in self.distributions:
      self.distributions[pool_as_tuple] = \
        AuthorDistribution(self.git_client, author_name_pool)

    return self.distributions[pool_as_tuple]

