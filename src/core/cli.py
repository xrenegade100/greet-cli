import warnings
from http.server import HTTPServer
from argparse import ArgumentParser
from src.manager.filemanager import FileManager
from src.model.config import ConfigBuilder
from src.model.greetissuetype import GreetIssueType
from src.classifier.classifier import greetClassifier
from src.http.server import Server
from src.utils.parser import Parser
from src.controller.analysis_controller import AnalysisController
from typing import Dict

warnings.filterwarnings("ignore")

__HTTP_HOSTNAME = 'localhost'
__HTTP_PORT = 19201

__argparser = ArgumentParser()
__argparser.add_argument('-i', '--input', help='The input path.')
__argparser.add_argument('-o', '--output', help='The output path.')
__argparser.add_argument(
            '-c',
            '--include-clear', 
            nargs='?',
            default=False,
            const=True,
            help='Whether to include analyzed entities with no issues detected in the results.'
)
__argparser.add_argument('-s', '--server', help='Whether to run the server.', nargs='?', const=True, default=False)

__args = __argparser.parse_args()

__config = (ConfigBuilder()
            .withInput(__args.input)
            .withOutputPath(__args.output)
            .withIncludeClear(__args.include_clear)
            .build())

__fm = FileManager(__config)



classifier = greetClassifier

def run():
  if __args.server and __name__ == '__main__':
    httpd = HTTPServer((__HTTP_HOSTNAME, __HTTP_PORT), Server)
    print(f'running server on port: {__HTTP_PORT}')
    httpd.serve_forever()
  else:
    __fm.loadInputFiles()
    files = __fm.getInputFiles()
    analysisController = AnalysisController(files, classifier, __config, __fm)

    analysisController.run()
  return




run()