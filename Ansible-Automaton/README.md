### Guide Ansible : 


# Automatisation avec Ansible

Ce guide détaille la mise en place de l'environnement Ansible pour gérer la configuration des équipements Cisco de manière déclarative.

## 1. Installation de l'environnement

Pour éviter les conflits avec les paquets systèmes, nous utilisons un environnement virtuel Python.

# 1. Création et activation de l'environnement virtuel (si pas déjà fait)

```bash
python3 -m venv venv
source venv/bin/activate

```

# 2. Installation d'Ansible et des dépendances SSH

```bash
pip install ansible paramiko ansible-pylibssh

```

# 3. Installation de la collection Cisco IOS (Obligatoire pour les modules cisco.ios.*)

```bash
ansible-galaxy collection install cisco.ios

```

## 2. Inventaire (Inventory)

Le fichier inventory.ini définit les cibles et les variables de connexion.

Pour vérifier que l'inventaire est bien lu par Ansible :

```bash

ansible-inventory -i inventory.ini --list

```

## 3. Test de Connexion

Avant de lancer les playbooks de configuration, il est essentiel de valider qu'Ansible peut se connecter aux équipements et s'authentifier.


```bash
# Pinge tous les équipements du groupe 'all'
ansible all -m ping -i inventory.ini

```

Résultat attendu : SUCCESS en vert pour R1, SW1 et SW2.
## 4. Exécution des Playbooks

Les playbooks sont des fichiers YAML décrivant l'état désiré du réseau.
# A. Configuration du Routeur

Ce playbook configure les sous-interfaces et le routage inter-VLAN.

```bash
ansible-playbook router_vlans.yml -i inventory.ini

```

# B. Configuration des Switchs

Ce playbook déploie les VLANs, assigne les ports d'accès et configure les Trunks.

```bash
ansible-playbook switch_vlans.yml -i inventory.ini

```
