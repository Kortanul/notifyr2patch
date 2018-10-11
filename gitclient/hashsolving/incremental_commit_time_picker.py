from datetime import timedelta
from math import floor

from lazy import lazy


class IncrementalCommitTimePicker:
  def __init__(self, commit_time_distribution,
               min_commit_offset=None,
               max_commit_offset=None):
    self.distribution = commit_time_distribution
    self.min_commit_offset = min_commit_offset
    self.max_commit_offset = max_commit_offset

  def next_simple_commit_date(self, author_date):
    commit_offset = next(self.simple_commit_offsets)

    return self._commit_date_for(author_date, commit_offset)

  def next_probable_commit_date(self, author_date):
    commit_offset = next(self.commit_offsets_in_distribution)

    return self._commit_date_for(author_date, commit_offset)

  @lazy
  def simple_commit_offsets(self):
    return self._simple_commit_offsets()

  @lazy
  def commit_offsets_in_distribution(self):
    return self._commit_offsets_in_distribution()

  def _commit_date_for(self, author_date, commit_offset):
    if commit_offset is None:
      commit_date = author_date
    else:
      commit_date = author_date + timedelta(seconds=commit_offset)

    return commit_date

  def _simple_commit_offsets(self):
    next_commit_offset = -1

    while True:
      next_commit_offset += 1

      if self._commit_offset_after_min_bound(next_commit_offset):
        if self._commit_offset_before_max_bound(next_commit_offset):
          yield next_commit_offset
        else:
          yield None

  def _commit_offsets_in_distribution(self):
    distribution = self.distribution.commit_time_lag_distribution

    buckets = distribution.distribution_values
    max_bucket_index = max(buckets)

    next_commit_offset = -1

    while True:
      next_commit_offset += 1

      commit_offset_within_buckets = next_commit_offset <= max_bucket_index

      commit_offset_after_min_bound = \
        self._commit_offset_after_min_bound(next_commit_offset)

      commit_offset_before_max_bound = \
        self._commit_offset_before_max_bound(next_commit_offset)

      if not commit_offset_within_buckets or not commit_offset_before_max_bound:
        yield None

      elif commit_offset_after_min_bound and \
         self._bucket_exists_for_commit_offset(next_commit_offset, buckets):
        yield next_commit_offset

  def _commit_offset_after_min_bound(self, next_commit_offset):
    return self.min_commit_offset is None or \
           next_commit_offset >= self.min_commit_offset

  def _commit_offset_before_max_bound(self, next_commit_offset):
    return self.max_commit_offset is None or \
           next_commit_offset <= self.max_commit_offset

  def _bucket_exists_for_commit_offset(self, commit_offset, buckets):
    bucket_index = self._commit_offset_to_bucket_index(commit_offset)

    return bucket_index in buckets

  def _commit_offset_to_bucket_index(self, commit_offset):
    return floor(commit_offset / self.distribution.lag_window_length)
