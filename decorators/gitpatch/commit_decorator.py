from decorators.gitpatch.file_decorator import FileDecorator

from decorators.unifieddiff.commit_decorator \
  import CommitDecorator \
  as UnifiedCommitDecorator


class CommitDecorator(UnifiedCommitDecorator):
  GIT_MBOX_DATE_FORMAT = \
    '{d:%a}, {d.day} {d:%b} {d:%Y} {d.hour}:{d.minute:02}:{d.second:02} {d:%z}'

  def __init__(self, commit, author_name=None, author_date=None,
               repo_base_path=None):
    super(CommitDecorator, self).__init__(commit, src_base_path=repo_base_path)

    self._author_name = author_name
    self._author_date = author_date

  @property
  def author_name(self):
    if self._author_name is not None:
      return self._author_name
    else:
      return self.commit.author

  @property
  def author_date(self):
    if self._author_date is not None:
      date = self._author_date
    else:
      date = self.commit.date

    return self.GIT_MBOX_DATE_FORMAT.format(d=date)

  def __str__(self):
    lines = [
      f'From {self.commit.id} Mon Sep 17 00:00:00 2001',
      f'From: {self.author_name}',
      f'Date: {self.author_date}',
      f'Subject: [PATCH] {self.commit.message}',
      '---',
      ''
    ]

    lines_str = '\n'.join(lines)

    return lines_str + super(CommitDecorator, self).__str__()

  def _create_file_decorator(self, file):
    return FileDecorator(file, src_base_path=self.src_base_path)
