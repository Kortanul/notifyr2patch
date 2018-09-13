import lazy_property
from fuzzywuzzy import process
from git import Repo


class GitClient:
  def __init__(self, repo_path):
    self.repo = Repo(repo_path)

  def checkout_detached(self, commit_id):
    self.repo.git.checkout(commit_id)

  def fuzzy_author_search(self, author_name):
    return process.extract(author_name, self.author_list)

  @lazy_property.LazyProperty
  def author_list(self):
    raw_authors = self.repo.git.log('--all', '--format=%aN <%cE>').split('\n')
    unique_authors = sorted(set(raw_authors))

    return unique_authors
