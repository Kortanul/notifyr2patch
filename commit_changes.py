from commit_file import CommitFile
from file_hunk import FileHunk


class CommitChanges:
  FILE_NAME_HEADER_STYLE = 'background: #ffffff; color: #333333'

  def __init__(self, commit_changes_row):
    self.files = []

    self.parse_commit_changes(commit_changes_row)

  def parse_commit_changes(self, commit_changes_row):
    changes_table = commit_changes_row.find('table', 'aui')

    if changes_table is not None:
      change_rows = changes_table.select('> tbody > tr')

      if change_rows is not None:
        list(map(lambda row: self.parse_row(row), change_rows))

  def parse_row(self, row):
    current_file = self.current_file

    if (row['style'] == self.FILE_NAME_HEADER_STYLE and
        len(row.select('> td')) == 2):
      self.files.append(CommitFile(row))

    elif current_file is not None:
      current_file.add_hunk(FileHunk(row))

    else:
      raise RuntimeError(
        'Changes were encountered before a file name header was encountered.'
        f"Row contains: #{str(row)}"
      )

  @property
  def current_file(self):
    if len(self.files) > 0:
      return self.files[-1]
