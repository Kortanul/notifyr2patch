import argparse

from commit.commit_organizer import CommitOrganizer


def organize_commits():
  args = parse_and_validate_args()

  organizer = CommitOrganizer(args.source_pattern, args.destination_folder)

  organizer.organize()


def parse_and_validate_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    'source_pattern',
    help='set the root path or glob pattern for the folder/files of Notifyr '
         'HTML attachments to organize.'
  )

  parser.add_argument(
    'destination_folder',
    help='set the root path of the folder where organized attachments should '
         'go.'
  )

  # read arguments from the command line
  args = parser.parse_args()

  return args


organize_commits()
