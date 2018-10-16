import argparse
import glob
import os
from datetime import datetime

from decorators.gitpatch.commit_decorator import CommitDecorator
from parsedmodels.notifyr_notification import NotifyrNotification


def parse_and_validate_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    "-S",
    "--source-folder",
    help="set the root path of a folder containing Notifyr HTML attachments"
  )

  parser.add_argument(
    "-D",
    "--destination-folder",
    help="set the ref onto which the patch is being applied"
  )

  # read arguments from the command line
  args = parser.parse_args()

  if args.source_folder is None:
    raise ValueError("--source-folder is required")

  if args.destination_folder is None:
    raise ValueError("--destination-folder is required")

  return args


def organize_notifications(src_folder_path, dest_folder_path):
  create_path(dest_folder_path)

  src_file_glob = f"{src_folder_path}/**/*.html"

  for src_file_path in glob.iglob(src_file_glob, recursive=True):
    src_file_path = normalize_path(src_file_path)

    try:
      notification = NotifyrNotification(src_file_path)

      project_name = notification.project_name
      commits = notification.commits

      if project_name is not None and len(commits) > 0:
        save_notification_files(notification, src_file_path, dest_folder_path)

    except Exception as e:
      print(f"Skipping {src_file_path}: ", e)


def save_notification_files(notification, src_file_path, dest_folder_path):
  dest_parent_folder = get_dest_folder_path(dest_folder_path, notification)

  create_path(dest_parent_folder)

  dest_basename = get_dest_basename(notification, src_file_path)
  full_dest_path = f"{dest_parent_folder}/{dest_basename}"

  save_notification(notification, src_file_path, full_dest_path)
  # save_patches(notification, src_file_path, full_dest_path)


def save_notification(notification, src_file_path, full_dest_path):
  full_html_path = f"{full_dest_path}.html"

  with open(full_html_path, 'w', encoding='utf-8') as html_file:
    print(f"`{src_file_path}` -> `{full_html_path}`")

    html_file.write(str(notification.html_content))


# FIXME Move this to a CommitWriter class
def save_patches(notification, src_file_path, full_dest_path):
  for commit in notification.commits:
    full_patch_path = f"{full_dest_path}.{commit.id}.patch"

    with open(full_patch_path, 'w', encoding='utf-8') as patch_file:
      print(f"`{src_file_path}` -> `{full_patch_path}`")

      decorator = \
        CommitDecorator(
          commit,
          commit_author="FIXME",
          commit_date=datetime.now()
        )

      patch_file.write(str(decorator))


def get_dest_folder_path(dest_folder_path, notification):
  project_name = notification.project_name
  branch_name = notification.branch_name

  dest_parent_folder = f"{dest_folder_path}/{project_name}/{branch_name}"

  return dest_parent_folder


def get_dest_basename(notification, src_file_path):
  commits = notification.commits
  first_commit = next(iter(commits), None)

  commit_date = first_commit.date.strftime('%Y-%m-%d--%H-%M-%S')
  commit_id = first_commit.id

  context_date = extract_date_from_path(src_file_path)
  context_message_id = extract_message_id_from_path(src_file_path)

  dest_basename = \
    f"{context_date}--{commit_date}--{commit_id}--msg-{context_message_id}"

  return dest_basename


def normalize_path(path):
  return path.replace("\\","/")


def create_path(path):
  if not os.path.exists(path):
    os.makedirs(path)


def extract_message_id_from_path(file_path):
  return extract_path_component(file_path, -1)


def extract_date_from_path(file_path):
  return extract_path_component(file_path, -2)


def extract_path_component(file_path, offset):
  dir_name = os.path.dirname(file_path)
  parts = dir_name.split('/')

  return parts[offset]


args = parse_and_validate_args()

src_folder_path = normalize_path(args.source_folder)
dest_folder_path = normalize_path(args.destination_folder)

organize_notifications(src_folder_path, dest_folder_path)
