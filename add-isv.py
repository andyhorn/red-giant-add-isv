from __future__ import print_function
import argparse
import zipfile
import os
import fileinput
import tempfile
import shutil

# The line in the .lic file to search for and to add the ISV port value to
ISV_LINE = "ISV redgiant"

PARSER = argparse.ArgumentParser()


# Get the command-line arguments
def get_args():
    # Set up the argument parser
    # PARSER = argparse.ArgumentParser()
    # Add an optional flag for a different output directory
    PARSER.add_argument("-o",
                        "--out",
                        help="specify a different output path for the modified file(s); default will overwrite - "
                             "must be a directory if -d is set, else must use a full filename",
                        action="store",
                        dest="out",
                        required=False,
                        default=None)
    PARSER.add_argument("-d",
                        "--dir",
                        help="modify a directory of files; default is a single file",
                        action="store_const",
                        const=True,
                        dest="dir",
                        required=False,
                        default=False)
    # Add a group for the required arguments: [Directory or File] and Port
    required_group = PARSER.add_argument_group("Required arguments")

    file_group = required_group.add_mutually_exclusive_group(required=True)
    file_group.add_argument("-l",
                            "--lic",
                            help="directly modify .lic files",
                            action="store_const",
                            const="lic",
                            dest="type")
    file_group.add_argument("-z",
                            "--zip",
                            help="modify .lic files within .zip files",
                            action="store_const",
                            const="zip",
                            dest="type")

    required_group.add_argument("-p",
                                "--port",
                                help="the isv port to add to each file",
                                action="store",
                                required=True)
    required_group.add_argument("path",
                                nargs=1,
                                help="the path to the file or directory (if specified) to be modified",
                                action="store")
    # Return the parsed arguments
    return PARSER.parse_args()


# Collect the desired files in the given directory
def get_files(endswith):
    if ARGS.dir:
        # Get the full file-path for the given directory
        file_path = os.path.realpath(ARGS.path)
        # Get a list of files in that directory
        all_files = os.listdir(file_path)
        print("locating %s files in %s" % (endswith, file_path))
        # Filter the files for the desired file type
        wanted_files = filter(lambda x: x.endswith(endswith), all_files)
        return wanted_files
    elif ARGS.path is not None:
        files = [ARGS.path]
        return files
    return None


# Process a license file, adding the ISV port value to the line
def process_single_file(file):
    print("Processing file %s" % file)
    added = False # Set the flag
    # Loop through the lines of the license file
    for line in fileinput.input(file, inplace=True):
        if line == ISV_LINE + "\n" or line == ISV_LINE + " \n":
            added = True # Trigger the flag
            line = "ISV redgiant port=%s\n" % ARGS.port # Add the port number
        print(line, end="") # Print the line (write in the file)
    if added:
        # If the line was added, print a message
        print("ISV %s was added to file '%s'" % (ARGS.port, file))


# Process a list of .zip files
def process_zip_files():
    print("Processing .zip files...")
    # Get a list of .zip files in the given directory
    zip_files = get_files(".zip")
    tempdir = tempfile.mkdtemp() # Make a temporary folder
    try:
        # Loop through the list of .zip files
        for zip_file in zip_files:
            zip_path = os.path.join(ARGS.dir, zip_file) if ARGS.dir is not False else zip_file[0]
            print(zip_path)
            tmp_zip = os.path.join(tempdir, "tmp.zip") # Make a .zip file in the temp directory
            print("Processing file %s" % zip_file)
            # Open the .zip file and the temporary .zip file
            with zipfile.ZipFile(tmp_zip, mode="w") as new_zip:
                with zipfile.ZipFile(zip_path, mode="r") as old_zip:
                    for item in old_zip.filelist:
                        # Search for license files in the "server" folder
                        # If this license file is not a server license file, simply copy the data
                        if "server" not in item.filename or ".lic" not in item.filename:
                            data = old_zip.read(item.filename)  # Extract the data from the .lic file
                            new_zip.writestr(item, data)        # Write the data to the new (temp) .zip file
                        else:
                            # Otherwise, copy the data to a new file, process that file, then add the file to
                            # the new .zip archive
                            print("Found server license: %s" % item.filename)
                            print("Extracting to temp location")
                            # Extract the data to a temporary file
                            tmp_file = old_zip.extract(item, path=tempdir)
                            # Process the temporary file and add the ISV port value
                            process_single_file(tmp_file)
                            print("Writing back to .zip archive")
                            # Open the temporary file
                            with open(tmp_file, "r") as file:
                                data = file.read()              # Read the file data
                                new_zip.writestr(item, data)    # Write the data to the new (temp) .zip file
            if ARGS.out is not None:
                new_path = os.path.join(ARGS.out, zip_file) if ARGS.dir else ARGS.out
                shutil.move(tmp_zip, new_path)
            else:
                shutil.move(tmp_zip, zip_path) # Move the temporary zip file over the top of the existing file
    finally:
        print("Removing temp directory")
        shutil.rmtree(tempdir) # Remove the temporary directory
        print("Processing complete!")


# Process the .lic files in the given directory
def process_local_files():
    print("Processing .lic files...")
    lic_files = get_files(".lic")   # Get the .lic files in the chosen directory
    for lic in lic_files:
        if ARGS.out is not None:
            # filename = os.path.basename(lic)
            new_file = os.path.join(ARGS.out, os.path.basename(lic)) if ARGS.dir else ARGS.out
            shutil.copy(lic, new_file)
            process_single_file(new_file)
        else:
            process_single_file(lic)    # Process each file, adding the ISV port value when necessary
    print("Complete!")


# Get the command-line arguments
ARGS = get_args()

# validate the output parameter
if ARGS.out is not None:
    if ARGS.dir:
        # check that the output path is a directory
        if not os.path.isdir(ARGS.out):
            PARSER.error("Output path is not a valid directory; Must be a directory when using -d flag")
    else:
        # check that the output path is a valid filename
        if not ARGS.out.endswith(".lic") or not ARGS.out.endswith(".zip"):
            PARSER.error("Must use a valid output filename ending in .lic or .zip")
        # check that the output directory exists
        dir = os.path.dirname(ARGS.out)
        if not os.path.exists(dir):
            PARSER.error("Output directory must exist")

if ARGS.type == "lic":
    # process .lic files
    process_local_files()

elif ARGS.type == "zip":
    # process .zip files
    process_zip_files()