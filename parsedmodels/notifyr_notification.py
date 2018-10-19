from bs4 import BeautifulSoup

from parsedmodels.commit.commit import Commit
from parsedmodels.html_transformer import HtmlTransformer
from parsedmodels.notification_details import NotificationDetails


class NotifyrNotification:
  COMMIT_TABLE_SELECTOR = '> tbody > tr:nth-of-type(2) > td > table > tbody'

  def __init__(self, filename):
    self.filename = filename
    self.details = None
    self.commits = []

    self._parse_file(filename)

  @property
  def html_content(self):
    with open(self.filename, mode='r', encoding='utf-8') as file:
      return self._extract_content(file)

  def __getattr__(self, attr):
    return getattr(self.details, attr)

  def _parse_file(self, filename):
    soup = BeautifulSoup(self.html_content, 'html.parser')

    self._parse_details(soup)
    self._parse_commits(soup)

  def _parse_details(self, soup):
    notification_header_row = soup.table.tr.table.tr

    self.details = NotificationDetails(notification_header_row)

  def _parse_commits(self, soup):
    commit_table = soup.table.tr.table.select_one(self.COMMIT_TABLE_SELECTOR)

    commit_headers = self._commit_header_rows(commit_table)

    changes_rows = \
      [self._changes_row_for(commit_header) for commit_header in commit_headers]

    self.commits = [
      Commit(commit_header, changes_row)
      for commit_header, changes_row in zip(commit_headers, changes_rows)
    ]

  def _commit_header_rows(self, commit_table):
    if commit_table:
      header_rows = \
        commit_table.find_all(self._has_nonempty_first_cell, recursive=False)

      return header_rows
    else:
      return []

  def _changes_row_for(self, commit_header_row):
    return commit_header_row.find_next_sibling(self._has_empty_first_cell)

  @classmethod
  def _has_nonempty_first_cell(cls, tag):
    first_cell = tag.select_one('> td')
    has_content = first_cell.get_text()

    return has_content

  @classmethod
  def _has_empty_first_cell(cls, tag):
    return not cls._has_nonempty_first_cell(tag)

  def _extract_content(self, file):
    file_content = file.read()

    if HtmlTransformer.contains_nested_markup(file_content):
      return self._extract_inner_content(file_content)
    else:
      return file_content

  # TODO: Move to a decorator or filter pattern.
  @staticmethod
  def _extract_inner_content(file_content):
    extracted_markup = \
      str(
        HtmlTransformer(file_content)
          .unpack_nested_markup()
          .remove_newlines()
          .decode_newlines()
          .decode_nonbreaking_spaces()
          .unescape_markup()
      )

    return extracted_markup
