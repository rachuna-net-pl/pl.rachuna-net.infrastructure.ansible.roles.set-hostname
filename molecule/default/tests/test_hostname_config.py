import pytest
import re

HOSTS_PATH = "/etc/hosts"

@pytest.mark.parametrize("distro, expected_entry", [
    ("ubuntu", r"127.0.1.1\s+test-ubuntu\s+test-ubuntu.rachuna-net.pl"),
    ("almalinux", r"127.0.1.1\s+test-almalinux\s+test-almalinux.rachuna-net.pl"),
    ("alpine", r"127.0.1.1\s+test-alpine\s+test-alpine.rachuna-net.pl"),
])
def test_hosts_configuration(host, distro, expected_entry):
    os_name = host.system_info.distribution

    if distro in os_name:
        hosts = host.run("sudo cat "+HOSTS_PATH).stdout            
        assert re.search(expected_entry, hosts), f"Błąd! Wpis '{expected_entry}' nie istnieje w /etc/hosts dla {os_name}"

@pytest.mark.parametrize("distro, expected_entry", [
    ("ubuntu", r"test-ubuntu.rachuna-net.pl"),
    ("almalinux", r"test-almalinux.rachuna-net.pl"),
    # ponieważ nie restartuje systemu gdyż cloud-init ustawiłby ponownie hostname
    ("alpine", r"test-alpine.rachuna-net.pl"),
])
def test_hosts_configuration(host, distro, expected_entry):
    os_name = host.system_info.distribution

    if distro in os_name:
        hosts = host.run("hostname").stdout    
        assert re.search(expected_entry, hosts), f"Błądny hostname '{expected_entry}'"