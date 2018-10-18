class ProbabilisticTimePickerFactory:
  def __init__(self, commit_offset_distribution_factory):
    self.commit_offset_distribution_factory = commit_offset_distribution_factory

    self.time_pickers = {}

  def get_time_picker_for(self, author_name, tz_offset):
    if author_name not in self.time_pickers:
      self.time_pickers[author_name] = dict()

    if tz_offset not in self.time_pickers[author_name]:
      distribution = \
        self.commit_offset_distribution_factory\
            .get_distribution_for(author_name)

      self.time_pickers[author_name][tz_offset] = \
        self._create_time_picker(distribution)

    return self.time_pickers[author_name][tz_offset]

  def _create_time_picker(self, distribution):
    raise NotImplementedError('Must be implemented by sub-class')
