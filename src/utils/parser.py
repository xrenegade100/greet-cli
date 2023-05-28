import os
import ast
from model import greetattribute, greetfunction
from typing import List


class Parser():
    
    def __init__(self, file_path):
        if os.path.isfile(file_path):
            self.functions = []
            self.attributes = []
            self.file_path = file_path
            with open(self.file_path, 'r') as source:
                analyze = source.read()
                code = ast.parse(analyze)
                self.code = code
                self.opened_file = analyze

    def get_functions(self) -> List[greetfunction.GreetFunction]:
        if len(self.functions) > 0:
            return self.functions
        else:
            return None
        
    def get_attributes(self) -> List[greetattribute.GreetAttribute]:
        if len(self.attributes) > 0:
            return self.attributes
        else:
            return None

    def extract_attribute(self):
        self.__extract(self.code)

    def __extract(self, code):
        childs = code.body 
        for index, node in enumerate(childs):
            name = ""
            if isinstance(node, ast.Assign) or (isinstance(node, ast.Expr) and isinstance(node.value, ast.Attribute)):
                if index - 1 >= 0 and isinstance(code.body[index - 1], ast.Expr):
                    name, colls = self.__extract_name(node)
                    start_line = self.__get_comment_first_line(code.body[index - 1].lineno)
                    attribute = greetattribute.GreetAttribute(
                        identifier= name,
                        startLine= start_line,
                        endLine= node.lineno,
                        startColumn= self.__get_comment_first_col(start_line),
                        endColumn= node.col_offset + len(name) + colls,
                        string= "",
                        value= "",
                        comment= ast.literal_eval(code.body[index - 1].value)
                    )
                    self.attributes.append(attribute)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                self.__extract(node)


    def __extract_name(self, node):
        name = ""
        colls = 0
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Attribute):
                name = node.targets[0].attr
                colls = 5
            else: 
                name = node.targets[0].id
        elif (isinstance(node, ast.Expr) and isinstance(node.value, ast.Attribute)):
            name = str(node.value.attr)
            colls = 5
        
        return name, colls
            

        

    def extract_function(self):
        for index, node in enumerate(ast.walk(self.code)):
            if isinstance(node, ast.FunctionDef):
                args = []
                for arg in node.args.args:
                    args.append(arg.arg)
                if isinstance(node.body[0], ast.Expr):
                    function = greetfunction.GreetFunction(
                        identifier= node.name,
                        startLine= node.lineno,
                        endLine= node.body[0].lineno,
                        startColumn= node.col_offset + 4,
                        endColumn= self.__get_comment_last_col(node.body[0].lineno - 1),
                        string= self.__get_func_code(node),
                        args= args,
                        comment= ast.literal_eval(node.body[0].value),
                        entities= []
                    )
                    self.functions.append(function)

    def __get_func_code(self, function):
        start = function.lineno-1
        end = function.body[-1].lineno+1
        temp = ""
        splitted = self.opened_file.split('\n')
        for i , line in enumerate(splitted):
            if i in range(start, end):
                temp += line + '\n'
            elif i > end:
                break
        return temp
    
    def __get_comment_last_col(self, line_number):
        splitted = self.opened_file.split('\n')
        return len(splitted[line_number]) - 1
    
    def __get_comment_first_line(self, end_line):
        splitted = self.opened_file.split('\n')
        i = end_line - 1

        if splitted[i].count('"""') == 2:
                return end_line
        
        i = i - 1 
        
        while i >= 0:
            if '"""' in splitted[i]:
                return i + 1
            else:
                i = i - 1

    def __get_comment_first_col(self, start_line):
        splitted = self.opened_file.split('\n')
        return splitted[start_line - 1].find('"')

