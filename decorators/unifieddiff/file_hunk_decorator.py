from decorators.unifieddiff.hunk_line_decorator import HunkLineDecorator
from decorators.unifieddiff.line_metrics import LineMetrics


# @@ -1,3 +1,9 @@
# +This is an important
# +notice! It should
# +therefore be located at
# +the beginning of this
# +document!
# +
#  This part of the
#  document has stayed the
#  same from version to
# @@ -8,13 +14,8 @@
#  compress the size of the
#  changes.
#
# -This paragraph contains
# -text that is outdated.
# -It will be deleted in the
# -near future.
# -
#  It is important to spell
# -check this dokument. On
# +check this document. On
#  the other hand, a
#  misspelled word isn't
#  the end of the world.
# @@ -22,3 +23,7 @@
#  this paragraph needs to
#  be changed. Things can
#  be added after it.
# +
# +This paragraph contains
# +important new additions
# +to this document.
class FileHunkDecorator:
  def __init__(self, file_hunk):
    self.file_hunk = file_hunk

    self.hunk_line_decorators = \
      [HunkLineDecorator(hunk_line) for hunk_line in file_hunk.lines]

    self.original_metrics = LineMetrics()
    self.new_metrics = LineMetrics()

    self.calculate_line_metrics()

  def __str__(self):
    original_start = self.original_metrics.starting_line_number
    original_length = self.original_metrics.total_line_count

    new_start = self.new_metrics.starting_line_number
    new_length = self.new_metrics.total_line_count

    hunk_range = \
      f'@@ -{original_start},{original_length} +{new_start},{new_length} @@\n'

    line_output = \
      '\n'.join([str(decorator) for decorator in self.hunk_line_decorators])

    return hunk_range + line_output + '\n'

  def calculate_line_metrics(self):
    for line in self.file_hunk.lines:
      self.original_metrics.add_line_number(line.original_line_number)
      self.new_metrics.add_line_number(line.new_line_number)
