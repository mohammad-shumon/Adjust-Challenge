# Adjust-Challenge

A small Python script to write and generate /etc/fstab file by parsing a YAML file containing varity of fstab configs and entries on Linux system.

NOTE: Make sure all entry points are included in YAML file for writing and generating the fstab file from scrach.



## Prerequisite 

- Installed Python3 on your system.
- Installed package installer for python, AKA pip on your system.
- Install dependencies.
- Execute the script with sudo.
- Execute **tune2fs** command to enable ext4 feature on disk partition for Root-Reserve option.



## Usage 

To backup fstab file if something goes wrong
- Run `cp /etc/fstab /etc/fstab.backup`

To copy the resources from git
- Run `git_clone https://github.com/mohammad-shumon/Adjust-Challenge.git`

To install dependencies
- Run `pip install -r requirements.txt`

To execute the Python script and parse the YAML file
- Run `python3 Fstab-Generator.py Adjust-Challenge.yml`

Check out the /etc/fstab file and if everything is right use `mount -a`. Else restore from the backup.
