from decorators.unifieddiff.file_decorator import FileDecorator


class CommitDecorator:
  def __init__(self, commit, src_base_path=None):
    self.commit = commit
    self.src_base_path = src_base_path

    self.file_decorators = [
      self._create_file_decorator(file) for file in commit.files
    ]

  def __str__(self):
    return ''.join([str(decorator) for decorator in self.file_decorators])

  def _create_file_decorator(self, file):
    return FileDecorator(file, src_base_path=self.src_base_path)
