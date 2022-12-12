import os
import sys
import myParamiko as m
### For RESTCONF
import requests
import json
### For Netmiko
from netmiko import Netmiko 
from netmiko import ConnectHandler
import subprocess
import time

# Define the Routers
HQ = {'device_type': 'cisco_ios', 'host': '192.168.149.146', 'username': 'cisco','password': 'cisco123!','port': 22, 'secret': 'cisco', 'verbose': True}
Branch = {'device_type': 'cisco_ios', 'host': '192.168.149.147', 'username': 'cisco','password': 'cisco123!','port': 22, 'secret': 'cisco', 'verbose': True}

    
# Gain Access to System Information Using RESTCONF
def system_info_restconf(url_base,headers,username,password):
    url = url_base + "/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/"
    
    response = requests.get(url,
                            auth=(username, password),
                            headers=headers,
                            verify=False
                            )

    return response.json()["Cisco-IOS-XE-device-hardware-oper:device-hardware-data"]["device-hardware"]

    
# Monitor
def monitor_skill():
    previousAdd = ""
    currentAdd = ""
    while True:
        # Finds Branch Address
        connection = ConnectHandler(**HQ)
        prompt = connection.find_prompt()
        if '>' in prompt:
            connection.enable()
        output = ""
        output += connection.send_command("show ip int GigabitEthernet2 | i Internet")
        connection.disconnect()
        currentAdd = output[output.find("is")+3:output.find("/")]
        if currentAdd != previousAdd:
            comtosend = "set peer "+ currentAdd
            # Applies Configurations on Branch
            connection = ConnectHandler(**Branch)
            prompt = connection.find_prompt()
            if '>' in prompt:
                connection.enable()
            output = connection.send_command("show run | i set peer")
            previousAdd = output[output.find("peer")+4:]
            rempeercom = "no set peer "+ previousAdd
            connection.send_config_set(["crypto map Crypt 10 ipsec-isakmp", rempeercom])
            connection.send_config_set(["no crypto isakmp key cisco address " + previousAdd])
            connection.send_config_set(["crypto map Crypt 10 ipsec-isakmp", comtosend])
            connection.send_config_set(["crypto isakmp key cisco address "+ currentAdd])
            print("IP Changed from "+ previousAdd +" to "+ currentAdd)
            previousAdd = currentAdd
        time.sleep(30)


# Router Command "show ip route" using Netmiko    
def showRoute1():
    connection = ConnectHandler(**HQ)
    prompt = connection.find_prompt()
    if '>' in prompt:
        connection.enable()
    output = ""
    output += connection.send_command("show ip route")
    connection.disconnect()
    return output

def showRoute2():
    connection = ConnectHandler(**Branch)
    prompt = connection.find_prompt()
    if '>' in prompt:
        connection.enable()
    output = ""
    output += connection.send_command("show ip route")
    connection.disconnect()
    return output

def showIpBrief1():
    connection = ConnectHandler(**HQ)
    prompt = connection.find_prompt()
    if '>' in prompt:
        connection.enable()
    output = ""
    output += connection.send_command("show ip int brief")
    connection.disconnect()
    return output

# Check for Neighbors
def checkOSPF():
    connection = ConnectHandler(**HQ)
    prompt = connection.find_prompt()
    if '>' in prompt:
        connection.enable()
    output = ""
    output += connection.send_command("show ip ospf neighbor")
    connection.disconnect()
    return output

def checkEIGRP():
    connection = ConnectHandler(**HQ)
    prompt = connection.find_prompt()
    if '>' in prompt:
        connection.enable()
    output = ""
    output += connection.send_command("show ip eigrp neighbor")
    connection.disconnect()
    return output

# Router Command "show crypto isakmp policy" for router 1
def show_isakmp():
    connection = ConnectHandler(**HQ)
    prompt = connection.find_prompt()
    if '>' in prompt:
        connection.enable()
    output = ""
    output += connection.send_command("show crypto isakmp policy")
    connection.disconnect()
    return output

if __name__ == "__main__":
    import routers
    # Router Info 
    device_address = routers.router['host']
    device_username = routers.router['username']
    device_password = routers.router['password']
    # RESTCONF Setup
    port = '443'
    url_base = "https://{h}/restconf".format(h=device_address)
    headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

    intf_list = get_configured_interfaces(url_base, headers,device_username,device_password)
    for intf in intf_list:
        print("Name:{}" .format(intf["name"]))
        try:
            print("IP Address:{}\{}\n".format(intf["ietf-ip:ipv4"]["address"][0]["ip"],
                                intf["ietf-ip:ipv4"]["address"][0]["netmask"]))
        except KeyError:
            print("IP Address: UNCONFIGURED\n")