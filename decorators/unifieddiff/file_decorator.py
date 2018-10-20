import re

from lazy import lazy

from decorators.unifieddiff.file_hunk_decorator import FileHunkDecorator


LINE_WITH_TRAILING_NEWLINE = r'.*(?:\r)?\n$'
NO_NEWLINE_MESSAGE = '\\ No newline at end of file\n'

##
# Example:
#   --- /path/to/original	timestamp
#   +++ /path/to/new	timestamp
#   @@ -1,3 +1,9 @@
#   +This is an important
#   +notice! It should
#   +therefore be located at
#   +the beginning of this
#   +document!
#   +
#    This part of the
#    document has stayed the
#    same from version to
#   @@ -8,13 +14,8 @@
#    compress the size of the
#    changes.
#
#   -This paragraph contains
#   -text that is outdated.
#   -It will be deleted in the
#   -near future.
#   -
#    It is important to spell
#   -check this dokument. On
#   +check this document. On
#    the other hand, a
#    misspelled word isn't
#    the end of the world.
#   @@ -22,3 +23,7 @@
#    this paragraph needs to
#    be changed. Things can
#    be added after it.
#   +
#   +This paragraph contains
#   +important new additions
#   +to this document.
class FileDecorator:
  def __init__(self, commit_file, src_base_path=None):
    self.commit_file = commit_file
    self.src_base_path = src_base_path

  @property
  def file_name(self):
    return self.commit_file.filename

  @lazy
  def _src_file_lines(self):
    if self.src_base_path:
      full_path = f"{self.src_base_path}/{self.file_name}"

      with open(full_path, mode='r', encoding='utf-8') as orig_file:
        return orig_file.readlines()
    else:
      return []

  @property
  def _src_file_ends_with_newline(self):
    src_file_lines = self._src_file_lines

    return bool(src_file_lines and
                re.match(LINE_WITH_TRAILING_NEWLINE, src_file_lines[-1]))

  @property
  def _diff_ends_at_last_line(self):
    return self._last_line_number_of_diff == self._last_line_number_of_src_file

  @property
  def _last_line_number_of_diff(self):
    max_line = \
      max(
        hunk_line.original_line_number \
        for file_hunks in self.commit_file.hunks \
        for hunk_line in file_hunks.lines
      )

    return max_line

  @property
  def _last_line_number_of_src_file(self):
    return len(self._src_file_lines)

  @property
  def _output_content_lines(self):
    hunk_decorators = \
      [FileHunkDecorator(file_hunk) for file_hunk in self.commit_file.hunks]

    return '\n'.join([str(decorator) for decorator in hunk_decorators])

  @property
  def _last_output_line(self):
    # TODO: Handle when the diff removes the trailing newline. This is rare,
    #       (and frowned upon), but could happen.
    if self._diff_ends_at_last_line and not self._src_file_ends_with_newline:
      return NO_NEWLINE_MESSAGE
    else:
      return ''

  @property
  def _output_lines_for_regular_file(self):
    lines = [
      f'--- a/{self.file_name}',
      f'+++ b/{self.file_name}',
      self._output_content_lines,
      self._last_output_line
    ]

    return lines

  @property
  def _output_lines_for_new_file(self):
    lines = [
      '--- /dev/null',
      f'+++ b/{self.file_name}',
      self._output_content_lines,
      ''
    ]

    return lines

  @property
  def _output_lines_for_deleted_file(self):
    hunk_range = \
      f'@@ -{1},{self._last_line_number_of_src_file} +0,0 @@'

    deletion_lines = \
      ''.join([f"-{original_line}" for original_line in self._src_file_lines])

    lines = [
      f'--- a/{self.file_name}',
      '+++ /dev/null',
      hunk_range,
      deletion_lines
    ]

    if not self._src_file_ends_with_newline:
      lines.append(NO_NEWLINE_MESSAGE)

    return lines

  def __str__(self):
    if self.commit_file.is_deleted:
      lines = self._output_lines_for_deleted_file
    elif self.commit_file.is_new:
      lines = self._output_lines_for_new_file
    else:
      lines = self._output_lines_for_regular_file

    return '\n'.join(lines)
