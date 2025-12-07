import sys

try:
    from config_router import run_router_config
    from Netmiko.config_switch import run_switches_config
#    from config_vpcs import run_vpcs_config
except ImportError as e:
    print("Erreur : Il manque un fichier de script (config_router.py, etc).")
    print(f"Détail : {e}")
    sys.exit(1)

def main():
    print("==========================================")
    print("   LANCEMENT DE L'AUTOMATISATION RÉSEAU   ")
    print("==========================================\n")

    # 1. Configuration du routeur (Prioritaire pour la passerelle)
    run_router_config()

    # 2. Configuration des Switchs
    # (Peut échouer si les switchs ne sont pas accessibles par IP)
    run_switches_config()

    # 3. Configuration des PCs (Indépendant du réseau, utilise la console)
#    run_vpcs_config()

    print("\n==========================================")
    print("       CONFIGURATION TERMINÉE             ")
    print("==========================================")

if __name__ == "__main__":
    main()