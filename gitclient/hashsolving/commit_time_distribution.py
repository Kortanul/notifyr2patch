import random
from datetime import timedelta

import numpy
from dateutil import tz
from lazy import lazy

LAG_WINDOW_CUTOFF = timedelta(days=14).total_seconds()
LAG_WINDOW_LENGTH = timedelta(minutes=5).total_seconds()

class CommitTimeDistribution:
  def __init__(self, git_client, author_name):
    self.git_client = git_client
    self.author_name = author_name

  @lazy
  def commits(self):
    return self.git_client.author_or_committer_commits(self.author_name)

  @lazy
  def commit_time_lag_ranges(self):
    return list(self.commit_time_lag_block_distribution.keys())

  @lazy
  def commit_time_lag_range_weights(self):
    return list(self.commit_time_lag_block_distribution.values())

  @lazy
  def commit_time_lag_block_distribution(self):
    offset_lags = numpy.array([
      (commit.committed_datetime - commit.authored_datetime).total_seconds()
      for commit in self.commits
    ])

    scaled_offset_lags = [
      offset_lag / LAG_WINDOW_LENGTH
      for offset_lag in offset_lags
      if offset_lag <= LAG_WINDOW_CUTOFF
    ]

    bucket_count = LAG_WINDOW_CUTOFF / LAG_WINDOW_LENGTH

    distribution = \
      self._calculate_distribution_for_range(
        scaled_offset_lags,
        0,
        bucket_count
      )

    return distribution

  @lazy
  def commit_timezone_offsets(self):
    return list(self.commit_timezone_offset_distribution.keys())

  @lazy
  def commit_timezone_offset_weights(self):
    return list(self.commit_timezone_offset_distribution.values())

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
    return self._calculate_distribution_for_range(all_offsets, -43200, 43200)

  def pick_commit_date(self, author_date):
    random_lag_range = self.pick_commit_time_lag_range()

    random_lag = random.choice(random_lag_range)
    commit_date = author_date + timedelta(seconds=random_lag)

    return commit_date

  def pick_commit_time_lag_range(self):
    try:
      lag_block_choice = random.choices(
        self.commit_time_lag_ranges, self.commit_time_lag_range_weights
      )

      lag_block = next(iter(lag_block_choice), 0)

    except IndexError:
      lag_block = 0

    lag_block_range = \
      numpy.arange(
        LAG_WINDOW_LENGTH * lag_block,
        LAG_WINDOW_LENGTH * lag_block + LAG_WINDOW_LENGTH
      )

    return lag_block_range

  def pick_commit_timezone_offset(self):
    offset_choice = random.choices(
      list(self.commit_timezone_offsets),
      list(self.commit_timezone_offset_weights)
    )

    offset_value = next(iter(offset_choice), 0)

    return tz.tzoffset(None, offset_value)

  def _calculate_distribution_for_range(self, values, start, stop):
    # Avoid divide by zero when there are no values
    if len(values) == 0:
      return {0: 1.0}

    histogram, bins = \
      numpy.histogram(values, bins=numpy.arange(start, stop), density=True)

    distribution_map = dict(zip(bins, histogram))

    simplified_distribution = \
      {offset.item(): distribution.item()
       for (offset, distribution) in distribution_map.items()
       if distribution > 0}

    return simplified_distribution

  def _west_of_utc_to_tzoffset(self, value):
    # Seconds WEST of UTC is opposite direction from TZ offset
    #
    # See:
    # https://stackoverflow.com/questions/11984618/why-does-python-return-a-negative-timezone-value
    return -value
