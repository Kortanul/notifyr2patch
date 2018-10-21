import argparse
import sys
from datetime import timedelta

from commit.solving.commit_solver import CommitSolver
from commit.solving.distributions.factories.author_commit_offset_distribution_factory import \
  AuthorCommitOffsetDistributionFactory
from commit.solving.distributions.factories.author_committer_distribution_factory import \
  AuthorCommitterDistributionFactory
from commit.solving.distributions.factories.author_distribution_factory import \
  AuthorDistributionFactory
from commit.solving.distributions.factories.author_timezone_distribution_factory import \
  AuthorTimezoneDistributionFactory
from commit.solving.distributions.factories.global_commit_offset_distribution_factory import \
  GlobalCommitOffsetDistributionFactory
from commit.solving.storage.native_set_storage import NativeSetStorage
from commit.solving.timepicking.factories.probabilistic_incremental_time_picker_factory import \
  ProbabilisticIncrementalTimePickerFactory
from commit.solving.timepicking.factories.probabilistic_random_time_picker_factory import \
  ProbabilisticRandomTimePickerFactory
from commit.solving.timepicking.factories.simple_incremental_time_picker_factory import \
  SimpleIncrementalTimePickerFactory
from gitclient.git_client import GitClient
from parsedmodels.notifyr_notification import NotifyrNotification
from util.hazelcast_utils import HazelcastUtils


def run_solver():
  args = parse_and_validate_args()

  repo_path = args.git_repo
  base_ref = args.base_ref
  notification_file_path = args.notification_file
  temp_path = args.temp_path

  git_client = GitClient(repo_path)
  notification = NotifyrNotification(notification_file_path)

  author_distribution_factory = AuthorDistributionFactory(git_client)
  timezone_distribution_factory = AuthorTimezoneDistributionFactory(git_client)

  committer_distribution_factory = \
    AuthorCommitterDistributionFactory(git_client)

  time_picker_factory = get_time_picker_factory(args, git_client)
  solution_storage = get_solution_storage(args)

  solver = \
    CommitSolver(
      git_client,
      author_distribution_factory,
      committer_distribution_factory,
      timezone_distribution_factory,
      time_picker_factory,
      solution_storage,
      temp_path
    )

  solver.solve_all(base_ref, notification)


def parse_and_validate_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    'notification_file',
    help='set the path to the Notifyr HTML attachment to transcribe'
  )

  parser.add_argument(
    '-G',
    '--git-repo',
    help='set the path to a local copy of the repo being patched',
    required=True
  )

  parser.add_argument(
    '-B',
    '--base-ref',
    help='set the ref onto which the patch is being applied',
    required=True
  )

  parser.add_argument(
    '-T',
    '--time-picker',
    help='indicate how commit times -- based off of the author time -- are '
         'picked (default: "prob_rand", for a probabilistic, random time '
         'picker)',
    choices=[
      'prob_incr',
      'prob_rand',
      'simple_incr'
    ],
    default='prob_rand'
  )

  parser.add_argument(
    '-O',
    '--commit-offset-distribution-type',
    help='when using a probabilistic time picker: indicate which population of '
         'commit times is used to compute the probability distribution of '
         'commit times (default: "author", for a probability distribution '
         'based on the history of the commit author)',
    choices=[
      'global',
      'author'
    ],
    default='author'
  )

  parser.add_argument(
    '-w',
    '--commit-offset-windows-span',
    help='when using a probabilistic time picker: indicate the span (in '
         'minutes) of each bucket of commit offsets that the solver should '
         'use when calculating the commit time probability distribution '
         '(default: "5", for buckets of 5 minute windows)',
    type=int,
    default=5
  )

  parser.add_argument(
    '-m',
    '--time-range-min',
    help='indicate the minimum offset (in days) the solver should consider '
         'between author time and commit time '
         '(default: "0", for 0 days after author date)',
    type=float,
    default=0
  )

  parser.add_argument(
    '-M',
    '--time-range-max',
    help='indicate the maximum offset (in days) the solver should '
         'consider between author time and commit time '
         '(default: "30", for 30 days after author date)',
    type=float,
    default=30
  )

  parser.add_argument(
    '-S',
    '--storage-backend',
    help='indicate where already-attempted commit solutions should be tracked'
         '(default: "local_set" for a local, in-memory set).',
    choices=[
      'clustered_hazelcast',
      'local_set'
    ],
    default='local_set'
  )

  parser.add_argument(
    '-H',
    '--hazelcast-server',
    help='when using the Hazelcast storage backend: specify a Hazelcast '
         'server address and port; repeat for each additional server in the'
         'cluster.',
    default=[],
    action='append'
  )

  parser.add_argument(
    '-p',
    '--temp-path',
    help='when hash solving: indicate the path where temporary files should '
         'be written (default: system temp path; use a RAM disk for optimal '
         'performance)'
  )

  args = parser.parse_args()

  if not validate_args(args):
    parser.print_usage(file=sys.stderr)
    exit(1)

  return args


