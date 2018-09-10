from decorators.unified_diff.file_decorator \
  import FileDecorator \
  as UnifiedFileDecorator


class FileDecorator(UnifiedFileDecorator):
  def __str__(self):
    diff_line = f'diff --git a/{self.file_name} b/{self.file_name}'

    return diff_line + '\n' + super(FileDecorator, self).__str__()
