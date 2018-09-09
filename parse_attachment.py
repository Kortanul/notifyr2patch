from notifyr_notification import NotifyrNotification

# notification1 = NotifyrNotification('attachment-0001.html')
notification1 = NotifyrNotification('attachment-0001.fuller.html')

print(notification1.details.project_name)
print(notification1.details.project_stash_url)
print(notification1.details.pusher)
print(notification1.details.action)
print(notification1.details.branch_name)

print(notification1.commits[0].id)
print(notification1.commits[0].message)
print(notification1.commits[0].author)
print(notification1.commits[0].date)

print(
  ', '.join(
    map(
      lambda file:file.filename,
      notification1.commits[0].changes[0].files
    )
  )
)
