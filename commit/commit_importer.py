import glob

from commit.solving.commit_solution import CommitSolution
from parsedmodels.notifyr_notification import NotifyrNotification
from util.path_utils import PathUtils


class CommitImporter:
  def __init__(self, git_client, author_distribution_factory,
               timezone_distribution_factory):
    self.git_client = git_client

    self.author_distribution_factory = author_distribution_factory
    self.timezone_distribution_factory = timezone_distribution_factory

  def import_notification_files(self, src_path_pattern, target_commit=None):
    normalized_src_path = PathUtils.normalize_path(src_path_pattern)

    src_file_glob = f"{normalized_src_path}/**/*.html"

    for src_file_path in glob.iglob(src_file_glob, recursive=True):
      print(f"Importing notification file: {src_file_path}")

      notification = NotifyrNotification(src_file_path)

      self.import_notification(notification, target_commit)

  def import_notification(self, notification, target_commit=None):
    for notification_commit in notification.commits:
      if target_commit is None or target_commit == notification_commit.id:
        self.import_commit(notification, notification_commit)

  def import_commit(self, notification, notification_commit):
    commit_solution = \
      self.build_commit_solution(notification, notification_commit)

    print('Importing commit:')
    print(f" - Original ID: {notification_commit.id}")
    commit_solution.print_inputs()

    commit_id = commit_solution.apply_to(self.git_client)

    print()
    print(f"Commit imported as: {commit_id}")
    print()
    print()

  def build_commit_solution(self, notification, notification_commit):
    author_distribution = \
      self._get_author_distribution(notification, notification_commit)

    author_name = author_distribution.most_frequent_author_name

    author_timezone_distribution = \
      self.timezone_distribution_factory.get_distribution_for(author_name)

    offset = author_timezone_distribution.most_frequent_timezone_offset
    author_date = notification_commit.date.astimezone(offset)

    commit_solution = \
      CommitSolution(
        notification_commit=notification_commit,
        author_name=author_name,
        committer_name=None,
        offset=offset,
        author_date=author_date,
        commit_date=None
      )

    return commit_solution

  def _get_author_distribution(self, notification, notification_commit):
    author_name_pool = [notification.pusher, notification_commit.author]

    distribution = \
      self.author_distribution_factory.get_distribution_for(author_name_pool)

    return distribution
