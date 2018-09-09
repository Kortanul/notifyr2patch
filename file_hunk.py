class FileHunk:
  def __init__(self, hunk_lines_table):
    self.lines = []
  
    self._parse_lines(hunk_lines_table)

  def _parse_lines(self, hunk_lines_table):
    pass
