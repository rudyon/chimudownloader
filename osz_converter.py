import argparse
import os
import tempfile
import shutil
from zipfile import ZipFile

parser = argparse.ArgumentParser(
    description='Convert osz files to the McOsu format')

parser.add_argument('input', metavar='I', type=str,
                    help='Folder that has all the osx files')
parser.add_argument('output', metavar='O', type=str, help='Output folder')
parser.add_argument(
    '--delete', help='Delete the files after conversion', action='store_true')
parser.add_argument(
    '--recursive', help='Search for files inside folders', action='store_true')
parser.add_argument(
    '--overwrite', help='Overwrite the folders if has the same folder name', action='store_true')

args = parser.parse_args()

if not args.input or not os.path.isdir(args.input):
    raise Exception("Input folder does not exist or is not valid")
if not args.output or not os.path.isdir(args.output):
    raise Exception("Output folder does not exist or is not valid")


def get_files(input_folder, recursive=False):
    files = []
    if recursive:
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".osz"):
                    files.append(os.path.join(root, file))
    else:
        for file in os.listdir(input_folder):
            if file.endswith(".osz"):
                files.append(os.path.join(input_folder, file))
    return files

def copy_files_to_temp(files):
    new_files = []
    tempfolder = tempfile.mkdtemp("osz_converter")
    for f in files:
        filename = os.path.basename(f)
        temp_file_path = os.path.join(
            tempfolder, "{}.zip".format(os.path.splitext(filename)[0]))
        shutil.copyfile(f, temp_file_path)
        new_files.append(temp_file_path)
    return new_files, tempfolder


def mkdir_for_folders(output_folder, folder_names, overwrite=False):
    not_extracted_files = []
    for filename in folder_names:
        name = os.path.splitext(os.path.basename(filename))[0]
        folder_name = os.path.join(output_folder, name)
        if os.path.isdir(folder_name):
            if not overwrite:
                print("Folder \"{}\" already exists, skipping".format(name))
                not_extracted_files.append(name)
            else:
                print("Overwriting \"{}\"".format(name))
                with ZipFile(filename, 'r') as zipObj:
                    zipObj.extractall(folder_name)
        else:
            os.mkdir(folder_name)
            print("Extracting \"{}\"".format(name))
            with ZipFile(filename, 'r') as zipObj:
                zipObj.extractall(folder_name)
    return not_extracted_files


files = get_files(args.input, args.recursive)

temp_files, tempfolder = copy_files_to_temp(files)

not_extracted_files = mkdir_for_folders(
    args.output, temp_files, args.overwrite)

shutil.rmtree(tempfolder)
if args.delete:
    for filename in files:
        if not os.path.splitext(os.path.basename(filename))[0] in not_extracted_files:
            print("Removing {}".format(filename))
            os.remove(filename)

print("Conversion finished")
