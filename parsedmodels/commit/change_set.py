from parsedmodels.commit.file import File
from parsedmodels.commit.file_hunk import FileHunk


class ChangeSet:
  FILE_NAME_HEADER_STYLE = 'background: #ffffff; color: #333333'

  CHANGES_TABLE_CLASS = 'aui'
  DIFF_HUNK_ROW_CLASS = 'diff-hunk'
  SEGMENT_LINES_TABLE_CLASS = 'segmentlines'

  def __init__(self, commit_changes_row):
    self.files = []

    self._parse_commit_changes(commit_changes_row)

  def _parse_commit_changes(self, commit_changes_row):
    changes_table = commit_changes_row.find('table', self.CHANGES_TABLE_CLASS)

    if changes_table is not None:
      change_rows = changes_table.select('> tbody > tr')

      if change_rows is not None:
        for row in change_rows:
          self._parse_row(row)

  def _parse_row(self, row):
    if self._is_file_header_row(row):
      self._parse_file_header(row)

    elif self._is_hunk_row(row):
      self._parse_hunks(row)

    else:
      raise RuntimeError(
        f'Unexpected row encountered. Row contains: #{str(row)}'
      )

  def _parse_file_header(self, row):
    self.files.append(File(row))

  def _parse_hunks(self, hunk_container_row):
    current_file = self._current_file

    if current_file is not None:
      hunk_tables = \
        hunk_container_row.find_all('table', self.SEGMENT_LINES_TABLE_CLASS)

      current_file.add_hunk(FileHunk(hunk_tables))

    else:
      raise RuntimeError(
        'Changes were encountered before a file name header was encountered.'
        f'Row contains: #{str(hunk_container_row)}'
      )

  @classmethod
  def _is_file_header_row(cls, row):
    return row['style'] == cls.FILE_NAME_HEADER_STYLE and \
           len(row.select('> td')) == 2

  @classmethod
  def _is_hunk_row(cls, row):
    return cls.DIFF_HUNK_ROW_CLASS in list(row['class'])

  @property
  def _current_file(self):
    if len(self.files) > 0:
      return self.files[-1]
