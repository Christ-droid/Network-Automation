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
- **IMPORTANT :** La commande ```bash no ip routing ``


