import random
from datetime import timedelta

import numpy
from dateutil import tz
from lazy import lazy

from gitclient.hashsolving.value_distribution import ValueDistribution


class CommitTimeDistribution:
  def __init__(self, commits, lag_window_length, lag_window_cutoff):
    self.commits = commits
    self.lag_window_length = lag_window_length
    self.lag_window_cutoff = lag_window_cutoff

  @lazy
  def commit_time_lag_distribution(self):
    offset_lags = numpy.array([
      (commit.committed_datetime - commit.authored_datetime).total_seconds()
      for commit in self.commits
    ])

    # Clip lags longer than `lag_window_cutoff`, then distribute the remaining
    # values into buckets of `lag_window_length` seconds each
    distribution = \
      ValueDistribution(
        offset_lags, self.lag_window_length, 0, self.lag_window_cutoff
      )

    return distribution

  @lazy
  def commit_timezone_offset_distribution(self):
    author_timezone_offsets = [
      self._west_of_utc_to_tzoffset(commit.author_tz_offset)
      for commit in self.commits
    ]

    committer_timezone_offsets = [
      self._west_of_utc_to_tzoffset(commit.committer_tz_offset)
      for commit in self.commits
    ]

    all_offsets = author_timezone_offsets + committer_timezone_offsets

    # Bucket GMT-12 and GMT+12 into 1 second blocks (86,400 blocks total)
    distribution = ValueDistribution(all_offsets, 1, -43200, 43200)

    return distribution

  def pick_commit_date(self, author_date):
    commit_lag_time_range = self.commit_time_lag_distribution.pick_range()

    specific_commit_lag = random.choice(commit_lag_time_range)
    commit_date = author_date + timedelta(seconds=specific_commit_lag)

    return commit_date

  def pick_commit_timezone_offset(self):
    offset_value = self.commit_timezone_offset_distribution.pick_value()

    return tz.tzoffset(None, offset_value)

  def __str__(self):
    return str({
      'commit_time_lags': str(self.commit_time_lag_distribution),
      'timezone_offsets': str(self.commit_timezone_offset_distribution)
    })

  @staticmethod
  def _west_of_utc_to_tzoffset(value):
    # Seconds WEST of UTC is opposite direction from TZ offset
    #
    # See:
    # https://stackoverflow.com/questions/11984618/why-does-python-return-a-negative-timezone-value
    return -value
