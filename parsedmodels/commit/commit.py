from parsedmodels.commit.change_set import ChangeSet
from parsedmodels.commit.commit_header import CommitHeader


class Commit:
  HEADER_ROW_SELECTOR = '> tbody > tr:nth-of-type(1)'
  CHANGES_ROW_SELECTOR = '> tbody > tr:nth-of-type(2)'

  def __init__(self, commit_table):
    self.header = None
    self.change_set = None

    self._parse_commit_table(commit_table)

  def _parse_commit_table(self, commit_table):
    header_row = commit_table.select_one(self.HEADER_ROW_SELECTOR)
    changes_row = commit_table.select_one(self.CHANGES_ROW_SELECTOR)

    self.header = CommitHeader(header_row)
    self.change_set = ChangeSet(changes_row)

  def __getattr__(self, attr):
    delegates = [
      self.header,
      self.change_set
    ]

    for delegate in delegates:
      if hasattr(delegate, attr):
        return getattr(delegate, attr)

    return getattr(super(Commit, self), attr)
