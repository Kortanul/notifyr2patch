from decorators.gitpatch.commit_decorator import CommitDecorator


class PatchWriter:
  @staticmethod
  def write(commit, author, target_filename, author_date=None,
            repo_base_path=None):
    with open(target_filename, 'w', encoding='utf-8') as patch_file:
      decorator = \
        CommitDecorator(
          commit,
          author_name=author,
          author_date=author_date,
          repo_base_path=repo_base_path
        )

      patch_file.write(str(decorator))
