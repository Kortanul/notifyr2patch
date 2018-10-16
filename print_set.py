import argparse

from commitsolving.hazelcast_client import HazelcastClient
from parsedmodels.notifyr_notification import NotifyrNotification


def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    "-F",
    "--notification-file",
    help="set the path to the Notifyr HTML attachment to transcribe"
  )

  # read arguments from the command line
  args = parser.parse_args()

  return args


args = parse_args()
notification = NotifyrNotification(args.notification_file)

for notification_commit in notification.commits:
  target_commit_id = notification_commit.id
  hazelcast_client = HazelcastClient(target_commit_id)

  combinations = hazelcast_client.solution_attempt_set.get_all().result()

  print("\nAll combinations attempted:")

  for combination in combinations:
    print(combination)
