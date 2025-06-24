### Przykładowe użycie
```yml
- name: Hardening Machine
  hosts: all
  become: yes
  gather_facts: yes

  roles:
  - role: set-hostname
    vars:
      input_debug: false
      input_hostname_fqdn: "test-{{ ansible_distribution | lower }}.rachuna-net.pl"
      input_disable_reboot: true

```
### Testy molecule
# molecule
```bash
python3 -m venv ~/.venvs/molecule
source ~/.venvs/molecule/bin/activate
pip install --upgrade pip

pip3 install ansible-core molecule molecule-proxmox pytest-testinfra ansible-lint molecule-plugins requests testinfra

export TEST_PROXMOX_DEBUG=
export TEST_PROXMOX_HOST=
export TEST_PROXMOX_PORT=
export TEST_PROXMOX_USER=
export TEST_PROXMOX_PASSWORD=
export TEST_PROXMOX_NODE=

molecule test

# molecule create
# molecule converge
# molecule verify
# molecule destroy
 ```