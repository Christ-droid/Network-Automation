CONFIGURATION INITIALE


Routeur :


conf t

hostname R1

no ip domain lookup

ip domain name rtp.cisco.com

username admin privilege 15 secret admin1234

crypto key generate rsa modulus 1024
inter line vty 0 15
login local
transport input ssh
exit


inter fa1/0
ip add 172.16.1.1 255.255.255.0
description LAN to Linux
no shutdown
exit


inter fa0/0.99
encapsulation dot1Q 99
ip add 172.16.99.1 255.255.255.0
description LAN Gestion S1
exit
inter fa0/0
no shutdown


inter fa0/1.100
encapsulation dot1Q 100
ip add 172.16.100.1 255.255.255.0
description LAN Gestion S2
exit
inter fa0/1
no shutdown
end
 
copy run start




Switch (1 / 2) : 


conf t
hostname S1 / S2
no ip routing
no ip domain lookup
ip domain name rtp.cisco.com
username admin privilege 15 secret admin1234
crypto key generate rsa modulus 1024
ip ssh version 2
inter line vty 0 15
login local
transport input ssh
exit

vlan 99 / 100
name Gestion_S1 / Gestion_S2
exit
inter vlan 99 / 100
ip add 172.16.99/100.2 255.255.255.0
description LAN Gestion_S1 / Gestion_S2
no shutdown
exit

ip default-gateway 172.16.99/100.1
 
inter g0/0
switchport trunk encapsulation dot1Q
switchport mode trunk
switchport trunk allowed vlan 99,100
no shutdown
end
 
copy run start