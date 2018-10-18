class SolutionStorage:
  def get_solution_set_size(self, commit_id):
    raise NotImplementedError('Must be implemented by sub-class')

  def has_seen(self, commit_id, commit_solution):
    raise NotImplementedError('Must be implemented by sub-class')

  def mark_seen(self, commit_id, commit_solution):
    raise NotImplementedError('Must be implemented by sub-class')
