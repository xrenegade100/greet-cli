class Config:
  """
    A class representing the configuration for greet-cli.
  """

  def __init__(self, input = './', outputPath = './greet.json', includeClear = False):
    """
      Initialize a new Config object.

      Args:
        -  input (str, optional): The input path. Defaults to './'.
        -  outputPath (str, optional): The output path for the greet.json file. Defaults to './greet.json'.
        -  includeClear (bool, optional): Whether to include analyzed entities with no issues detected in the results.
    """
    self.__input = input
    self.__outputPath = outputPath
    self.__includeClear = includeClear

  def getInput(self):
    return self.__input
  
  def getOutputPath(self):
    return self.__outputPath
  
  def getIncludeClear(self):
    return self.__includeClear
    
class ConfigBuilder:
  """
    A class representing a builder for the Config class.
  """

  def __init__(self):
    """
      Initialize a new ConfigBuilder object.
    """
    self.__input = './'
    self.__outputPath = './greet.json'
    self.__includeClear = False

  def withInput(self, input: str):
    """
      Set the input path.

      Args:
        - input (str): The input path.
    """
    self.__input = input
    return self

  def withOutputPath(self, outputPath: str):
    """
      Set the output path.

      Args:
        - outputPath (str): The output path.
    """
    self.__outputPath = outputPath
    return self

  def withIncludeClear(self, includeClear: bool):
    """
      Set whether to include analyzed entities with no issues detected in the results.

      Args:
        - includeClear (bool): Whether to include analyzed entities with no issues detected in the results.
    """
    self.__includeClear = includeClear
    return self

  def build(self) -> Config:
    """
      Build a Config object.

      Returns:
        - Config: A Config object.
    """
    return Config(self.__input, self.__outputPath, self.__includeClear)