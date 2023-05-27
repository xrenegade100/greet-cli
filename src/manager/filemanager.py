import os
from src.model.config import Config

class FileManager:
    """
      A class for managing input files and reading their content.
    """

    def __init__(self, config: Config): 
        """
          Initializes the FileManager with a Config object.

          Args:
            config (Config): The configuration object.
        """
        self.__config = config
        self.__files = []

    def getInputFiles(self):
        """
          Returns the list of input files.

          Returns:
            List[str]: The list of input file paths.
        """
        return self.__files

    def loadInputFiles(self):
        """
          Loads the input files based on the configuration.

          Raises:
            FileNotFoundError: If the input path specified in the configuration does not exist.
        """
        PATH = self.__config.getInput()
        if not os.path.exists(PATH):
          raise FileNotFoundError("Input path does not exist: {}".format(PATH))
        self.__files = self.__get_python_files(PATH)
    
    def __get_python_files(self, path):
        """
          Returns all of the Python files in the given path.

          Args:
            path (str): The path to search for Python files.

          Returns:
            List[str]: The list of Python file paths.
        """
        python_files = []
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == '.py':
                python_files.append(path)
            return python_files
        for directory_path, _, file_names in os.walk(path):
            for file_name in file_names:
                if os.path.splitext(file_name)[1] == '.py':
                    python_files.append(os.path.join(directory_path, file_name))
        return python_files
    
    def readInputFile(self, name: str):
      """
        Reads the content of the input file with the given name.

        Args:
          name (str): The name of the input file.

        Returns:
          str: The content of the input file.
      """
      with open(name, 'r') as file:
          data = file.read()
      return data
