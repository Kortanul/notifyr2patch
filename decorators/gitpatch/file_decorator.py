    base_output = super(FileDecorator, self).__str__()
    return diff_line + '\n' + base_output

  @property
  def _output_lines_for_new_file(self):
    base_lines = super(FileDecorator, self)._output_lines_for_new_file

    lines = [
      'new file mode 100644',
      *base_lines
    ]

    return lines

  @property
  def _output_lines_for_deleted_file(self):
    base_lines = super(FileDecorator, self)._output_lines_for_deleted_file

    lines = [
      'deleted file mode 100644',
      *base_lines
    ]

    return lines