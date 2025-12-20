from netmiko import ConnectHandler
import address_table as add


# Paramètres de connexion (Management via Fa1/0)
router_info = {
    'device_type': 'cisco_ios',
    'ip': '172.16.1.1',  # IP accessible depuis votre Linux
    'username': 'admin',
    'password': 'admin1234',
    'secret': 'admin1234'
}

print("In root")

# Commandes basées sur votre tableau Excel
# ADAPTEZ "GigabitEthernet0/0" si votre routeur utilise "FastEthernet0/0"
commands = [
    # VLAN 10
    'interface Fa0/0.10',
        'encapsulation dot1Q 10',
        'ip address 192.168.10.1 255.255.255.0',
        'exit',

    # VLAN 20
    'interface Fa0/0.20',
        'encapsulation dot1Q 20',
        'ip address 192.168.20.1 255.255.255.0',
        'exit',


    'interface Fa0/0',
        'no shutdown',
        'exit',

    # VLAN 30
    'interface Fa0/1.30',
        'encapsulation dot1Q 30',
        'ip address 192.168.30.1 255.255.255.0',
        'exit',

    # VLAN 40
    'interface Fa0/1.40',
        'encapsulation dot1Q 40',
        'ip address 192.168.40.1 255.255.255.0',
        'exit',

    'interface Fa0/1',
        'no shutdown',
        'exit',



    # DHCP CONFIGURATION
    'ip dhcp excluded 192.168.10.1 192.168.10.10',
    'ip dhcp excluded 192.168.20.1 192.168.20.10',
    'ip dhcp excluded 192.168.30.1 192.168.30.10',
    'ip dhcp excluded 192.168.40.1 192.168.40.10',

    'ip dhcp pool VLAN-10',
        'network 192.168.10.0 255.255.255.0',
        'default-router 192.168.10.1',
        'exit',

    'ip dhcp pool VLAN-20',
        'network 192.168.20.0 255.255.255.0',
        'default-router 192.168.20.1',
        'exit',

    'ip dhcp pool VLAN-30',
        'network 192.168.30.0 255.255.255.0',
        'default-router 192.168.30.1',
        'exit',

    'ip dhcp pool VLAN-40',
        'network 192.168.40.0 255.255.255.0',
        'default-router 192.168.40.1',
        'exit',
]

def run_router_config():
    print("\n--- DÉBUT CONFIGURATION ROUTEUR ---")
    try:
        net_connect = ConnectHandler(**router_info)
        print(f"Connecté à {router_info['ip']}")

        output = net_connect.send_config_set(commands)
        print(output)

        net_connect.disconnect()
        print("OK : Routeur configuré.")
    except Exception as e:
        print(f"ERREUR Routeur : {e}")
    print("--- FIN CONFIGURATION ROUTEUR ---\n")

if __name__ == "__main__":
    run_router_config()