from decorators.unified_diff.file_decorator import FileDecorator


class CommitDecorator:
  def __init__(self, commit):
    self.file_decorators = \
      [FileDecorator(file) for file in commit.change_set.files]

  def __str__(self):
    ''.join([str(decorator) for decorator in self.file_decorators])
