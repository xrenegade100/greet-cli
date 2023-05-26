class File:
  """
    Class that represents a file detected as a Python file and can be analyzed.
  """

  def __init__(self, name: str, path: str):
    """
      Constructor for the File class.

      Parameters:
      - name (str): The name of the file.
      - path (str): The path of the file.
    """
    self.__name = name
    self.__path = path

  def get_name(self) -> str:
    return self.__name

  def get_path(self) -> str:
    return self.__path