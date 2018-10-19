import random
from collections import defaultdict
from functools import reduce
from operator import itemgetter

from lazy import lazy


class AuthorDistribution:
  def __init__(self, git_client, author_name_pool):
    self.git_client = git_client
    self.author_name_pool = author_name_pool

  @lazy
  def author_names(self):
    return list(self.distribution.keys())

  @lazy
  def author_name_weights(self):
    return list(self.distribution.values())

  @lazy
  def most_frequent_author_name(self):
    sorted_values = \
      sorted(self.distribution.items(), key=itemgetter(1), reverse=True)

    first_value = next(iter(sorted_values), (None, None))

    return first_value[0]

  @lazy
  def distribution(self):
    confidences = self.author_confidences

    total_weight = reduce((lambda x, y: x + y), confidences.values())

    frequencies = {
      name: target_weight/total_weight
      for (name, target_weight) in confidences.items()
    }

    return frequencies

  @lazy
  def author_confidences(self):
    author_confidences = defaultdict(int)

    for author_name in self.author_name_pool:
      candidates = self._get_author_candidates(author_name)

      for candidate_tuple in candidates:
        name = candidate_tuple[0]
        weight = candidate_tuple[1]

        author_confidences[name] += weight

    return author_confidences

  def pick_author(self):
    author_choice = random.choices(
      self.author_names,
      self.author_name_weights
    )

    return next(iter(author_choice), None)

  def _get_author_candidates(self, name):
    return self.git_client.fuzzy_author_search(name)
