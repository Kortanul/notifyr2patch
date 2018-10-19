class SolutionStorage:
  def get_all_solutions_for(self, commit_id):
    raise NotImplementedError('Must be implemented by sub-class')

  def get_solution_set_size_for(self, commit_id):
    raise NotImplementedError('Must be implemented by sub-class')

  def clear_solution_set_for(self, commit_id):
    raise NotImplementedError('Must be implemented by sub-class')

  def has_seen(self, commit_id, commit_solution):
    raise NotImplementedError('Must be implemented by sub-class')

  def mark_seen(self, commit_id, commit_solution):
    raise NotImplementedError('Must be implemented by sub-class')
