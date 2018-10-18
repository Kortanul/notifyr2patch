from lazy import lazy

from commitsolving.committimepicking.commit_time_picker import CommitTimePicker


class SimpleIncrementalTimePicker(CommitTimePicker):
  def __init__(self, min_commit_offset, max_commit_offset):
    self.min_commit_offset = min_commit_offset
    self.max_commit_offset = max_commit_offset

  def pick_commit_date(self, author_date):
    commit_offset = next(self.commit_offsets)

    return self._commit_date_for(author_date, commit_offset)

  @lazy
  def commit_offsets(self):
    return self._create_commit_offsets_generator()

  def _create_commit_offsets_generator(self):
    next_commit_offset = self.min_commit_offset - 1

    while True:
      next_commit_offset += 1

      if next_commit_offset <= self.max_commit_offset:
        yield next_commit_offset
      else:
        yield None
