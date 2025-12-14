### 3. Guide Ansible : `ANSIBLE_GUIDE.md`
*Ce fichier reprend votre ébauche en corrigeant les commandes, en ajoutant la gestion de l'environnement virtuel et en structurant l'inventaire.*

```markdown
# Automatisation avec Ansible

Ce guide détaille la mise en place de l'environnement Ansible pour gérer la configuration des équipements Cisco de manière déclarative.

## 1. Installation de l'environnement

Pour éviter les conflits avec les paquets systèmes, nous utilisons un environnement virtuel Python.

```bash
# 1. Création et activation de l'environnement virtuel (si pas déjà fait)
python3 -m venv venv
source venv/bin/activate

# 2. Installation d'Ansible et des dépendances SSH
pip install ansible paramiko ansible-pylibssh

# 3. Installation de la collection Cisco IOS (Obligatoire pour les modules cisco.ios.*)
ansible-galaxy collection install cisco.ios

2. Inventaire (Inventory)

Le fichier inventory.ini définit les cibles et les variables de connexion.

Exemple de fichier inventory.ini :
Ini, TOML

[cisco_routers]
R1 ansible_host=172.16.1.1

[cisco_switches]
SW1 ansible_host=172.16.99.2
SW2 ansible_host=172.16.100.2

[all:vars]
# Variables communes à tous les équipements
ansible_user=admin
ansible_password=admin1234
ansible_connection=network_cli
ansible_network_os=cisco.ios.ios
ansible_become=yes
ansible_become_method=enable
ansible_become_password=admin1234

Pour vérifier que l'inventaire est bien lu par Ansible :
Bash

ansible-inventory -i inventory.ini --list

3. Test de Connexion

Avant de lancer les playbooks de configuration, il est essentiel de valider qu'Ansible peut se connecter aux équipements et s'authentifier.
Bash

# Pinge tous les équipements du groupe 'all'
ansible all -m ping -i inventory.ini

Résultat attendu : SUCCESS en vert pour R1, SW1 et SW2.
4. Exécution des Playbooks

Les playbooks sont des fichiers YAML décrivant l'état désiré du réseau.
A. Configuration du Routeur

Ce playbook configure les sous-interfaces et le routage inter-VLAN.
Bash

ansible-playbook router_vlans.yml -i inventory.ini

B. Configuration des Switchs

Ce playbook déploie les VLANs, assigne les ports d'accès et configure les Trunks.
Bash

ansible-playbook switch_vlans.yml -i inventory.ini