import argparse

from gitclient.git_client import GitClient
from gitclient.hash_solver import CommitSolver
from parsedmodels.notifyr_notification import NotifyrNotification


def parse_args():
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

  return args


args = parse_args()

client = GitClient(args.git_repo)
notification = NotifyrNotification(args.notification_file)

CommitSolver(client, args.base_ref, notification).run()
