from parsedmodels.commit.change_set import ChangeSet
from parsedmodels.commit.commit_header import CommitHeader


class Commit:
  def __init__(self, header_row, changes_row):
    self.header = None
    self.change_set = None

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
