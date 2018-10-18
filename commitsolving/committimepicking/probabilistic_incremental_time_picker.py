from math import floor

from lazy import lazy

from commitsolving.committimepicking.commit_time_picker import CommitTimePicker


class ProbabilisticIncrementalTimePicker(CommitTimePicker):
  def __init__(self, commit_offset_distribution):
    self.offset_distribution = commit_offset_distribution

  def pick_commit_date(self, author_date):
    commit_offset = next(self.commit_offsets)

    return self._commit_date_for(author_date, commit_offset)

  @lazy
  def commit_offsets(self):
    return self._create_commit_offsets_generator()

  def _create_commit_offsets_generator(self):
    distribution = self.offset_distribution.distribution

    buckets = distribution.distribution_values
    max_bucket_index = max(buckets)

    next_commit_offset = distribution.min_value - 1

    while True:
      next_commit_offset += 1

      if next_commit_offset > max_bucket_index:
        yield None

      else:
        yield next_commit_offset

  def _bucket_exists_for_commit_offset(self, commit_offset, buckets):
    bucket_index = self._commit_offset_to_bucket_index(commit_offset)

    return bucket_index in buckets

  def _commit_offset_to_bucket_index(self, commit_offset):
    return floor(commit_offset / self.offset_distribution.lag_window_length)
