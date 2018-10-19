class LineMetrics:
  def __init__(self):
    self.line_numbers = []

  def add_line_number(self, line_number):
    if line_number != -1:
      self.line_numbers.append(line_number)

  @property
  def starting_line_number(self):
    return self._min_line_number

  @property
  def total_line_count(self):
    if self.line_numbers:
      return self._max_line_number - self._min_line_number + 1
    else:
      return 0

  @property
  def _min_line_number(self):
    if self.line_numbers:
      return min(self.line_numbers)
    else:
      return 0

  @property
  def _max_line_number(self):
    if self.line_numbers:
      return max(self.line_numbers)
    else:
      return 0
