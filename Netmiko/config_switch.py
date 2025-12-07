from netmiko import ConnectHandler

# --- DÉFINITION DES SWITCHS ---
switches_info = [
    # --- SWITCH 1 (IP: 172.16.99.2) ---
    {
        'name': 'Switch S1',
        'device_type': 'cisco_ios',
        'ip': '172.16.99.2',    # Connexion via le VLAN 99
        'username': 'admin',
        'password': 'admin1234',
        'secret': 'admin1234',
        'config_cmds': [
            # 1. VLANs
            'vlan 10', 'name PC1_VLAN',
            'vlan 20', 'name PC2_VLAN',
            'exit',

            # 2. Ports Utilisateurs
            'interface GigabitEthernet0/1',
            'switchport mode access', 'switchport access vlan 10', 'spanning-tree portfast', 'no shutdown', 'exit',

            'interface GigabitEthernet0/2',
            'switchport mode access', 'switchport access vlan 20', 'spanning-tree portfast', 'no shutdown', 'exit',

            # 3. Trunk Uplink (Préserve le SSH sur VLAN 99)
            'interface GigabitEthernet0/0',
            'switchport trunk encapsulation dot1q',
            'switchport mode trunk',
            'switchport trunk allowed vlan 10,20,30,40,99,100', 
            'no shutdown',
            'exit',

            # 4. Gateway
            'ip default-gateway 172.16.99.1'
        ]
    },

    # --- SWITCH 2 (IP: 172.16.100.2) ---
    {
        'name': 'Switch S2',
        'device_type': 'cisco_ios',
        'ip': '172.16.100.2',    
        'username': 'admin',
        'password': 'admin1234',
        'secret': 'admin1234',
        'config_cmds': [
            # 1. VLANs
            'vlan 30', 'name PC3_VLAN',
            'vlan 40', 'name PC4_VLAN',
            'exit',

            # 2. Ports Utilisateurs
            'interface GigabitEthernet0/1',
            'switchport mode access', 'switchport access vlan 30', 'spanning-tree portfast', 'no shutdown', 'exit',

            'interface GigabitEthernet0/2',
            'switchport mode access', 'switchport access vlan 40', 'spanning-tree portfast', 'no shutdown', 'exit',

            # 3. Trunk Uplink
            'interface GigabitEthernet0/0',
            'switchport trunk encapsulation dot1q',
            'switchport mode trunk',
            'switchport trunk allowed vlan 10,20,30,40,99,100',
            'no shutdown',
            'exit',

            # 4. Gateway
            'ip default-gateway 172.16.100.1'
        ]
    }
]

def run_switches_config():
    print("\n--- DÉBUT CONFIGURATION SWITCHS (VIA VLAN 99) ---")
    
    for device in switches_info:
        print(f"Connexion à {device['name']} ({device['ip']})...")
        try:
            # Établissement de la connexion SSH
            net_connect = ConnectHandler(
                device_type=device['device_type'],
                ip=device['ip'],
                username=device['username'],
                password=device['password'],
                secret=device['secret'],
                conn_timeout=10
            )

            net_connect.enable()

            print(f"Envoi de la configuration sur {device['name']}...")

            # Envoi des commandes
            output = net_connect.send_config_set(device['config_cmds'])

            net_connect.save_config()

            print(f"Succès : Configuration appliquée sur {device['name']}.")
            net_connect.disconnect()

        except Exception as e:
            print(f"ERREUR sur {device['name']} : {e}")

    print("--- FIN CONFIGURATION SWITCHS ---\n")

if __name__ == "__main__":
    run_switches_config()