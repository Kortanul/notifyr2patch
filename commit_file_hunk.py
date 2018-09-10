from hunk_line import HunkLine


class CommitFileHunk:
  def __init__(self, hunk_tables):
    self.lines = []
  
    self._parse_hunk_tables(hunk_tables)

  def _parse_hunk_tables(self, hunk_tables):
    if hunk_tables is not None:
      for hunk_table in hunk_tables:
        self._parse_hunk_lines(hunk_table)

  def _parse_hunk_lines(self, hunk_table):
    hunk_line_rows = hunk_table.find_all('tr')

    for hunk_line_row in hunk_line_rows:
      self.lines.append(HunkLine(hunk_line_row))
