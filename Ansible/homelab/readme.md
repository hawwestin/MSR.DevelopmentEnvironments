# Diagnostic
**IMPORTANT:** Always set the ANSIBLE_CONFIG environment variable before running playbooks:
This fix issue with paths to ansible roles.
By default it looks for them under playbooks directory. 

```bash
export ANSIBLE_CONFIG=$PWD/Ansible/homelab/ansible.cfg
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password
```


# General
This is a drop of my homelab setup and context to reader that may find this on Github. 
HomeLab pc/servers verious in use and form. In 2026 There is; 
- One Qnap Nas an old unit with all quorks of pre-build system. 
- One Raspberry pi 4b 4gb
- Two Dell optiplex
- One TopTone fanless minipc 

# Purpose
This repo is my mess of learning new stuff that I found interesting to learn or at leass get a grasp of concept. 

My commercial expirience is a factor in this journey. 

One of the main purpose is to have some kind of backup in case any of homelab hosts dies and I need to reconfigure those. Manual things are beeing lost over years of thinkering around boxes. Today I'm mature enough to follow practices that are slower than just slamming shell snippets via ssh but in long run more stable. 