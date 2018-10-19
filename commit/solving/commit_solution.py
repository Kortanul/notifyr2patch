import tempfile
from os import path

from lazy import lazy

from decorators.gitpatch.patch_writer import PatchWriter

TEMP_PATCH_FILENAME = "temp.patch"


class CommitSolution:
  def __init__(self, notification_commit, author_name, committer_name,
               offset, author_date, commit_date):
    self.notification_commit = notification_commit

    self.author_name = author_name
    self.committer_name = committer_name
    self.offset = offset
    self.author_date = author_date
    self.commit_date = commit_date

  @lazy
  def offset_value(self):
    return self.offset.utcoffset(None)

  def apply_to(self, git_client, base_ref=None, temp_path=None):
    if base_ref is not None:
      git_client.checkout_detached(base_ref)
      git_client.abort_mailbox_patch()

    with tempfile.TemporaryDirectory(dir=temp_path) as tmp_dir:
      tmp_patch_filename = path.join(tmp_dir, TEMP_PATCH_FILENAME)

      PatchWriter.write(
        self.notification_commit,
        self.author_name,
        tmp_patch_filename,
        author_date=self.author_date
      )

      git_client.apply_mailbox_patch(
        tmp_patch_filename,
        committer=self.committer_name,
        commit_date=self.commit_date,
      )

    new_commit_id = git_client.head_revision

    return new_commit_id

  def print_inputs(self):
    print(f" - Author: {self.author_name}")
    print(f" - Committer: {self.committer_name}")
    print(f" - Offset: {self.offset}")
    print(f" - Author Date: {self.author_date}")
    print(f" - Commit Date: {self.commit_date}")
    print('')

  def __str__(self):
    return str(
      (
        self.author_name,
        self.committer_name,
        self.offset_value,
        self.author_date,
        self.commit_date
      )
    )
