#! /usr/bin/python3
# -*- coding: utf8 -*-
#
# The patch apply script to download and apply patches cleanly on a repo. 
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

# *****************************************************************************#

def get_directory_stat():
    pass

def get_remote_connection():
    pass

def is_remote_and_losthost_same():
    pass

def create_format_patch():
    pass

def create_merge_branch():
    pass