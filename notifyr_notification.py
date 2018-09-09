from bs4 import BeautifulSoup

from commit import Commit
from html_transformer import HtmlTransformer
from notification_details import NotificationDetails


class NotifyrNotification:
  def __init__(self, filename):
    self.details = None

    self._parse_file(filename)

  def _parse_file(self, filename):
    with open(filename) as file:
      content = self._extract_content(file)
      soup = BeautifulSoup(content, 'html.parser')

      self._parse_details(soup)
      self._parse_commits(soup)

  def _parse_details(self, soup):
    notification_header_row = soup.table.tr.table.tr

    self.details = NotificationDetails(notification_header_row)

  def _parse_commits(self, soup):
    commits_row = soup.table.tr.table.select_one('> tbody > tr:nth-of-type(2)')

    first_commit_table = commits_row.select_one('> td:nth-of-type(1) > table')

    self.commits = [Commit(first_commit_table)]

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
          .decode_spaces()
          .unescape_markup()
      )

    return extracted_markup
