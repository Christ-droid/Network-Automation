---

### 2. Guide Netmiko : `NETMIKO_GUIDE.md`
*Ce fichier explique comment utiliser les scripts Python que vous avez uploadés (`main.py`, etc.).*

```markdown
# Automatisation avec Python & Netmiko

Ce dossier contient les scripts Python permettant de configurer les équipements Cisco via SSH en utilisant la librairie `Netmiko`.

## Structure des fichiers

* `main.py` : Point d'entrée principal. Il orchestre l'exécution des configurations (Routeur puis Switchs).
* `config_router.py` : Contient la logique pour configurer les sous-interfaces (VLAN 10, 20, 30, 40) sur R1.
* `config_switch.py` : Contient les dictionnaires de définition des switchs et les commandes pour configurer les VLANs et les ports d'accès.

## Installation

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances.

```bash
# 1. Création de l'environnement virtuel
python3 -m venv venv

# 2. Activation
source venv/bin/activate

# 3. Installation des requis
pip install netmiko

Utilisation

Une fois l'environnement activé et la connectivité SSH validée (voir README principal), lancez simplement le script principal :
Bash

python3 main.py