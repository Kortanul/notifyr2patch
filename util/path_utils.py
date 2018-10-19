import os


class PathUtils:
  @staticmethod
  def normalize_path(path):
    return path.replace("\\","/")

  @staticmethod
  def create_path_recursively(path):
    if not os.path.exists(path):
      os.makedirs(path)

  @staticmethod
  def extract_path_component(file_path, offset):
    dir_name = os.path.dirname(file_path)
    parts = dir_name.split('/')

    return parts[offset]
