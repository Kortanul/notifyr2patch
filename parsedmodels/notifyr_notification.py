from bs4 import BeautifulSoup

from parsedmodels.commit.commit import Commit
from parsedmodels.html_transformer import HtmlTransformer
from parsedmodels.notification_details import NotificationDetails


class NotifyrNotification:
  COMMITS_WRAPPER_SELECTOR = '> tbody > tr:nth-of-type(2)'
  COMMITS_TABLE_SELECTOR = '> td > table'

  def __init__(self, filename):
    self.details = None

    self._parse_file(filename)

  def __getattr__(self, attr):
    return getattr(self.details, attr)

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
    commits_row = soup.table.tr.table.select_one(self.COMMITS_WRAPPER_SELECTOR)
    commit_tables = commits_row.select(self.COMMITS_TABLE_SELECTOR)

    self.commits = [Commit(commit_table) for commit_table in commit_tables]

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
