class CommitFileHunk:
  def __init__(self, hunk_tables):
    self.lines = []
  
    self._parse_lines(hunk_tables)

  def _parse_lines(self, hunk_tables):
    pass