def validate_args(args):
  args_valid = True

  min_commit_offset = args.time_range_min
  max_commit_offset = args.time_range_max

  if min_commit_offset < 0:
    print(
      '--min-commit-offset must be greater than or equal to 0',
      file=sys.stderr
    )

    args_valid = False

  if min_commit_offset > max_commit_offset:
    print(
      '--max-commit-offset must be greater than or equal to min-commit-offset',
      file=sys.stderr
    )

    args_valid = False

  if args.commit_offset_windows_span < 1:
    print(
      '--commit-offset-windows-span must be greater than or equal to 1',
      file=sys.stderr
    )

    args_valid = False

  if args.storage_backend == 'clustered_hazelcast' and \
      len(args.hazelcast_server) == 0:
    print(
      '--hazelcast-server must be specified at least once when using the '
      '"clustered_hazelcast" backend',
      file=sys.stderr
    )

    args_valid = False

  return args_valid


def get_time_picker_factory(args, git_client):
  time_picker_type = args.time_picker

  if time_picker_type == 'simple_incr':
    time_picker_factory = get_simple_time_picker_factory(args)
  else:
    time_picker_factory = \
      get_probabilistic_time_picker_factory(args, time_picker_type, git_client)

  return time_picker_factory


def get_simple_time_picker_factory(args):
  min_commit_offset, max_commit_offset = get_time_range(args)

  time_picker_factory = \
    SimpleIncrementalTimePickerFactory(min_commit_offset, max_commit_offset)

  return time_picker_factory


def get_probabilistic_time_picker_factory(args, picker_type_name, git_client):
  commit_offset_distribution_factory = \
    get_commit_offset_distribution_factory(args, git_client)

  factories = {
    'prob_incr': ProbabilisticIncrementalTimePickerFactory,
    'prob_rand': ProbabilisticRandomTimePickerFactory
  }

  factory_type = factories[picker_type_name]
  time_picker_factory = factory_type(commit_offset_distribution_factory)

  return time_picker_factory


def get_commit_offset_distribution_factory(args, git_client):
  distribution_type_name = args.commit_offset_distribution_type

  commit_offset_windows_span = \
    timedelta(minutes=args.commit_offset_windows_span).total_seconds()

  min_commit_offset, max_commit_offset = get_time_range(args)

  factories = {
    'global': GlobalCommitOffsetDistributionFactory,
    'author': AuthorCommitOffsetDistributionFactory
  }

  factory_type = factories[distribution_type_name]

  commit_offset_distribution_factory = \
    factory_type(
      git_client,
      min_commit_offset,
      max_commit_offset,
      commit_offset_windows_span
    )

  return commit_offset_distribution_factory


def get_time_range(args):
  min_commit_offset = timedelta(days=args.time_range_min).total_seconds()
  max_commit_offset = timedelta(days=args.time_range_max).total_seconds()

  return min_commit_offset, max_commit_offset


def get_solution_storage(args):
  storage_type_name = args.storage_backend

  if storage_type_name == 'clustered_hazelcast':
    storage = get_hazelcast_storage(args)
  else:
    storage = NativeSetStorage()

  return storage


def get_hazelcast_storage(args):
  return HazelcastUtils.create_hazelcast_storage(args.hazelcast_server)


run_solver()
