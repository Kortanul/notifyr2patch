import re

from lazy import lazy

from parsedmodels.commit.file import File


class RegularFile(File):
  VIEW_CHANGES_CELL_SELECTOR = '> td:nth-of-type(2)'

  FILENAME_PATTERN = \
    re.compile(
      r'<a[^>]*href=".+/commits/[a-zA-z0-9]+#(?P<filename>[^"]+)"[^>]*>'
      r'View changes</a>'
    )

  def __init__(self, file_header_row):
    super().__init__()

    self.hunks = []

    self._parse_header_row(
      file_header_row, self.VIEW_CHANGES_CELL_SELECTOR, self.FILENAME_PATTERN
    )

  @property
  def is_deleted(self):
    return False

  @lazy
  def is_new(self):
    return all(hunk.is_new for hunk in self.hunks)

  def add_hunk(self, hunk):
    self.hunks.append(hunk)
