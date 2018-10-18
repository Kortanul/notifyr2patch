from commitsolving.committimepicking.simple_incremental_time_picker \
  import SimpleIncrementalTimePicker


class SimpleIncrementalTimePickerFactory:
  def __init__(self, min_commit_offset, max_commit_offset):
    self.min_commit_offset = min_commit_offset
    self.max_commit_offset = max_commit_offset

    self.time_pickers = {}

  def get_time_picker_for(self, author_name, tz_offset):
    if author_name not in self.time_pickers:
      self.time_pickers[author_name] = dict()

    if tz_offset not in self.time_pickers[author_name]:
      self.time_pickers[author_name][tz_offset] = \
        SimpleIncrementalTimePicker(
          self.min_commit_offset,
          self.max_commit_offset
        )

    return self.time_pickers[author_name][tz_offset]
