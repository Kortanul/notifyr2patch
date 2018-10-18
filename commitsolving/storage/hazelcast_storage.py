from commitsolving.storage.solution_storage import SolutionStorage


class HazelcastStorage(SolutionStorage):
  def __init__(self, hazelcast_client):
    self.client = hazelcast_client
    self.cached_sets = {}

  def get_solution_set_size(self, commit_id):
    attempt_set = self._commit_solution_set_for(commit_id)

    return attempt_set.size().result()

  def has_seen(self, commit_id, commit_solution):
    attempt_set = self._commit_solution_set_for(commit_id)
    attempt_as_str = str(commit_solution)

    return attempt_set.contains(attempt_as_str).result()

  def mark_seen(self, commit_id, commit_solution):
    attempt_set = self._commit_solution_set_for(commit_id)
    attempt_as_str = str(commit_solution)

    attempt_set.add(attempt_as_str)

  def _commit_solution_set_for(self, commit_id):
    if commit_id not in self.cached_sets:
      self.cached_sets[commit_id] = \
        self.client.get_set(commit_id, 'commit_solutions')

    return self.cached_sets[commit_id]

