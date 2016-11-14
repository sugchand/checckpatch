#! /usr/bin/python3
# -*- coding: utf8 -*-
#
# **** NOT A MULTI-THREADED APPLICATION. NEVER TRY TO RUN THE MULTIPLE INSTANCE
# **** OF SCRIPT. CAN CAUSE UNPREDICTABLE ISSUES WITH MERGING.
#
# The script to download and apply patches on a given repo.
# It does the following
# 1. Download patches on local-machine at LOCAL_PATCH_DIR
# 2. Copy the patches to remote machine, into the remote repo
# 3. Apply the patch.
#
# Second use-case is to validate patches before sending to the public ML.It can
# be done as follows
# 1. Provide number of last commits to test.
# 2. Script will create the mbox, pull a new branch having latest master. Apply
# 
# Prerequisites/Assumptions 
# 1. SSH server is running on remote server.
# 2. Mutt must be available on local machine when it uses for download patches.

# *****************************************************************************#
#                    MANDATORY PARAMETERS                                      #
# *****************************************************************************#
PATCHWORK_URL = ""
MUTT_EXE = "" # Valid only for the Linux machine.
REMOTE_HOST = "" # The host where the repo is located.
REMOTE_REPO = "" # Repo
LOCAL_PATCH_DIR = "" # Local directory where the patches tobe downloaded.

# *****************************************************************************#
#                     OPTIONAL PARAMETERS                                      #
# *****************************************************************************#
# Default is master branch, New branch created when branch is nonexistent.
REMOTE_BRANCH = "master"
REMOTE_USERNAME = ""

# *****************************************************************************#
import getpass
import paramiko
import socket
import os
import platform
import argparse

def get_file_stat(path, dir_stat_dic):
    for f in os.listdir(path):
        if os.path.isdir(f):
            dir_stat_dic = get_file_stat(f, dir_stat_dic)
        else:
            dir_stat_dic[f] = os.path.getmtime(f)
    return dir_stat_dic

def get_directory_stat_local(path):
    '''
    get the statistics of directory. Each file stat stored in a dictionary
    as {
        ['file1', 'stat']
        }
    '''
    dir_stat_dic = { }
    if path is None:
        return dir_stat_dic
    get_file_stat(path, dir_stat_dic)
    return dir_stat_dic

def compare_dir_dic(old_dir_stat, new_dir_stat):
    '''
    The two dictionary of files with mtime compared each other to decide what
    new files are added or modified the existing ones.
    '''
    mod_files = []
    for filename, mtime in new_dir_stat.items():
        if filename in old_dir_stat:
            # The file present in OLD stat as well. Check the mod-time now
            if mtime == old_dir_stat[filename]:
                # Nothing to do the file is not changed.
                return mod_files
        mod_files.append(filename)
        return mod_files

def open_mutt():
    '''
    Open the mutt client for the user to download the relevant patches
    '''
    os.system('mutt')

def get_password():
    pwd = getpass.getpass()
    return pwd

def get_remote_connection(host, user_name, port = 22):
    print("login: " + user_name)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host,
                             port=port,
                             username = user_name,
                             password = get_password())
    except socket.error:
        print("Failed to connect/get remote connection to %s" % host)
    except paramiko.BadAuthenticationType:
        print("Authentication failed, user: %s" % user_name)
    return ssh

def is_remote_and_localhost_same():
    pass

def create_format_patch():
    pass

def create_merge_branch():
    pass


if __name__ == "__main__":
    if platform.system() != 'Linux':
        print("Checkpath works only on the Linux machine")
        exit(1)
    ssh = get_remote_connection(REMOTE_HOST, REMOTE_USERNAME, port = 22)
    old_dir_stat = get_directory_stat_local(LOCAL_PATCH_DIR)
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--mutt', help='Use mutt-client to get patches')
    ap.add_argument('-p', '--patchwork', help='Open patchworks in browser')
    ap.add_argument('-r', '--remote-repo', help='remote repo to apply patches')
    ap.add_argument('-d', '--local-dir', help='local dir to store patches')
