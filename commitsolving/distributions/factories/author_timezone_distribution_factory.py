from commitsolving.distributions.author_timezone_distribution import \
  AuthorTimezoneDistribution


class AuthorTimezoneDistributionFactory:
  def __init__(self, git_client):
    self.git_client = git_client
    self.distributions = {}

  def get_distribution_for(self, author_name):
    if author_name not in self.distributions:
      distribution = AuthorTimezoneDistribution(self.git_client, author_name)

      self.distributions[author_name] = distribution

      print(
        f"Author timezone distribution for {author_name}:\n"
        f"{distribution}"
      )

      print()

    return self.distributions[author_name]

