from commit_change_set import CommitChangeSet
from commit_header import CommitHeader


class Commit:
  def __init__(self, commit_table):
    self.header = None
    self.change_set = None

    self._parse_commit_table(commit_table)

  def _parse_commit_table(self, commit_table):
    header_row = commit_table.select_one('> tbody > tr:nth-of-type(1)')
    changes_row = commit_table.select_one('> tbody > tr:nth-of-type(2)')

    self.header = CommitHeader(header_row)
    self.change_set = CommitChangeSet(changes_row)

  def __getattr__(self, attr):
    delegates = [
      self.header,
      self.change_set
    ]

    for delegate in delegates:
      if hasattr(delegate, attr):
        return getattr(delegate, attr)

    return getattr(super(), attr)
