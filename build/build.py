from argparse import ArgumentParser
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join

parser = ArgumentParser()
parser.add_argument('-p', '--platform', required=True, choices=['linux', 'win'])

args = parser.parse_args()

# CONFIG
PLATFORM = 'linux' if args.platform == 'linux' else 'win'
VERSION = "0.0.1-alpha.1"
OUT_FILE_NAME = f"greet-cli-{PLATFORM}-{VERSION}.zip"

def add_files_to_archive_LINUX(directory, archive):
    for file_name in listdir(directory):
        if file_name == '__pycache__':
            continue
        file_path = join(directory, file_name)
        if isfile(file_path):
            if file_path.startswith('./build/'):
                archive.write(file_path, f'./runtime/{file_path[21:]}')
            else:
                archive.write(file_path)
        else:
            add_files_to_archive_LINUX(file_path, archive)

def add_files_to_archive_WIN(directory, archive):
    for file_name in listdir(directory):
        if file_name == '__pycache__':
            continue
        file_path = join(directory, file_name)
        if isfile(file_path):
            if file_path.startswith('./build/'):
                archive.write(file_path, f'./runtime/{file_path[19:]}')
            else:
                archive.write(file_path)
        else:
            add_files_to_archive_WIN(file_path, archive)


def package_linux():
    archive = ZipFile(f'{OUT_FILE_NAME}', 'w')

    archive.write('./build/resources/greet.sh', 'greet.sh')

    # Aggiunta ricorsiva dei file e delle cartelle nella cartella "./src"
    add_files_to_archive_LINUX('./src', archive)
    add_files_to_archive_LINUX('./build/runtime/linux/lib/python3.10/site-packages/pip', archive)

    archive.write('./build/runtime/linux/bin/python', './runtime/bin/python')
    archive.write('./build/runtime/linux/bin/pip', './runtime/bin/pip')

    archive.write('./build/runtime/linux/pyvenv.cfg', './runtime/pyvenv.cfg')
    archive.write('requirements.txt')
    archive.close()

def package_win():
    archive = ZipFile(f'{OUT_FILE_NAME}', 'w')

    archive.write('./build/resources/greet.cmd', 'greet.cmd')

    # Aggiunta ricorsiva dei file e delle cartelle nella cartella "./src"
    add_files_to_archive_WIN('./src', archive)
    add_files_to_archive_WIN('./build/runtime/win/lib/python3.10/site-packages/pip', archive)
    add_files_to_archive_WIN('./build/runtime/win/Scripts/', archive)

    archive.write('./build/runtime/win/bin/python.exe', './runtime/bin/python.exe')
    archive.write('./build/runtime/win/bin/pip', './runtime/bin/pip')
    archive.write('./build/runtime/win/bin/python3.dll', './runtime/bin/python3..exe')
    archive.write('./build/runtime/win/bin/python310.dll', './runtime/bin/python310.dll')
    archive.write('./build/runtime/win/bin/vcruntime140.dll', './runtime/bin/vcruntime140.dll')
    archive.write('./build/runtime/win/bin/vcruntime140_1.dll', './runtime/bin/vcruntime140_1.dll')
    
    archive.write('./build/runtime/win/pyvenv.cfg', './runtime/pyvenv.cfg')
    archive.write('requirements.txt')
    archive.close()

if args.platform == 'linux':
    package_linux()
elif args.platform == 'win':
    package_win()
