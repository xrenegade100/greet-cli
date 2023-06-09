from .greetentity import AbstractGreetEntity

class GreetAttribute(AbstractGreetEntity):
    """
    A class representing a greet attribute.
    """

    def __init__(self, identifier: str, startLine: int, endLine: int, startColumn: int, endColumn: int, code: str, value: str, comment: str = ''):
        """
        Constructor for the GreetAttribute class.

        Args:
            identifier (str): The identifier of the attribute.
            startLine (int): The start line of the attribute.
            endLine (int): The end line of the attribute.
            startColumn (int): The start column of the attribute.
            endColumn (int): The end column of the attribute.
            string (str): The string representing the attribute.
            value (str): The value assigned to the attribute.
            comment (str, optional): Optional comment associated with the attribute. Defaults to ''.
        """
        super().__init__(identifier, startLine, endLine, startColumn, endColumn, code=code)
        self.__value = value
        self.__comment = comment

    def getCode(self) -> str:
        """
        Get the string representing the greet attribute.

        Returns:
            str: The string representing the greet attribute.
        """
        return f"""\"\"\"
{self.__comment.strip()}
\"\"\"
{self._AbstractGreetEntity__identifier} = {self.__value}
"""
