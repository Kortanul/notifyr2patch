from decorators.git_patch.file_decorator import FileDecorator

from decorators.unified_diff.commit_decorator \
  import CommitDecorator \
  as UnifiedCommitDecorator


class CommitDecorator(UnifiedCommitDecorator):
  GIT_MBOX_DATE_FORMAT = \
    '{d:%a}, {d.day} {d:%b} {d:%Y} {d.hour}:{d.minute:02}:{d.second:02} {d:%z}'

  @property
  def commit_date(self):
    # return self.commit.date.strftime('%a, %d %b %Y %H:%M:%S %z')
    return self.GIT_MBOX_DATE_FORMAT.format(d=self.commit.date)

  def __str__(self):
    lines = [
      f'From {self.commit.id} Mon Sep 17 00:00:00 2001',
      f'From: {self.commit.author}', # FIXME Email look-up,
      f'Date: {self.commit_date}',
      f'Subject: [PATCH] {self.commit.message}',
      '---',
      ''
    ]

    lines_str = '\n'.join(lines)

    return lines_str + super(CommitDecorator, self).__str__()

  def _create_file_decorator(self, file):
    return FileDecorator(file)
