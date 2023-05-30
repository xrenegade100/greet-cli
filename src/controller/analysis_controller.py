from ast import Dict
from src.model.greetentity import AbstractGreetEntity
from src.utils.parser import Parser
from src.classifier.classifier import Classifier
from typing import List
from src.manager.filemanager import FileManager

from src.model.config import Config
from src.model.greetissuetype import GreetIssueType

class AnalysisController:
	__result = {}
    
	def __init__(self, files: List[str], classifier: Classifier, config: Config, fileManager: FileManager):
		self.__classifier = classifier
		self.__config = config
		self.__files = files
		self.__fm = fileManager

	def run(self):
		output = []
		for f in self.__files:    
			print('\n\n: ===== file %s : =====' % f)
			p = Parser(self.__fm.readInputFile(f))
			try:
				p.parse_file()
			except RuntimeError:
				continue

			total_issues = {
				GreetIssueType.CLEAR: 0,
				GreetIssueType.ATTRIBUTE_OPPOSITE_COMMENT: 0,
				GreetIssueType.METHOD_OPPOSITE_COMMENT: 0,
				GreetIssueType.NOT_IMPL_CONDITION: 0
			}

			functions = p.get_functions() or []
			attributes = p.get_attributes() or []
			entities: List[AbstractGreetEntity] = [*functions, *attributes]
			for entity in entities:
				entity.setIssue(GreetIssueType(self.__classifier.predict(entity)))
				total_issues[entity.getIssue()] += 1
				if entity.getIssue() == GreetIssueType.CLEAR and not self.__config.getIncludeClear():
					continue
				if self.__config.getOutputPath() is not None:
					if entity.getIssue() == GreetIssueType.CLEAR and not self.__config.getIncludeClear():
						continue
					output.append({'file': f, 'identifier': entity.getIdentifier(), 'issue': entity.getIssue()._name_, 'line': entity.getStartLine()})
				print(f""":`{entity.getIdentifier()}`: {self.getReadableIssueName(GreetIssueType(entity.getIssue()))}: line {entity.getStartLine()}""")
			self.__save_file_result(f, total_issues)
		if self.__config.getOutputPath() is not None:
			self.__fm.saveToOutputPath(output)
		self.__print_all_results(self.__config.getIncludeClear())
		return

	def getReadableIssueName(self, type: GreetIssueType):
		if type == GreetIssueType.CLEAR:
			return "clear"
		return f'\033[91m{type._name_.replace("_", " ").lower()}\033[0m'


	def __save_file_result(self, file: str, result: Dict):
		self.__result[file] = result

	def __print_all_results(self, include_clear: bool = False):
		print("""\n\n: ==== TOTAL RESULTS ====\n""")
		if include_clear:
			for file, result in self.__result.items():
				print(f": file {file}")
				print("MOP\tAOP\tCLEAR\tNIC")
				print(f'{result.get(GreetIssueType.METHOD_OPPOSITE_COMMENT, 0)}\t{result.get(GreetIssueType.ATTRIBUTE_OPPOSITE_COMMENT, 0)}\t{result.get(GreetIssueType.CLEAR, 0)}\t{result.get(GreetIssueType.NOT_IMPL_CONDITION, 0)}')
		else:
			for file, result in self.__result.items():
				print(f": file {file}")
				print("MOP\tAOP\tNIC")
				print(f'{result.get(GreetIssueType.METHOD_OPPOSITE_COMMENT, 0)}\t{result.get(GreetIssueType.ATTRIBUTE_OPPOSITE_COMMENT, 0)}\t{result.get(GreetIssueType.NOT_IMPL_CONDITION, 0)}')
		