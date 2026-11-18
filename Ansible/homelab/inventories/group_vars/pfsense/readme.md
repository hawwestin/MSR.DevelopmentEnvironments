Test Privilage escalation. 
```bash
ansible pfsense -m command -a "whoami" --become
```