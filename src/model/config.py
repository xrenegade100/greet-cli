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
    