import argparse

from commit.commit_importer import CommitImporter
from commit.solving.distributions.factories.author_distribution_factory import \
  AuthorDistributionFactory
from commit.solving.distributions.factories.author_timezone_distribution_factory import \
  AuthorTimezoneDistributionFactory
from gitclient.git_client import GitClient


def bulk_import_commits():
  args = parse_and_validate_args()

  source_pattern = args.source_pattern
  repo_path = args.git_repo
  target_commit = args.target_commit

  git_client = GitClient(repo_path)

  author_distribution_factory = AuthorDistributionFactory(git_client)
  timezone_distribution_factory = AuthorTimezoneDistributionFactory(git_client)

  importer = \
    CommitImporter(
      git_client, author_distribution_factory, timezone_distribution_factory
    )

  importer.import_notification_files(source_pattern, target_commit)


def parse_and_validate_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    "source_pattern",
    help="set the root path or glob pattern for the folder/files of Notifyr "
         "HTML attachments to import."
  )

  parser.add_argument(
    '-G',
    '--git-repo',
    help='set the path to a local copy of the repo into which commits will be '
         'imported.',
    required=True
  )

  parser.add_argument(
    '-C',
    '--target-commit',
    help='specify exactly which commit should be imported out of those in the '
         'notifications in the source path.',
    default=None
  )

  args = parser.parse_args()

  return args


bulk_import_commits()
