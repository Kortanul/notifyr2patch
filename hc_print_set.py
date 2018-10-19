import argparse

from util.hazelcast_utils import HazelcastUtils


def print_set():
  args = parse_and_validate_args()
  commit_id = args.commit_id

  hazelcast_storage = get_hazelcast_storage(args)
  solutions = hazelcast_storage.get_all_solutions_for(commit_id)

  print("\nAll solutions attempted:")

  for solution in solutions:
    print(solution)


def parse_and_validate_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    "commit_id",
    help="The ID of the commit for which the solution set is being cleared."
  )

  parser.add_argument(
    '-H',
    '--hazelcast-server',
    help='specify a Hazelcast server address and port; repeat for each '
         'additional server in the cluster.',
    required=True,
    action='append'
  )

  # read arguments from the command line
  args = parser.parse_args()

  return args


def get_hazelcast_storage(args):
  return HazelcastUtils.create_hazelcast_storage(args.hazelcast_server)


print_set()
