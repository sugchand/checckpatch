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
# 2. Mutt must be available on local machine when it is used for download patches.


# *****************************************************************************#
#                    MANDATORY PARAMETERS                                      #
# *****************************************************************************#
ENV_PARAMS = {
              'PATCHWORK_URL' : "https://patchwork.ozlabs.org/project/openvswitch/list/",
              'MUTT_EXE' : "mutt", # Valid only for the Linux machine.
              'REMOTE_HOST' : "", # The host where the repo is located.
              'REMOTE_REPO' : "", # Repo
              'LOCAL_PATCH_DIR' : "/tmp/", # Local directory where the patches tobe downloaded.
              'REMOTE_USERNAME' : "sugesh",

# *****************************************************************************#
#                     OPTIONAL PARAMETERS                                      #
# *****************************************************************************#
                # Default is master branch, New branch created when branch is nonexistent.
                'REMOTE_BRANCH' : "master",
                }

# *****************************************************************************#
import getpass
import paramiko
import socket
import os
import platform
import argparse
import webbrowser

REMOTE_PATCH_DIR = ".mbox_patches"
def get_file_stat(path, dir_stat_dic):
    for f in os.listdir(path):
        f = os.path.abspath(os.path.join(path,f))
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
    if not os.path.exists(path):
        os.mkdir(path)
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
    print("*******************************************************************")
    print("USE %s DIRECTORY TO SAVE THE PATCHES" % ENV_PARAMS['LOCAL_PATCH_DIR'])
    print("*******************************************************************")
    '''
    Open the mutt client for the user to download the relevant patches
    '''
    os.system('mutt')

def open_patchwork():
    print(ENV_PARAMS)
    print("*******************************************************************")
    print("USE %s DIRECTORY TO SAVE THE PATCHES" % ENV_PARAMS['LOCAL_PATCH_DIR'])
    print("*******************************************************************")
    try:
        return webbrowser.open_new_tab(ENV_PARAMS['PATCHWORK_URL'])
    except:
        print("Failed to open the webbrowser, Exiting..")
        return False

def get_password():
    pwd = getpass.getpass()
    return pwd

def get_remote_connection(host, user_name, port = 22):
    if not host or not user_name:
        print("Invalid User Name or Password")
        return None
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

def remote_copy_files(ssh, remote_repo, patches):
    remote_patch_dir = os.path.join(remote_repo, REMOTE_PATCH_DIR)
    sftp = ssh.open_sftp()
    if not os.path.exists(remote_patch_dir):
        sftp.mkdir(remote_patch_dir)
    for f in patches:
        sftp.put(f, remote_patch_dir)

def create_format_patch():
    pass

def create_merge_branch():
    pass

def cmdline_arg_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--mutt',
                    dest = 'MUTT_EXE',
                    action="store_const",
                    const = ENV_PARAMS['MUTT_EXE'],
                    help='Use mutt-client to get patches')
    ap.add_argument('-p', '--patchwork',
                    dest = 'PATCHWORK_URL',
                    action = 'store_const',
                    const = ENV_PARAMS['PATCHWORK_URL'],
                    metavar = 'PATCHWORK-URL',
                    help='Open patchworks in browser')
    ap.add_argument('-purl', '--patchwork-url',
                    dest = 'PATCHWORK_URL',
                    metavar = 'PATCHWORK-URL',
                    default = ENV_PARAMS['PATCHWORK_URL'],
                    help = 'Patchwork URL to open in browser(Optional)')
    ap.add_argument('-r', '--remote-repo',
                    metavar = 'REMOTE-REPO',
                    dest = 'REMOTE_REPO',
                    default = ENV_PARAMS['REMOTE_REPO'],
                    help='remote repo to apply patches')
    ap.add_argument('-d', '--local-dir',
                    metavar = 'LOCAL-DIR',
                    dest = 'LOCAL_PATCH_DIR',
                    default = ENV_PARAMS['LOCAL_PATCH_DIR'],
                    help='local dir to store patches')
    ap.add_argument('-s', '--server',
                    metavar = 'REMOTE-HOST',
                    dest = 'REMOTE_HOST',
                    default = ENV_PARAMS['REMOTE_HOST'],
                    help = 'Remote host to connect')
    ap.add_argument('-b', '--branch',
                    metavar = 'REMOTE-BRANCH',
                    dest = 'REMOTE_BRANCH',
                    default = ENV_PARAMS['REMOTE_BRANCH'],
                    help = 'Remote branch to apply the patch')
    ap.add_argument('-u', '--username',
                    metavar = 'REMOTE-USERNAME',
                    dest = 'REMOTE_USERNAME',
                    default = ENV_PARAMS['REMOTE_USERNAME'],
                    help = 'Log-in Name for the server')
    args = ap.parse_args()
    return args

class linux_checkpatch():
    def __init__(self):
        pass

    def open_user_mbox_app(self):
        global ENV_PARAMS
        if ENV_PARAMS['MUTT_EXE']:
            open_mutt()
        elif ENV_PARAMS['PATCHWORK_URL']:
            open_patchwork()

    def set_env_params(self, args):
        global ENV_PARAMS
    # Is it Mutt/patchwork to generate the patch??
        if not args.MUTT_EXE and not args.PATCHWORK_URL:
            print("Please select either mutt/patchwork by -m or -p")
            return
        if args.MUTT_EXE and args.PATCHWORK_URL:
            print("Cannot use mutt and patchwork together, Exiting...")
            return
        ENV_PARAMS = vars(args)
        if args.MUTT_EXE:
            ENV_PARAMS['PATCHWORK_URL'] = None
        elif args.PATCHWORK_URL:
            ENV_PARAMS['MUTT_EXE'] = None

    def run_apply_patch(self, args):
        self.set_env_params(args)
        # Snapshot the stat of directory for reference.
        old_stat_dic = get_directory_stat_local(ENV_PARAMS['LOCAL_PATCH_DIR'])
        self.open_user_mbox_app()
        new_stat_dic = get_directory_stat_local(ENV_PARAMS['LOCAL_PATCH_DIR'])
        print(new_stat_dic)
        diff_file_list = compare_dir_dic(old_stat_dic, new_dir_stat=new_stat_dic)
        print(diff_file_list)

class windows_checkpatch():
    def __init__(self):
        pass

    def set_env_params(self, args):
    # Is it Mutt/patchwork to generate the patch??
        if not args.PATCHWORK_URL:
            print("Please select patchwork using option -p")
            return
        if args.MUTT_EXE and args.PATCHWORK_URL:
            print("Cannot use mutt and patchwork together, Exiting...")
            return

if __name__ == "__main__":
    args = cmdline_arg_parse()
    if platform.system() == 'Linux':
        sys_obj = linux_checkpatch();
        sys_obj.run_apply_patch(args)
