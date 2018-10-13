import re

from parsedmodels.commit.file import File


class RegularFile(File):
  VIEW_CHANGES_CELL_SELECTOR = '> td:nth-of-type(2)'

  FILENAME_PATTERN = \
    re.compile(
      r'<a[^>]*href=".+/commits/[a-zA-z0-9]+#(?P<filename>[^"]+)"[^>]*>'
      r'View changes</a>'
    )

  def __init__(self, file_row):
    super().__init__()

    self.hunks = []

    self._parse_row(
      file_row, self.VIEW_CHANGES_CELL_SELECTOR, self.FILENAME_PATTERN
    )

  @property
  def is_deleted(self):
    return False

  def add_hunk(self, hunk):
    self.hunks.append(hunk)
