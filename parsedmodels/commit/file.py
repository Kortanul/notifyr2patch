import re


class File:
  def __init__(self):
    self.filename = ''

  @property
  def is_deleted(self):
    raise NotImplementedError()

  def _parse_row(self, row, filename_element_selector, filename_pattern):
    deletion_element = row.select_one(filename_element_selector)

    if deletion_element is not None:
      decoded_contents = deletion_element.decode_contents()

      self._parse_filename_from_content(filename_pattern, decoded_contents)

  def _parse_filename_from_content(self, pattern, content):
    match = pattern.match(content)

    if match is not None:
      self.filename = match.group('filename')
