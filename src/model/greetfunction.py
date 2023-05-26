from .greetentity import AbstractGreetEntity
from typing import List

class GreetFunction(AbstractGreetEntity):
  """
    A class representing a greet function found in a source code file.
  """

  def __init__(self, identifier: str, startLine: int, endLine: int, startColumn: int, endColumn: int, string: str, args: List[str] = [], comment = '', entities: List[AbstractGreetEntity] = []):
    """
    Constructor for the GreetFunction class.

    Args:
        startLine (int): The start line of the greet function.
        endLine (int): The end line of the greet function.
        startColumn (int): The start column of the greet function.
        endColumn (int): The end column of the greet function.
        string (str): The string representing the greet function.
    """
    super().__init__(identifier, startLine, endLine, startColumn, endColumn, string)
    self.__args = args
    self.__comment = comment
    self.__entities = entities

  def getEntities(self) -> List[AbstractGreetEntity]:
    """
      Get the entities associated with the greet function.

      Returns:
        List[AbstractGreetEntity]: The entities associated with the greet function.
    """
    return self.__entities

  def getString(self) -> str:
    """
      Get the string representing the greet function.

      Returns:
        str: The string representing the greet function.
    """
    argsList = []
    for arg in self.__args:
      argsList.append(str(arg))

    argsString = ", ".join(argsList)

    return f"""{self.__comment}
def {self._AbstractGreetEntity__identifier}({argsString}):
    """

