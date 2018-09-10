from decorators.unified_diff.file_decorator import FileDecorator
from decorators.unified_diff.file_hunk_decorator import FileHunkDecorator
from decorators.unified_diff.hunk_line_decorator import HunkLineDecorator
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

  print(f'{commit.id} by {commit.author} on {commit.date}:')
  print(commit.message)
  print('')

  for file in commit.files:
    print(FileDecorator(file))

  print('')
