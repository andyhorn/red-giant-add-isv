import argparse
import zipfile
import os
import fileinput
import tempfile
import shutil


def get_args():
    # Set up the argument parser
    parser = argparse.ArgumentParser()
    file_group = parser.add_mutually_exclusive_group()
    file_group.add_argument("-l", "--lic", help="directly modify .lic files", action="store_const", const="lic", dest="type")
    file_group.add_argument("-z", "--zip", help="modify .lic files within .zip files", action="store_const", const="zip", dest="type")
    required_group = parser.add_argument_group("Required arguments")
    required_group.add_argument("-d", "--dir", help="the directory containing the licenses", action="store", dest="dir", required=True)
    required_group.add_argument("-p", "--port", help="the isv port to add to each file", action="store", required=True)
    return parser.parse_args()


def get_files(endswith):
    file_path = os.path.realpath(ARGS.dir)
    all_files = os.listdir(file_path)
    print("locating %s files in %s" % (endswith, file_path))
    wanted_files = []
    for file in all_files:
        if file.endswith(endswith):
            wanted_files.append(os.path.join(file_path, file))
    return wanted_files


def process_single_file(file):
    print("Processing file %s" % file)
    for line in fileinput.input(file, inplace=True):
        if "ISV redgiant" in line:
            print("Adding port number %s to redgiant ISV" % ARGS.port)
            line = "ISV redgiant port=%s\n" % ARGS.port
        print(line, end="")


def process_zip_files():
    print("Processing .zip files...")
    zip_files = get_files(".zip")
    tempdir = tempfile.mkdtemp()
    try:
        for zip_file in zip_files:
            tmp_zip = os.path.join(tempdir, "tmp.zip")
            print("Processing file %s" % zip_file)
            with zipfile.ZipFile(tmp_zip, mode="w") as new_zip:
                with zipfile.ZipFile(zip_file, mode="r") as old_zip:
                    for item in old_zip.filelist:
                        if "server" not in item.filename or ".lic" not in item.filename:
                            data = old_zip.read(item.filename)
                            new_zip.writestr(item, data)
                        else:
                            print("Found server license: %s" % item.filename)
                            print("Extracting to temp location")
                            tmp_file = old_zip.extract(item, path=tempdir)
                            process_single_file(tmp_file)
                            print("Writing back to .zip archive")
                            with open(tmp_file, "r") as file:
                                data = file.read()
                                new_zip.writestr(item, data)
            shutil.move(tmp_zip, zip_file)
    finally:
        print("Removing temp directory")
        shutil.rmtree(tempdir)
        print("Processing complete!")


def process_local_files():
    print("Processing unzipped files...")
    lic_files = get_files(".lic")
    for lic in lic_files:
        process_single_file(lic)
    print("Complete!")


ARGS = get_args()

if ARGS.type == "zip":
    process_zip_files()
else:
    process_local_files()
