from decorators.git_patch.commit_decorator import CommitDecorator
from parsedmodels.notifyr_notification import NotifyrNotification

# notification1 = NotifyrNotification('sample_inputs/attachment-0001.html')
notification1 = NotifyrNotification('sample_inputs/attachment-0001.fuller.html')

print(notification1.details.project_name)
print(notification1.details.project_stash_url)
print(notification1.details.pusher)
print(notification1.details.action)
print(notification1.details.branch_name)

for commit in notification1.commits:
  print('')

  print(CommitDecorator(commit))
  print('')
