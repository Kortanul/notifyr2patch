from datetime import timedelta


class CommitTimePicker:
  @staticmethod
  def _commit_date_for(author_date, commit_offset):
    if commit_offset is None:
      commit_date = author_date
    else:
      commit_date = author_date + timedelta(seconds=commit_offset)

    return commit_date
