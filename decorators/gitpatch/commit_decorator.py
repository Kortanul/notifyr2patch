from decorators.gitpatch.file_decorator import FileDecorator

from decorators.unifieddiff.commit_decorator \
  import CommitDecorator \
  as UnifiedCommitDecorator


class CommitDecorator(UnifiedCommitDecorator):
  GIT_MBOX_DATE_FORMAT = \
    '{d:%a}, {d.day} {d:%b} {d:%Y} {d.hour}:{d.minute:02}:{d.second:02} {d:%z}'

  def __init__(self, commit, commit_author=None, commit_date=None):
    super(CommitDecorator, self).__init__(commit)

    self._commit_author = commit_author
    self._commit_date = commit_date

  @property
  def commit_author(self):
    if self._commit_author is not None:
      return self._commit_author
    else:
      return self.commit.author

  @property
  def commit_date(self):
    if self._commit_date is not None:
      date = self._commit_date
    else:
      date = self.commit.date

    return self.GIT_MBOX_DATE_FORMAT.format(d=date)

  def __str__(self):
    lines = [
      f'From {self.commit.id} Mon Sep 17 00:00:00 2001',
      f'From: {self.commit_author}',
      f'Date: {self.commit_date}',
      f'Subject: [PATCH] {self.commit.message}',
      '---',
      ''
    ]

    lines_str = '\n'.join(lines)

    return lines_str + super(CommitDecorator, self).__str__()

  def _create_file_decorator(self, file):
    return FileDecorator(file)
