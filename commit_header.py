import re
import dateutil.parser

from bs4 import BeautifulSoup
from datetime import datetime


class CommitHeader:
  COMMIT_ID_PATTERN = \
    re.compile(r'<a href=".+/commits/(?P<commit_id>[a-zA-z0-9]+)"[^>]+>.+</a>')

  def __init__(self, commit_header_row):
    self.id = ''
    self.message = ''
    self.author = ''
    self.date = datetime.utcfromtimestamp(0)

    self._parse_row(commit_header_row)

  def _parse_row(self, commit_header_row):
    if commit_header_row is not None:
      self._parse_commit_id(commit_header_row)
      self._parse_commit_message(commit_header_row)
      self._parse_commit_author(commit_header_row)
      self._parse_commit_time(commit_header_row)

  def _parse_commit_id(self, commit_header_row):
    commit_matches = \
      self._parse_cell_with_regex(commit_header_row, 1, self.COMMIT_ID_PATTERN)

    if commit_matches is not None:
      self.id = commit_matches['commit_id']

  def _parse_commit_message(self, commit_header_row):
    commit_message = self._parse_text_cell(commit_header_row, 2)

    if commit_message is not None:
      self.message = commit_message

  def _parse_commit_author(self, commit_header_row):
    commit_message = self._parse_and_strip_text_cell(commit_header_row, 3)

    if commit_message is not None:
      self.author = commit_message

  def _parse_commit_time(self, commit_header_row):
    cell_contents = self._get_cell_contents(commit_header_row, 4)

    if cell_contents is not None:
      # It gets harder and harder to find time nowadays.
      # But we still need to try.
      time_element = cell_contents.find('time')

      if time_element is not None:
        time_value = time_element['datetime']

        self.date = dateutil.parser.parse(time_value)

  def _parse_cell_with_regex(self, commit_header_row, cell_index, regex):
    html_content = self._get_cell_html(commit_header_row, cell_index)

    if html_content is not None:
      match = regex.match(html_content)

      if match is not None:
        return match.groupdict()

  def _parse_text_cell(self, commit_header_row, cell_index):
    html_content = self._get_cell_html(commit_header_row, cell_index)

    if html_content is not None:
      proper_spaced = html_content.replace('<br/>', '\n')

      return BeautifulSoup(proper_spaced, 'html.parser').get_text()

  def _parse_and_strip_text_cell(self, commit_header_row, cell_index):
    cell_text = self._parse_text_cell(commit_header_row, cell_index)

    if cell_text is not None:
      return cell_text.strip()

  def _get_cell_html(self, commit_header_row, cell_index):
    cell_contents = self._get_cell_contents(commit_header_row, cell_index)

    if cell_contents is not None:
      html_content = cell_contents.decode_contents()

      return html_content

  def _get_cell_contents(self, commit_header_row, cell_index):
    return commit_header_row.select_one(f"> td:nth-of-type({cell_index})")
