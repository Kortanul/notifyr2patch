import argparse

from commitsolving.hazelcast_client import HazelcastClient
from commitsolving.storage.hazelcast_storage import HazelcastStorage


def clear_set():
  args = parse_and_validate_args()
  commit_id = args.commit_id

  hazelcast_storage = get_hazelcast_storage(args)

  solution_count = hazelcast_storage.get_solution_set_size_for(commit_id)
  hazelcast_storage.clear_solution_set_for(commit_id)

  print(f"`{solution_count}` solutions for `{commit_id}` cleared.")


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
  server_list = args.hazelcast_server
  client = HazelcastClient(server_list)
  hazelcast_storage = HazelcastStorage(client)

  return hazelcast_storage


clear_set()

