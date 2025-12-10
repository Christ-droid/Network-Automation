# CONFIGURATION INITIALE (BOOTSTRAP)

Ce document détaille la procédure de configuration manuelle **obligatoire** pour initialiser les équipements réseaux (Routeur et Switchs) dans GNS3. 

L'objectif est d'établir la connectivité de base et l'accès SSH nécessaire à l'exécution des scripts d'automatisation Python.

## 1. Résumé de la Topologie

| Équipement | Interface | Rôle | Réseau / VLAN |
| :--- | :--- | :--- | :--- |
| **Linux (Contrôleur)** | Eth0 | Hôte d'automatisation | `172.16.1.0/24` |
| **R1** (Vers Linux) | Fa1/0 | Passerelle du Linux | `172.16.1.1` |
| **R1** (Vers S1) | Fa0/0.99 | Passerelle de Gestion S1 | `172.16.99.1` (VLAN 99) |
| **R1** (Vers S2) | Fa0/1.100 | Passerelle de Gestion S2 | `172.16.100.1` (VLAN 100) |
| **Switch S1** | Vlan 99 | IP de Management | `172.16.99.2` |
| **Switch S2** | Vlan 100 | IP de Management | `172.16.100.2` |

---

## 2. Configuration du Routeur (R1)

Le routeur agit comme la passerelle centrale. Il doit gérer trois réseaux distincts : le lien vers le Linux et les deux VLANs de management pour les switchs.



```bash
conf t

! --- 1. Configuration Système de base ---
hostname R1
no ip domain lookup              ! Empêche la résolution DNS (évite les délais en cas d'erreur de frappe)
ip domain name rtp.cisco.com     ! Domaine requis pour générer les clés cryptographiques RSA

! --- 2. Sécurité et Utilisateurs ---
username admin privilege 15 secret admin1234  ! Création de l'admin avec privilèges max (15)
crypto key generate rsa modulus 1024          ! Génère la clé de cryptage pour activer le SSH

! --- 3. Activation du SSH (Lignes virtuelles) ---
line vty 0 15
 login local                     ! Utilise l'utilisateur "admin" défini plus haut
 transport input ssh             ! Force l'utilisation de SSH (bloque Telnet)
 exit

! --- 4. Interface vers le PC Linux ---
interface fa1/0
 ip add 172.16.1.1 255.255.255.0
 description LAN to Linux
 no shutdown
 exit

! --- 5. Interface vers Switch 1 (VLAN 99) ---
interface fa0/0
 no shutdown                     ! On active l'interface physique
 exit
! Sous-interface logique pour le Tagging VLAN
interface fa0/0.99
 encapsulation dot1Q 99          ! Indispensable : Définit que cette interface traite le VLAN 99
 ip add 172.16.99.1 255.255.255.0
 description LAN Gestion S1
 exit

! --- 6. Interface vers Switch 2 (VLAN 100) ---
interface fa0/1
 no shutdown
 exit
interface fa0/1.100
 encapsulation dot1Q 100         ! Traite le VLAN 100
 ip add 172.16.100.1 255.255.255.0
 description LAN Gestion S2
 exit

end
copy run start                   ! Sauvegarde la configuration
```

---

## 3.Configuration des Switchs (S1 et S2)

Les switchs doivents être accessible via une adresse IP de gestion (SVI)
- **IMPORTANT :** La commande 
```bash 
no ip routing 
```
est cruciale. Elle transforme le switch multicouche en switch de niveau 2, ce qui force l'utilisation de la passerelle par défaut pour répondre au ping du Linux.

**Instructions**
Adaptez les valeurs selon le switch que vous configurez :

- **S1** utilise le **VLAN 99**.
- **S2** utilise le **VLAN 100**.

```bash
conf t

! --- 1. Identité et Paramètres Système ---
hostname S1                      ! (ou S2)
no ip routing                    ! CRUCIAL : Désactive le routage pour que la Gateway fonctionne
no ip domain lookup
ip domain name rtp.cisco.com

! --- 2. Sécurité SSH ---
username admin privilege 15 secret admin1234
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 15
 login local
 transport input ssh
 exit

! --- 3. Création du VLAN de Gestion ---
! Le VLAN doit être déclaré pour que l'interface SVI monte
vlan 99                          ! (ou vlan 100 pour S2)
 name Gestion_S1                 ! (ou Gestion_S2)
 exit

! --- 4. Configuration de l'Interface Virtuelle (SVI) ---
interface vlan 99                ! (ou interface vlan 100 pour S2)
 ip add 172.16.99.2 255.255.255.0 ! (ou 172.16.100.2 pour S2)
 description LAN Gestion
 no shutdown
 exit

! --- 5. Passerelle par défaut ---
! Indispensable pour répondre aux pings venant du Linux
ip default-gateway 172.16.99.1   ! (ou 172.16.100.1 pour S2)

! --- 6. Configuration du Trunk (Uplink vers Routeur) ---
interface g0/0
 switchport trunk encapsulation dot1Q  
 switchport mode trunk
 ! On autorise le VLAN de gestion pour commencer (Python ajoutera les autres)
 switchport trunk allowed vlan 99,100
 no shutdown
 end

copy run start

```

---

## 4. Configuration de l'Hôte Linux
Le linux se trouve dans le réseau ```172.16.1.0/24```. Pour qu'il puisse envoyer des commandes aux switchs (qui sont dans les réseaux ```99``` et ```100```), il faut lui indiquer de passer par le routeur ```172.16.1.1```.

Ouvrez un terminal Linux et exécutez : 
```bash
# Ajouter la route vers le réseau de management de S1
sudo ip route add 172.16.99.0/24 via 172.16.1.1

# Ajouter la route vers le réseau de management de S2
sudo ip route add 172.16.100.0/24 via 172.16.1.1

# TEST DE CONNECTIVITÉ (Obligatoire avant de lancer Python)
ping -c 4 172.16.99.2
ping -c 4 172.16.100.2
```

---


