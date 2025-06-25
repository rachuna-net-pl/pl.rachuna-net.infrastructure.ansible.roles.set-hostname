## Wymagania

- Ansible w wersji co najmniej 2.9
- System operacyjny: 
  - Debian (wszystkie wersje)
  - Ubuntu (wszystkie wersje)
  - Alpine Linux (wszystkie wersje)
  - RedHat Enterprise Linux (7, 8, 9)
- Uprawnienia administratora (root) na docelowych serwerach

---
## Funkcjonalność

Rola wykonuje następujące operacje:

1. **Zmiana nazwy hosta** - ustawia systemową nazwę hosta:
   - Wykorzystuje moduł `hostname` do zmiany nazwy
   - Obsługuje pełne nazwy domenowe (FQDN)
   - Automatycznie wykrywa typ systemu operacyjnego

2. **Konfiguracja pliku hosts** - modyfikuje plik `/etc/hosts`:
   - Dla systemów innych niż Alpine:
     ```
     127.0.1.1   hostname   hostname.fqdn
     ```
   - Dla systemu Alpine Linux:
     ```
     127.0.1.1   hostname.fqdn   hostname
     ```

3. **Zarządzanie restartem** - obsługuje restart systemu:
   - Automatyczny restart po zmianie nazwy (opcjonalny)
   - Możliwość wyłączenia restartu dla środowisk produkcyjnych

---
## Zmienne

### Zmienne konfiguracyjne (defaults/main.yml)

| Zmienna | Domyślna wartość | Opis |
|---------|------------------|------|
| `input_debug` | `false` | Włącza tryb debugowania |
| `input_hostname_fqdn` | `{{ inventory_hostname }}` | Pełna nazwa hosta (FQDN) do ustawienia |
| `input_disable_reboot` | `false` | Wyłącza automatyczny restart po zmianie nazwy hosta |

---
## Użycie

### Podstawowa konfiguracja

```yaml
- hosts: all
  roles:
    - role: set_hostname
      vars:
        input_hostname_fqdn: "serwer1.domena.pl"
```

### Konfiguracja bez restartu

```yaml
- hosts: all
  roles:
    - role: set_hostname
      vars:
        input_hostname_fqdn: "serwer1.domena.pl"
        input_disable_reboot: true
```

### Konfiguracja z użyciem zmiennych Ansible

```yaml
- hosts: all
  roles:
    - role: set_hostname
      vars:
        input_hostname_fqdn: "{{ ansible_distribution | lower }}-serwer.domena.pl"
```

---
## Bezpieczeństwo

Rola implementuje następujące praktyki bezpieczeństwa:

- Bezpieczna modyfikacja pliku hosts
- Zachowanie odpowiednich uprawnień plików systemowych
- Możliwość kontroli nad restartami systemu

---
## Testowanie

> [!tip]
> Rola zawiera testy Molecule, które można uruchomić następującymi komendami:

```bash
# Przygotowanie środowiska
python3 -m venv ~/.venvs/molecule
source ~/.venvs/molecule/bin/activate
pip install --upgrade pip
pip3 install ansible-core molecule molecule-proxmox pytest-testinfra ansible-lint molecule-plugins requests testinfra

# Uruchomienie testów
molecule test

# Pojedyncze komendy
molecule create    # Utworzenie środowiska testowego
molecule converge  # Uruchomienie roli
molecule verify    # Weryfikacja rezultatów
molecule destroy   # Usunięcie środowiska testowego
```

> [!tip]
> Testy znajdują się w katalogu `molecule/default/` i obejmują:
> - Weryfikację konfiguracji hostname
> - Sprawdzenie poprawności pliku hosts
> - Testy dla różnych dystrybucji Linux

---
## Uwagi

> [!important]
> ⚠️ **Ważne**: 
> - Zmiana nazwy hosta wymaga restartu systemu
> - Dla środowisk produkcyjnych zaleca się ustawienie `input_disable_reboot: true` i zaplanowanie restartu w odpowiednim oknie serwisowym
> - W przypadku systemów z cloud-init, hostname może zostać nadpisany po restarcie
