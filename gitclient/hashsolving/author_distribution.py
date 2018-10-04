import random
from collections import defaultdict
from functools import reduce

from lazy import lazy


class AuthorDistribution:
  def __init__(self, git_client, author_name_pool):
    self.git_client = git_client
    self.author_names = author_name_pool

  def pick_author(self):
    author_choice = random.choices(
      list(self.author_frequencies.keys()),
      list(self.author_frequencies.values())
    )

    return next(iter(author_choice), None)

  @lazy
  def author_frequencies(self):
    confidences = self._raw_target_confidences

    total_weight = reduce((lambda x, y: x + y), confidences.values())

    frequencies = {
      name: target_weight/total_weight
      for (name, target_weight) in confidences.items()
    }

    return frequencies

  @property
  def _raw_target_confidences(self):
    target_confidences = defaultdict(int)

    for author_name in self.author_names:
      candidate_confidences = self._get_author_candidates(author_name)

      for confidence_tuple in candidate_confidences:
        name = confidence_tuple[0]
        weight = confidence_tuple[1]

        final_weight = target_confidences[name] + weight
        target_confidences[name] = final_weight

    return target_confidences

  def _get_author_candidates(self, name):
    return self.git_client.fuzzy_author_search(name)
