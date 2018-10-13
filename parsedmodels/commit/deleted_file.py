import re

from parsedmodels.commit.file import File


class DeletedFile(File):
  FILENAME_ELEMENT_SELECTOR = '> td > del'

  FILENAME_PATTERN = \
    re.compile(
      r'<a[^>]*href=".+/commits/[a-zA-z0-9]+#(?P<filename>[^"]+)"[^>]*>'
      r'[^<]+</a>'
    )

  def __init__(self, file_deletion_row):
    super().__init__()

    self._parse_row(
      file_deletion_row, self.FILENAME_ELEMENT_SELECTOR, self.FILENAME_PATTERN
    )

  @property
  def is_deleted(self):
    return True
