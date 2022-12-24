#!/bin/bash

# invoke python wrapper with Playbook path, and private data dir location
python3 minimal_ansible_playbook.py -p ./site.yaml -d ./

# invoke python wrapper with fully qualified path, and private data dir
# python3 minimal_ansible_playbook.py -p /Users/timothyjanusz/source/dev_ops/ansibleplaybookrunner/project/site.yaml -d /tmp
