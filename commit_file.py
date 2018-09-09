import re


class CommitFile:
  FILENAME_PATTERN = \
    re.compile(
      r'<a[^>]*href=".+/commits/[a-zA-z0-9]+#(?P<filename>[^"]+)"[^>]*>'
      r'View changes</a>'
    )

  def __init__(self, file_header_change_row):
    self.filename = ''
    self.hunks = []

    self._parse_header(file_header_change_row)

  def add_hunk(self, hunk):
    self.hunks.append(hunk)

  def _parse_header(self, file_header_change_row):
    view_changes_cell = file_header_change_row.select_one('> td:nth-of-type(2)')

    if view_changes_cell is not None:
      decoded_contents = view_changes_cell.decode_contents()
      match = self.FILENAME_PATTERN.match(decoded_contents)

      if match is not None:
        self.filename = match.group('filename')
