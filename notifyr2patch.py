import argparse

from decorators.gitpatch.commit_decorator import CommitDecorator
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
client.checkout_detached(args.base_ref)

print(client.fuzzy_author_search("brmiller"))
print(client.fuzzy_author_search("Brendan Miller"))

notification = NotifyrNotification(args.notification_file)

print(notification.details.project_name)
print(notification.details.project_stash_url)
print(notification.details.pusher)
print(notification.details.action)
print(notification.details.branch_name)

CommitSolver(client, args.base_ref, notification).run()

# for commit in notification.commits:
#   print('')
#
#   print(CommitDecorator(commit))
#   print('')
