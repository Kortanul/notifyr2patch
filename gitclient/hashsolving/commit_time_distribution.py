import random
from datetime import timedelta

import numpy
from dateutil import tz
from lazy import lazy

FIVE_MINUTES_IN_SECONDS = timedelta(minutes=5).total_seconds()

class CommitTimeDistribution:
  def __init__(self, git_client, author_name):
    self.git_client = git_client
    self.author_name = author_name

  @lazy
  def commits(self):
    return self.git_client.author_or_committer_commits(self.author_name)

  @lazy
  def author_commit_time_lag_distribution(self):
    offset_lags = numpy.array([
      (commit.committed_datetime - commit.authored_datetime).total_seconds()
      for commit in self.commits
    ])

    # Bucket 48 hours of times between author date and commit date into 5
    # minute blocks (576 blocks total)
    return self._calculate_distribution(offset_lags, 576)

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

  def pick_author_commit_time_lag_range(self):
    lag_block_choice = random.choices(
      list(self.author_commit_time_lag_distribution.keys()),
      list(self.author_commit_time_lag_distribution.values())
    )

    lag_block = next(iter(lag_block_choice), 0)

    lag_block_range = \
      numpy.arange(
        FIVE_MINUTES_IN_SECONDS * lag_block,
        FIVE_MINUTES_IN_SECONDS * lag_block + FIVE_MINUTES_IN_SECONDS
      )

    return lag_block_range

  def pick_commit_timezone_offset(self):
    offset_choice = random.choices(
      list(self.commit_timezone_offset_distribution.keys()),
      list(self.commit_timezone_offset_distribution.values())
    )

    offset_value = next(iter(offset_choice), 0)

    return tz.tzoffset(None, offset_value)

  def _calculate_distribution(self, values, bin_count):
    return self._calculate_distribution_for_range(values, 0, bin_count)

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
