from commit_changes import CommitChanges
from commit_details import CommitHeader


class Commit:
  def __init__(self, commit_table):
    self.header = None
    self.changes = None

    self._parse_commit_table(commit_table)

  def _parse_commit_table(self, commit_table):
    header_row = commit_table.select_one('> tbody > tr:nth-of-type(1)')
    changes_row = commit_table.select_one('> tbody > tr:nth-of-type(2)')

    self.header = CommitHeader(header_row)
    self.changes = [CommitChanges(changes_row)]

  def __getattr__(self, attr):
    return getattr(self.header, attr)
