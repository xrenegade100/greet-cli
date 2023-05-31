from abc import ABC
from .greetissuetype import GreetIssueType

class AbstractGreetEntity(ABC):
	"""
    	An abstract base class representing a greet entity.
    """
    
	def __init__(self, identifier: str, startLine: int, endLine: int, startColumn: int, endColumn: int, code: str, issue: GreetIssueType = GreetIssueType.CLEAR):
		"""
        Constructor for the abstract greet entity.

        Args:
            startLine (int): The start line of the entity.
            endLine (int): The end line of the entity.
            startColumn (int): The start column of the entity.
            endColumn (int): The end column of the entity.
            string (str): The string extracted from the source code representing the greet entity.
        """
		self.__identifier = identifier
		self.__startLine = startLine
		self.__endLine = endLine
		self.__startColumn = startColumn
		self.__endColumn = endColumn
		self.__code = code
		self.__issue = issue

	def getIdentifier(self) -> str:
		return self.__identifier

	def getStartLine(self) -> int:
		return self.__startLine
	
	def getEndLine(self) -> int:
		return self.__endLine
	
	def getStartColumn(self) -> int:
		return self.__startColumn
	
	def getEndColumn(self) -> int:
		return self.__endColumn
	
	def getIssue(self) -> GreetIssueType:
		return self.__issue

	# Function to set the issue type
	def setIssue(self, issue: GreetIssueType):
		self.__issue = issue

	def getCode(self) -> str:
		return self.__code