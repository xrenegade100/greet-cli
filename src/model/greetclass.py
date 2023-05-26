from src.model.greetentity import AbstractGreetEntity
from typing import List 
 
class GreetClass():
  """
    Class that represents a class found in a source code file.
  """

  def __init__(self, name: str, entities: List[AbstractGreetEntity]  = []):
    """
      Constructor for a GreetClass.

      Parameters:
      - name (str): The name of the class.
      - entities (List[AbstractGreetEntity], optional): A list of greeting entities associated with the class.
        Default is an empty list.
      
        @see src.model.greetentity.AbstractGreetEntity
      """
    self.__name = name
    self.__entities: List[AbstractGreetEntity] = entities
    return

  def getName(self):
    return self.__name
  
  def getEntities(self):
    return self.__entities