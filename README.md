# Ansible playbook runner

Attempt at having a python script run playbook for automation. 

Currently when our AWS code deploy application hooks run and invoke ansible playbooks any
any result info is not captured and more importantly any failures in the ansible playbook are
not reported back to the code hook (e.g. ansible failure should cause event hook to fail)
AWS code deploy hook info [is found here](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html#appspec-hooks-server)

This simple project simulates how to invoke ansible playbooks via a bash script
which can return ansible playbook results info and more importantly return a non zero return code to the 
bash script to ensure that code deploy fails the hook on playbook failure.

## Tools Utilized
The project utilizes
* **Python3** - Python module to invoke ansible
* **bash.sh** - Bash .sh file simulating the applicationHook script file
* **Ansible runner** - [Ansbile runner module](https://ansible-runner.readthedocs.io/en/stable/python_interface/#)
* **Ansbile** - [Ansible automation](https://docs.ansible.com/ansible/2.9/index.html)

## Project Structure
The project utilizes this structure

```
├── env                     (ansible runner configuration info)
|   settings
├── project                 (ansible top level project folder)
|     ├── group_vars
|           all.yaml
|     ├── roles             (ansible roles)
|       ├── sample1         (sample1 ansible role)
|           ├── defaults
|           ├── tasks
|               main.yaml
|       ├── sample2         (sample2 ansible role)
|           ├── defaults
|           ├── tasks
|               main.yaml
|     ├── site.yaml     (sample playbook invoked)
├── applicationStart.sh    (example code deploy app hook file)
├── minimal_ansible_playbook.py    (python script encapsulating ansible invocation logic)
```



## Python Setup
The project assumes python 3.9. It is unclear if this project works with older 2.x versions of python. Our current requirement is for
rhel8.x which provides python3.8 OOTB. I only used 3.9 since I already had this installed on my machine.

Additionally this assumes using venv for virtual environments with all requirements installed w/in the virtual environment.

```bash
# install python 3.9
brew install python@3.9

# verify version is install
python3 --version

# location
which python3
# /opt/homebrew/bin/python3

### create venv to install packages
# Create directory for venvs (don't do it inside this directory)
mkdir python_virtualenvs
cd python_virtualenvs

# create venv for all our stuff (ansibleplaybookrunner)
python3 -m venv ansibleplaybookrunner

# activate this env
# source ansibleplaybookrunner/bin/activate
source python_virtualenvs/ansibleplaybookrunner/bin/activate

# or if running from other directory (ansibleplaybookrunner)
source ../python_virtualenvs/ansibleplaybookrunner/bin/activate
# verify python location
which python3
# xxxxxxx/python_virtualenvs/ansibleplaybookrunner/bin/python3

```

To install all required python modules (e.g. ansible version, ansible runner, etc.)

```bash
# before running must install specific python modules
pip install -r requirements.txt

```

## Command line execution
To run this locally you need to invoke the applicationStart.sh file on the command line.

```bash
# invoke the playbook
./applicationStart.sh

# check the return code from last script run (0 is OK 1 is failed)
echo $?
```

## Ansible runner info
The open source [ansible runner module is utilized to invoke ansible via python](https://ansible-runner.readthedocs.io/en/stable/python_interface/#)

Notes on the runner module:
* Basic configuration is found w/in the env/settings file (e.g. idle_timeout). This must be adjusted based on playbook execution. For example, we have
some playbooks that take 20+ minutes to run and must adjust this setting.
* Runner utilizes a "PrivateDataDir" which writes out ansible execution info (e.g. artifacts/ansible_run_number/rc, status, stderr, stdout, etc.)

## Open Issues
The following are open issues/items 
* **Python2.x** unclear if this solution works for older python versions
* **CodeDeploy Integration** - it is assumed that .sh file returning non zero causes code deploy event hook failure. This needs to be validated.
