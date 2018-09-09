import re


class NotificationDetails:
  PROJECT_PATTERN = \
    re.compile(r'<a href="(?P<stash_url>[^\"]+)"[^>]+>(?P<project>.+)</a>')

  ACTION_PATTERN = \
    re.compile(
      r'<div[^>]+>\n(?P<user>.+) has\s?\n?'
      r'<span class="il">(?P<action>.+)</span> '
      r'to: \'(?P<branch>[^\']+)\''
    )

  def __init__(self, notification_header_row):
    self.project_name = ''
    self.project_stash_url = ''

    self.pusher = ''
    self.action = ''
    self.branch_name = ''

    self.parse_row(notification_header_row)

  def parse_row(self, notification_header_row):
    notification_header_cell = notification_header_row.td

    self.parse_project(notification_header_cell)
    self.parse_action(notification_header_cell)

  def parse_project(self, notification_header_cell):
    project_element = notification_header_cell.contents[2]

    if project_element is not None:
      match = self.PROJECT_PATTERN.match(str(project_element))

      if match is not None:
        self.project_name = match.group('project')
        self.project_stash_url = match.group('stash_url')

  def parse_action(self, notification_header_cell):
    action_element = notification_header_cell.contents[-1]

    if action_element is not None:
      match = self.ACTION_PATTERN.match(str(action_element))

      if match is not None:
        self.pusher = match.group('user')
        self.action = match.group('action')
        self.branch_name = match.group('branch')
