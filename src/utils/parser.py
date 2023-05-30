import os
import ast
from src.model import greetattribute, greetfunction
from typing import List
from enum import Enum

class Structures(Enum):
    LIST = 0
    TUPLE = 1
    SET = 2
    DICTIONARY = 3

class Parser():
    
    def __init__(self, parsed_file):
        self.DATA_STRUCTURES_COLSURES = {
            "list_start": "[",
            "list_end": "]",
            "graph_start": "{",
            "graph_end": "}",
            "tuple_start": "(",
            "tuple_end": ")"
        }
        self.code = None
        self.functions = []
        self.attributes = []
        if len(parsed_file) > 0:
            code = ast.parse(parsed_file)
            self.code = code
            self.opened_file = parsed_file

    def get_functions(self) -> List[greetfunction.GreetFunction]:
        """
            returns an array of elements of type GreetFunction containing the information
            extracted by parsing the file if it contains elements, None otherwise
        """
        if len(self.functions) > 0:
            return self.functions
        else:
            return None
        
    def get_attributes(self) -> List[greetattribute.GreetAttribute]:
        """
            returns an array of elements of type GreetAttribute containing the information
            extracted by parsing the file if it contains elements, None otherwise
        """
        if len(self.attributes) > 0:
            return self.attributes
        else:
            return None
        
    def parse_file(self):
        self.extract_attribute()
        self.extract_function()

    def extract_attribute(self):
        """
            the function takes care of extracting the variables and their comments
            from the target file of the class by calling the private function __extract()
        """
        if self.code:
            self.__extract(self.code)

    def __extract(self, code):
        """
            through the use of the ast class for parsing the syntactic tree,
            the function takes care of extracting the variables from the target file with the respective comments,
            i.e. those found above the variable and which are documentation comments, i.e. multiline.

            The analysis is carried out recursively, when the function is inside a node of the tree that can have children, therefore a function or a class,
            we take the list of children of the node, if we find a node corresponding to a variable we verify that its left brother,
            i.e. the node immediately before in the file, is a multiline comment, if so we create an instance of GreetAttribute containing
            the fundamental information for the analysis and insert it in the list, otherwise we go after you.
            
            When in the list of children we find a node of type Function or Class we recursively call the function to re-perform the analysis

            Args:
                code: the parent node of the subtree to be analyzed
        """
        childs = code.body 
        for index, node in enumerate(childs):
            name = ""
            if isinstance(node, ast.Assign) or (isinstance(node, ast.Expr) and isinstance(node.value, ast.Attribute)):
                if index - 1 >= 0 and isinstance(code.body[index - 1], ast.Expr) and isinstance(code.body[index - 1].value, ast.Str):
                    name, colls = self.__extract_name(node)
                    start_line = code.body[index - 1].lineno
                    attribute = greetattribute.GreetAttribute(
                        identifier= name,
                        startLine= start_line,
                        endLine= node.lineno,
                        startColumn= self.__get_comment_first_col(start_line),
                        endColumn= node.col_offset + len(name) + colls,
                        string= "",
                        value= self.__extract_assign_value(node),
                        comment= ast.literal_eval(code.body[index - 1].value)
                    )
                    self.attributes.append(attribute)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                self.__extract(node)

    def __extract_assign_value(self, node):
        value = ""
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Str):
                expr = ast.Expr(node.value)
                ast.fix_missing_locations(expr)
                value = '"' + str(ast.literal_eval(expr.value)) +'"'
            elif isinstance(node.value, ast.Num):
                expr = ast.Expr(node.value)
                ast.fix_missing_locations(expr)
                value = ast.literal_eval(expr.value)
            elif isinstance(node.value, ast.Name):
                value = node.value.id
            elif isinstance(node.value, ast.Call):
                value = self.__extract_call(node.value)
            elif isinstance(node.value, ast.List):
                value = self.__extract_data_structures(node.value.elts, Structures.LIST)
            elif isinstance(node.value, ast.Set):
                value = self.__extract_data_structures(node.value.elts, Structures.SET)
            elif isinstance(node.value, ast.Tuple):
                value = self.__extract_data_structures(node.value.elts, Structures.TUPLE)
            elif isinstance(node.value, ast.Dict):
                value = self.__extract_dictionary(node.value)
        
            return value
        else:
            return None

    def __extract_call(self, node):
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Call):
            func_name = self.__extract_call(node.func)
        else:
            func_name = node.func.id
        args = ""
        args_with_key = ""


        for i, arg in enumerate(node.args):
            if isinstance(arg, ast.Str):
                expr = ast.Expr(arg)
                ast.fix_missing_locations(expr)
                args += '"' + str(ast.literal_eval(expr.value)) +'"'
            elif isinstance(arg, ast.Num):
                expr = ast.Expr(arg)
                ast.fix_missing_locations(expr)
                args += str(ast.literal_eval(expr.value))
            if isinstance(arg, ast.Name):
                args += arg.id
            elif isinstance(arg, ast.Call):
                args += self.__extract_call(arg)
            elif isinstance(arg, ast.List):
                args += self.__extract_data_structures(arg.elts, Structures.LIST)
            elif isinstance(arg, ast.Set):
                args += self.__extract_data_structures(arg.elts, Structures.SET)
            elif isinstance(arg, ast.Tuple):
                args += self.__extract_data_structures(arg.elts, Structures.TUPLE)
            elif isinstance(arg, ast.Dict):
                value = self.__extract_dictionary(arg)

            if i != len(node.args) - 1:
                args += ", "


        for i, keyword in enumerate(node.keywords):
            value = ""

            if isinstance(keyword.value, ast.Str):
                expr = ast.Expr(keyword.value)
                ast.fix_missing_locations(expr)
                value += '"' + str(ast.literal_eval(expr.value)) +'"'
            elif isinstance(keyword.value, ast.Num):
                expr = ast.Expr(keyword.value)
                ast.fix_missing_locations(expr)
                value += str(ast.literal_eval(expr.value))
            if isinstance(keyword.value, ast.Name):
                value += keyword.value.id
            elif isinstance(keyword.value, ast.Call):
                value += self.__extract_call(keyword.value)
            elif isinstance(keyword.value, ast.List):
                value += self.__extract_data_structures(keyword.value.elts, Structures.LIST)
            elif isinstance(keyword.value, ast.Set):
                value += self.__extract_data_structures(keyword.value.elts, Structures.SET)
            elif isinstance(keyword.value, ast.Tuple):
                value += self.__extract_data_structures(keyword.value.elts, Structures.TUPLE)
            elif isinstance(keyword.value, ast.Dict):
                value = self.__extract_dictionary(keyword.value)

            args_with_key += str(keyword.arg) + "=" + str(value)
            
            if i != len(node.keywords) - 1:
                args_with_key += ", "
        
        call = func_name + "("
        if args != "":
            call += args

        if args_with_key != "":
            call += ", " + args_with_key
        
        call += ")"

        return call
    
    def __extract_data_structures(self, structure, type):

        res = ""
        if type == Structures.LIST:
            res += self.DATA_STRUCTURES_COLSURES["list_start"]
        elif type == Structures.SET:
            res += self.DATA_STRUCTURES_COLSURES["graph_start"]
        elif type == Structures.TUPLE:
            res += self.DATA_STRUCTURES_COLSURES["tuple_start"]
        
        for i, item in  enumerate(structure):
            if isinstance(item, ast.Str):
                expr = ast.Expr(item)
                ast.fix_missing_locations(expr)
                res += '"' + str(ast.literal_eval(expr.value)) +'"'
            elif isinstance(item, ast.Num):
                expr = ast.Expr(item)
                ast.fix_missing_locations(expr)
                res += str(ast.literal_eval(expr.value))
            elif isinstance(item, ast.Name):
                res += item.id
            elif isinstance(item, ast.Call):
                res += self.__extract_call(item)
            elif isinstance(item, ast.List):
                res += self.__extract_data_structures(item.elts, Structures.LIST)
            elif isinstance(item, ast.Set):
                res += self.__extract_data_structures(item.elts, Structures.SET)
            elif isinstance(item, ast.Tuple):
                res += self.__extract_data_structures(item.elts, Structures.TUPLE)
            elif isinstance(item, ast.Dict):
                value = self.__extract_dictionary(item)

            if i != len(structure) - 1:
                res += ", "

        if type == Structures.LIST:
            res += self.DATA_STRUCTURES_COLSURES["list_end"]
        elif type == Structures.SET:
            res += self.DATA_STRUCTURES_COLSURES["graph_end"]
        elif type == Structures.TUPLE:
            res += self.DATA_STRUCTURES_COLSURES["tuple_end"]

        return res
            


    def __extract_dictionary(self, dict):
        dictionary = self.DATA_STRUCTURES_COLSURES["graph_start"]
        for i, item in enumerate(dict.values):
            value = ""
            if isinstance(item, ast.Str):
                expr = ast.Expr(item)
                ast.fix_missing_locations(expr)
                value = '"' + str(ast.literal_eval(expr.value)) +'"'
            elif isinstance(item, ast.Num):
                expr = ast.Expr(item)
                ast.fix_missing_locations(expr)
                value = str(ast.literal_eval(expr.value))
            elif isinstance(item, ast.Name):
                value = item.id
            elif isinstance(item, ast.Call):
                value = self.__extract_call(item)
            elif isinstance(item, ast.List):
                value = self.__extract_data_structures(item.elts, Structures.LIST)
            elif isinstance(item, ast.Set):
                value = self.__extract_data_structures(item.elts, Structures.SET)
            elif isinstance(item, ast.Tuple):
                value = self.__extract_data_structures(item.elts, Structures.TUPLE)
            elif isinstance(item, ast.Dict):
                value = self.__extract_dictionary(item)
            
            dictionary += ast.literal_eval(dict.keys[i]) + ": " + value

            if i != len(dict.values) - 1:
                dictionary += ", "
        
        dictionary += self.DATA_STRUCTURES_COLSURES["graph_end"]

        return dictionary


    def __extract_name(self, node):
        name = ""
        colls = 0
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Attribute):
                name = node.targets[0].attr
                colls = 5
            elif isinstance(node.targets[0], ast.Tuple):
                name = self.__extract_data_structures(node.targets[0].elts, Structures.TUPLE)
            elif isinstance(node.targets[0], ast.List):
                name = self.__extract_data_structures(node.targets[0].elts, Structures.LIST)
            else: 
                name = node.targets[0].id
        elif (isinstance(node, ast.Expr) and isinstance(node.value, ast.Attribute)):
            name = str(node.value.attr)
            colls = 5
        
        return name, colls
            

        

    def extract_function(self):
        if self.code:
            for index, node in enumerate(ast.walk(self.code)):
                if isinstance(node, ast.FunctionDef):
                    args = []
                    for arg in node.args.args:
                        args.append(arg.arg)
                    if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                        function = greetfunction.GreetFunction(
                            identifier= node.name,
                            startLine= node.lineno,
                            endLine= node.body[0].end_lineno,
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

