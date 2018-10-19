import glob

from parsedmodels.notifyr_notification import NotifyrNotification
from util.path_utils import PathUtils


class CommitOrganizer:
  def __init__(self, src_path_pattern, dest_folder_path):
    self.src_folder_path = PathUtils.normalize_path(src_path_pattern)
    self.dest_folder_path = PathUtils.normalize_path(dest_folder_path)

  def organize(self):
    PathUtils.create_path_recursively(self.dest_folder_path)

    src_file_glob = f"{self.src_folder_path}/**/*.html"

    for src_file_path in glob.iglob(src_file_glob, recursive=True):
      src_file_path = PathUtils.normalize_path(src_file_path)

      try:
        notification = NotifyrNotification(src_file_path)

        project_name = notification.project_name
        commits = notification.commits

        if project_name is not None and len(commits) > 0:
          self.save_notification_files(notification, src_file_path)

      except Exception as e:
        print(f"Skipping {src_file_path}: ", e)

  def save_notification_files(self, notification, src_file_path):
    dest_parent_folder = \
      self.get_dest_folder_path(self.dest_folder_path, notification)

    PathUtils.create_path_recursively(dest_parent_folder)

    dest_basename = self.get_dest_basename(notification, src_file_path)
    full_dest_path = f"{dest_parent_folder}/{dest_basename}"

    self.save_notification(notification, src_file_path, full_dest_path)

  def save_notification(self, notification, src_file_path, full_dest_path):
    full_html_path = f"{full_dest_path}.html"

    with open(full_html_path, 'w', encoding='utf-8') as html_file:
      print(f"`{src_file_path}` -> `{full_html_path}`")

      html_file.write(str(notification.html_content))

  def get_dest_folder_path(self, dest_folder_path, notification):
    project_name = notification.project_name
    branch_name = notification.branch_name

    dest_parent_folder = f"{dest_folder_path}/{project_name}/{branch_name}"

    return dest_parent_folder

  def get_dest_basename(self, notification, src_file_path):
    commits = notification.commits
    first_commit = next(iter(commits), None)

    commit_date = first_commit.date.strftime('%Y-%m-%d--%H-%M-%S')
    commit_id = first_commit.id

    context_date = self.extract_date_from_path(src_file_path)
    context_message_id = self.extract_message_id_from_path(src_file_path)

    dest_basename = \
      f"{context_date}--{commit_date}--{commit_id}--msg-{context_message_id}"

    return dest_basename

  @staticmethod
  def extract_message_id_from_path(file_path):
    return PathUtils.extract_path_component(file_path, -1)

  @staticmethod
  def extract_date_from_path(file_path):
    return PathUtils.extract_path_component(file_path, -2)

