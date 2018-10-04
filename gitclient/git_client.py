from fuzzywuzzy import process
from git import Repo
from lazy import lazy


class GitClient:
  def __init__(self, repo_path):
    self.repo = Repo(repo_path)

  def checkout_detached(self, commit_id):
    self.repo.git.checkout(commit_id)

  def fuzzy_author_search(self, author_name):
    return process.extract(author_name, self.author_list)

  def author_or_committer_commits(self, name):
    author_commits = self.author_commits(name)
    committer_commits = self.committer_commits(name)

    return set(author_commits).union(committer_commits)

  def author_commits(self, author_name):
    commits = \
      list(self.repo.iter_commits(author = author_name, all = True))

    return commits

  def committer_commits(self, committer_name):
    commits = \
      list(self.repo.iter_commits(committer = committer_name, all = True))

    return commits

  @lazy
  def author_list(self):
    raw_authors = self.repo.git.log('--all', '--format=%aN <%cE>').split('\n')
    unique_authors = sorted(set(raw_authors))

    return unique_authors
