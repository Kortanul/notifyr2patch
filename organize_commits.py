import argparse

from gitclient.git_client import GitClient
from organizer.commit_organizer import CommitOrganizer


def run_solver():
  args = parse_and_validate_args()

  git_client = GitClient(args.git_repo)

  organizer = \
    CommitOrganizer(git_client, args.source_folder, args.destination_folder)

  organizer.run()


def parse_and_validate_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    "-G",
    "--git-repo",
    help="set the path to a local copy of the repo notifications correspond to"
  )

  parser.add_argument(
    "-S",
    "--source-folder",
    help="set the root path of a folder containing Notifyr HTML attachments"
  )

  parser.add_argument(
    "-D",
    "--destination-folder",
    help="set the root path of the folder where organized attachments should go"
  )

  # read arguments from the command line
  args = parser.parse_args()

  if args.git_repo is None:
    raise ValueError("--git-repo is required")

  if args.source_folder is None:
    raise ValueError("--source-folder is required")

  if args.destination_folder is None:
    raise ValueError("--destination-folder is required")

  return args


