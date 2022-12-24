"""Minimal ansible playbook runner

This script permits the user to invoke an ansible playbook via python
and encapsulates the return values from ansible and interrogates for
failures and purposely raises an Runtime errors on failures.

This is used so that when invoked from a .sh file via code deploy 
if ansible has a failure the code deploy should fail as well.

this supports two command line arguments
 * -d --PrivateDataDir (private data dir for ansible runner)
 * -p --Playbook (fully qualified path to playbook)

this should be invoked w/in .sh file using
python3 minimal_ansible_playbook.py -p full/path/to/my/playbook.yaml -d /full_path_to_ansible_private_dir

or relative paths appear to work as well (site.yaml and private data dir at top level)
python3 minimal_ansible_playbook.py -p ./site.yaml -d ./
"""

import argparse
from ansible_runner import Runner, RunnerConfig

def run_playbook(p_args):
    priv_data_dir = p_args.PrivateDataDir
    playbook_to_run = p_args.Playbook

    # Create runner config from input parms
    print("Creating RunnerConfig")
    rc = RunnerConfig(
        private_data_dir=priv_data_dir,
        playbook=playbook_to_run
    )

    rc.prepare()
    r = Runner(config=rc)
    print("Invoking Runner To Run Playbook")
    r.run()
    print("Return Status: {} with RC: {}".format(r.status, r.rc))
    print("Return Stats: {}".format(r.stats))
    if r.stats is None:
        print("FATAL ERROR WITH Runner!")
        raise RuntimeError('Ansible Runner crashed! Check log for errors.') 
    
    failed_dict = r.stats['failures']
    if len(failed_dict) != 0:
        print("FAILURES FOUND!")
        raise RuntimeError('Ansible Playbook failed! Check log for errors.') 
    else:
        print("Invoke Playbook - SUCCESSFUL")

if __name__ == '__main__':
    print("main - invoking playbook")   
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Playbook", help = "Playbook name")
    parser.add_argument("-d", "--PrivateDataDir", help = "PrivateDataDir")
    p_args = parser.parse_args()
    print("Ansible Invoked with args: {}".format(p_args))
    stats = run_playbook(p_args)
