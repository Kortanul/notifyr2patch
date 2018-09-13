

##
# Example:
#    It is important to spell
#   -check this dokument. On
#   +check this document. On
#    the other hand, a
class HunkLineDecorator:
  def __init__(self, hunk_line):
    self.hunk_line = hunk_line

  def __str__(self):
    return f"{self.marker}{self.hunk_line.content}"

  @property
  def marker(self):
    marker_value = self.hunk_line.change_type.value

    # Ensure there is always at least 1 character
    return marker_value.rjust(1, ' ')
