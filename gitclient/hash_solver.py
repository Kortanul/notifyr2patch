from collections import Counter
from functools import reduce


class CommitSolver:
  def __init__(self, git_client, base_ref, notification):
    self.git_client = git_client
    self.base_ref = base_ref
    self.notification = notification
    
  def run(self):
    for commit in self.notification.commits:
      print(self._get_author_name_candidates(commit))

  def _get_author_name_candidates(self, commit):
    pusher_candidates = self._get_notification_pusher_candidates()
    commit_candidates = self._get_commit_author_candidates(commit)

    all_candidates = pusher_candidates + commit_candidates

    sorted_candidates = \
      sorted(
        all_candidates,
        key=lambda candidate: candidate[1],
        reverse=True
      )

    sorted_candidate_map = {}

    for candidate in sorted_candidates:
      name = candidate[0]
      weight = candidate[1]

      if name not in sorted_candidate_map:
        sorted_candidate_map[name] = weight

    return list(sorted_candidate_map.keys())

  def _get_notification_pusher_candidates(self):
    return self.git_client.fuzzy_author_search(self.notification.pusher)

  def _get_commit_author_candidates(self, commit):
    return self.git_client.fuzzy_author_search(commit.author)
