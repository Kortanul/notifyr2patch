import os

import git
from fuzzywuzzy import process
from git import Repo
from lazy import lazy


class GitClient:
  def __init__(self, repo_path):
    self.repo_path = repo_path
    self.repo = Repo(repo_path)

  def reset_head_softly(self):
    self.repo.head.reset('HEAD~1', index=False, working_tree=False)

  def apply_plain_patch_to_index(self, filename):
    full_patch_path = self._relative_to_absolute_path(filename)

    return self.repo.git.apply(full_patch_path, '--cached')

  def apply_mailbox_patch(self, filename):
    full_patch_path = self._relative_to_absolute_path(filename)

    return self.repo.git.am(full_patch_path)

  def abort_mailbox_patch(self):
    try:
      return self.repo.git.am('--abort')
    except git.exc.GitCommandError as err:
      if err.status != 128:
        raise

  def checkout_detached(self, commit_id):
    return self.repo.git.checkout(commit_id)

  def fuzzy_author_search(self, author_name):
    return process.extract(author_name, self.author_list)

  def author_or_committer_commits(self, name):
    author_commits = self.author_commits(name)
    committer_commits = self.committer_commits(name)

    return set(author_commits).union(committer_commits)

  def author_commits(self, author_name):
    commits = \
      list(self.repo.iter_commits(author=author_name, all=True))

    return commits

  def committer_commits(self, committer_name):
    commits = \
      list(self.repo.iter_commits(committer=committer_name, all=True))

    return commits

  @lazy
  def author_list(self):
    raw_authors = self.repo.git.log('--all', '--format=%aN <%cE>').split('\n')
    unique_authors = sorted(set(raw_authors))

    return unique_authors


  def _relative_to_absolute_path(self, path):
    return os.path.join(os.getcwd(), path)
