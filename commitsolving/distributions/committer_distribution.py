import random
from collections import defaultdict
from functools import reduce
from operator import itemgetter

from lazy import lazy


class CommitterDistribution:
  def __init__(self, git_client, author_name):
    self.git_client = git_client
    self.author_name = author_name

  @lazy
  def commits(self):
    return self.git_client.get_commits_by_author(self.author_name)

  @lazy
  def committer_names(self):
    return list(self.committer_frequencies.keys())

  @lazy
  def committer_name_weights(self):
    return list(self.committer_frequencies.values())

  @lazy
  def most_frequent_committer_name(self):
    sorted_values = \
      sorted(
        self.committer_frequencies.items(),
        key=itemgetter(1),
        reverse=True
      )

    first_value = next(iter(sorted_values), (None, None))

    return first_value[0]

  @lazy
  def committer_frequencies(self):
    appearance_counts = self.committer_appearance_counts

    total_appearances = \
      reduce((lambda x, y: x + y), appearance_counts.values(), 0)

    if total_appearances == 0:
      frequencies = {self.author_name: 1.0}
    else:
      frequencies = {
        name: appearance_count/total_appearances
        for (name, appearance_count) in appearance_counts.items()
      }

    return frequencies

  @lazy
  def committer_appearance_counts(self):
    appearance_counts = defaultdict(int)

    for commit in self.commits:
      committer = commit.committer
      committer_str = f"{committer.name} <{committer.email}>"

      appearance_counts[committer_str] += 1

    return appearance_counts

  def pick_committer(self):
    committer_choice = random.choices(
      self.committer_names,
      self.committer_name_weights
    )

    return next(iter(committer_choice), None)
