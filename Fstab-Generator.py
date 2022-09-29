# Linux-Utils: Python script for parsing YMAL file to configure and generate fstab file.
#
# Author: Mohammad Shumon <shifat18@gmail.com>
#

# To parsing YAML file and to use PyYMAL module
import yaml

# To interacting with the operating system
import os

# To access system specific parameter and functions and manipulate Python Runtime Environment.
import sys

# To run programs and scripts by spawning new processes
import subprocess

# To work with dates as date objects
import datetime

### Declaring global variables
FileSystemRecordsValues = ""
OptionKeyValue = ""
FilePath = '/etc/fstab'
LastModTime = os.path.getmtime(FilePath)
###

### Backup current fstab file with including datetime in the file name.
TimeStamp = datetime.datetime.fromtimestamp(LastModTime).strftime("%b-%d-%y-%H:%M:%S")

try:
    os.rename(FilePath, FilePath + "_" + TimeStamp)

except (OSError, PermissionError):
    print('Use sudo to execute the script')
###

### Clean fstab file for parsing the YAML file.
FstabFile = open(FilePath, 'w')
FstabFile.write('# <File System>   <Mount Point>   <File System Type>   <Mount Options>   <Dump>   <File System Pass>' + '\n')
FstabFile.close()
###

### Open and process YAML file.
with open(sys.argv[1], "r") as file:

    try:
        # Parsing YAML file safely to Python object.
        ProcessedYAMLOutput = yaml.safe_load(file)
        FstabEntries = ProcessedYAMLOutput['fstab']

        for FileSystemRecords in FstabEntries:

            for FileSystemRecordsValue in FstabEntries[FileSystemRecords]:

                # Fetching list items and options.
                if type(FstabEntries[FileSystemRecords][FileSystemRecordsValue]) == list:

                    for FileSystemOption in FstabEntries[FileSystemRecords][FileSystemRecordsValue]:
                        OptionKeyValue = OptionKeyValue + "," + FileSystemOption

                    break

                # To set root-reservation by command on disk because fstab doesn't support this.
                if 'root-reserve' in FileSystemRecordsValue:
                    Command = subprocess.run(["tune2fs", "-m10", f'{FileSystemRecords}'], stdout=subprocess.DEVNULL)
                    return_code = Command.returncode

                    if return_code == 0:
                        print(f'root-reserve on partition {FileSystemRecords} has been modify it successfully')

                    else:
                        print(f'there is some problems to set root-reserve on partition {FileSystemRecords},take look at syslog')

                    break

                # Placing the exporter address next to the file-system address.
                if 'export' in FileSystemRecordsValue:
                    FileSystemRecordsValues = FileSystemRecordsValues + ":" + str(FstabEntries[FileSystemRecords][FileSystemRecordsValue])

                else:
                    FileSystemRecordsValues = FileSystemRecordsValues + " " + str(FstabEntries[FileSystemRecords][FileSystemRecordsValue])

            if ":" in FileSystemRecordsValues:
                FstabRecord = FileSystemRecords + FileSystemRecordsValues

            else:
                FstabRecord = FileSystemRecords + " " + FileSystemRecordsValues

            if (":" in FstabRecord) and (OptionKeyValue != ""):
                FstabRecord = FstabRecord + OptionKeyValue.replace(",", " ", 1) + " 0 0"

            else:
                FstabRecord = FstabRecord + " defaults 0 0"
###

            ### Write to fstab file
            GenerateFstab = open(FilePath, 'a')
            GenerateFstab.write(FstabRecord + "\n")
            GenerateFstab.close()
            ###

            FileSystemRecordsValues = ""

    except yaml.YAMLError as exc:
        print(exc)

# For mounting fstab after finished the processes please uncomment the next line
# MountCommand = subprocess.run(["mount", "-a"])
