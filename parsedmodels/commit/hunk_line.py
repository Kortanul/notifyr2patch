from enum import Enum

from parsedmodels.html_transformer import HtmlTransformer


class ChangeType(Enum):
  CONTEXT = ''
  REMOVED = '-'
  ADDED = '+'

class HunkLine:
  LINE_NUMBER_SELECTOR = 'td.line.number'
  MARKER_TYPE_SELECTOR = 'td.line.marker'
  LINE_CONTENT_SELECTOR = "td[class='line']"

  def __init__(self, hunk_line_row):
    self.original_line_number = -1
    self.new_line_number = -1
    self.change_type = ChangeType.CONTEXT
    self.content = ''

    self._parse_hunk_line_row(hunk_line_row)

  @property
  def is_new(self):
    return self.original_line_number == -1

  def _parse_hunk_line_row(self, hunk_line_row):
    self._parse_original_line_number(hunk_line_row)
    self._parse_new_line_number(hunk_line_row)
    self._parse_change_type(hunk_line_row)
    self._parse_line_content(hunk_line_row)

  def _parse_original_line_number(self, hunk_line_row):
    original_line_number = self._parse_line_number(hunk_line_row, 0)

    if original_line_number is not None:
      self.original_line_number = original_line_number

  def _parse_new_line_number(self, hunk_line_row):
    new_line_number = self._parse_line_number(hunk_line_row, 1)

    if new_line_number is not None:
      self.new_line_number = new_line_number

  def _parse_change_type(self, hunk_line_row):
    marker_cell = hunk_line_row.select_one(self.MARKER_TYPE_SELECTOR)

    if marker_cell is not None:
      marker_type = marker_cell.get_text()
      self.change_type = ChangeType(marker_type)

  def _parse_line_content(self, hunk_line_row):
    content_cell = hunk_line_row.select_one(self.LINE_CONTENT_SELECTOR)

    if content_cell is not None:
      self.content = str(
        HtmlTransformer(content_cell.get_text()).decode_nonbreaking_spaces()
      )

  def _parse_line_number(self, hunk_line_row, index):
    line_numbers = hunk_line_row.select(self.LINE_NUMBER_SELECTOR)

    if line_numbers is not None and len(line_numbers) > index:
      line_number_text = line_numbers[index].get_text()

      if line_number_text:
        return int(line_number_text)
