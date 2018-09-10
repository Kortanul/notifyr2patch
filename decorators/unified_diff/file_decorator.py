from decorators.unified_diff.file_hunk_decorator import FileHunkDecorator


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
  def __init__(self, commit_file):
    self.commit_file = commit_file

    self.hunk_decorators = \
      [FileHunkDecorator(file_hunk) for file_hunk in commit_file.hunks]

  @property
  def file_name(self):
    return self.commit_file.filename

  def __str__(self):
    lines = [
      f'--- a/{self.file_name}',
      f'+++ b/{self.file_name}',
      ''.join([str(decorator) for decorator in self.hunk_decorators])
    ]

    return '\n'.join(lines)
