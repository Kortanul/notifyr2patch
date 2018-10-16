import argparse

from gitclient.git_client import GitClient
from gitclient.commit_solver import CommitSolver
from parsedmodels.notifyr_notification import NotifyrNotification


def parse_and_validate_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    "-G",
    "--git-repo",
    help="set the path to a local copy of the repo being patched"
  )

  parser.add_argument(
    "-B",
    "--base-ref",
    help="set the ref onto which the patch is being applied"
  )

  parser.add_argument(
    "-F",
    "--notification-file",
    help="set the path to the Notifyr HTML attachment to transcribe"
  )

  # read arguments from the command line
  args = parser.parse_args()

  if args.git_repo is None:
    raise ValueError("--git-repo is required")

  if args.base_ref is None:
    raise ValueError("--base-ref is required")

  if args.notification_file is None:
    raise ValueError("--base-ref is required")

  return args


args = parse_and_validate_args()

repo_path = args.git_repo
base_ref = args.base_ref
notification_file_path = args.notification_file

git_client = GitClient(repo_path)
notification = NotifyrNotification(notification_file_path)

CommitSolver(git_client, base_ref, notification).run()
