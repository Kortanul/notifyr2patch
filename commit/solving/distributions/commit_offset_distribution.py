import random

import numpy
from lazy import lazy

from commit.solving.distributions.value_distribution import ValueDistribution


class CommitOffsetDistribution:
  def __init__(self, commits, commit_offset_windows_span, max_commit_offset,
               min_commit_offset=0):
    self.commits = commits

    self.commit_offset_windows_span = commit_offset_windows_span

    self.min_commit_offset = min_commit_offset
    self.max_commit_offset = max_commit_offset

  @lazy
  def distribution(self):
    commit_offsets = numpy.array([
      (commit.committed_datetime - commit.authored_datetime).total_seconds()
      for commit in self.commits
    ])

    # Clip lags longer than `lag_window_cutoff`, then distribute the remaining
    # values into buckets of `lag_window_length` seconds each
    distribution = \
      ValueDistribution(
        commit_offsets,
        self.commit_offset_windows_span,
        self.min_commit_offset,
        self.max_commit_offset
      )

    return distribution

  @lazy
  def most_frequent_commit_offset(self):
    return self.distribution.most_frequent_value

  def pick_commit_offset(self):
    commit_offset_range = self.distribution.pick_range()
    commit_offset = random.choice(commit_offset_range)

    return commit_offset

  def __str__(self):
    return str(self.distribution)
