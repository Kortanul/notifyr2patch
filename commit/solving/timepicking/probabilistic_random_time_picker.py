from commit.solving.timepicking.commit_time_picker import CommitTimePicker


class ProbabilisticRandomTimePicker(CommitTimePicker):
  def __init__(self, commit_offset_distribution):
    self.commit_offset_distribution = commit_offset_distribution

  def pick_commit_date(self, author_date):
    commit_offset = self.commit_offset_distribution.pick_commit_offset()

    return self._commit_date_for(author_date, commit_offset)
