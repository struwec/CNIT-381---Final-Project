### Teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Imports
import routers
import skills
import ansible_runner

# Router Info 
device_address = routers.router['host']
device_username = routers.router['username']
device_password = routers.router['password']

# RESTCONF Setup
port = '443'
url_base = "https://{h}/restconf".format(h=device_address)
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}

# Bot Details
bot_email = 'Botington@webex.bot'
teams_token = 'MGEwZGY5NGItMzI4OS00YjM0LWE3NGUtYzgzNWU5MzU2ZDEyODc3ZmIyODgtZDAz_P0A1_b34062fa-24f1-480f-a815-05d10d8cf4f2'
bot_url = "https://482f-144-13-254-60.ngrok.io"
bot_app_name = 'BotingtonTheThird Network Management Chatbot'

# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},],
)

# Bot Greeting
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm BotingtonTheThird, your friendly CSR bot! I hope I can be useful to you.  ".format(
        sender.firstName
    )
    response.markdown += "\n\nSee what I can do with **/help**."
    return response
    
# Provide System Information with RESTCONF
def sys_info(incoming_msg):
    """Return the system info
    """
    response = Response()
    info = skills.system_info_restconf(url_base, headers,device_username,device_password)

    if len(info) == 0:
        response.markdown = "I don't have any information of this device"
    else:
        response.markdown = "Here is the device system information I know. \n\n"
        response.markdown += "Device type: {}.\nSerial-number: {}.\nCPU Type:{}\n\nSoftware Version:{}\n" .format(
            info['device-inventory'][0]['hw-description'], info['device-inventory'][0]["serial-number"], 
            info['device-inventory'][4]["hw-description"],info['device-system-data']['software-version'])

    return response


# Router Command "show ip route" using Netmiko for both routers
def showRoute1(incoming_msg):
    response = Response()
    response.markdown = "These are HQ routes\n"
    response.markdown += skills.showRoute1()
    return response

def showRoute2(incoming_msg):
    response = Response()
    response.markdown = "These are Branch routes\n"
    response.markdown += skills.showRoute2()
    return response

# Router Command "show ip interface brief" using Netmiko for both routers
def showIpBrief1(incoming_msg):
    response = Response()
    response.markdown = "This is the IP Interface Brief for HQ\n"
    response.markdown += skills.showIpBrief1()
    return response

def showIpBrief2(incoming_msg):
    response = Response()
    response.markdown = "This is the IP Interface Brief for Branch\n"
    response.markdown += skills.showIpBrief2()
    return response

# Configure OSPF and EIGRP on both routers with Ansible
def config_EIGRP(incoming_msg):
    e = "eigrp"
    e = ansible_runner.run(private_data_dir='/home/devasc/labs/devnet-src/Final', playbook='eigrp.yaml')
    if(e=="eigrp"):
        return "EIGRP configuration failed!"
    return "EIGRP configured correctly"
    
def config_OSPF(incoming_msg):
    o = "ospf"
    o = ansible_runner.run(private_data_dir='/home/devasc/labs/devnet-src/Final', playbook='ospf.yaml')
    if(o=="ospf"):
        return "OSPF configuration failed!"
    return "OSPF configured correctly"

# Check for Neighbors 
def checkOSPF(incoming_msg):
    response = Response()
    response.markdown = "Now Showing OSPF Neighbor Statement\n"
    response.markdown += skills.checkOSPF()
    return response

def checkEIGRP(incoming_msg):
    response = Response()
    response.markdown = "Now Showing EIGRP Neighbor Statement\n"
    response.markdown += skills.checkEIGRP()
    return response


# Monitoring
def monitor(incoming_msg):
        skills.monitor_skill()
        
def isakmp(incoming_msg):
    response = Response()
    response.markdown = "These are the new VPN configurations on HQ and Branch routers\n"
    response.markdown += skills.show_isakmp()
    return response

# Set the bot greeting
bot.set_greeting(greeting)

# Bot's Commmands
bot.add_command("system info", "Show System Information", sys_info)
bot.add_command("show ip route HQ" , "Look at the routes on HQ router with Netmiko", showRoute1)
bot.add_command("show ip route Branch", "Look at the routes on Branch router with Netmiko", showRoute2)
bot.add_command("show ip int br HQ" , "Look at the IP interface brief on HQ", showIpBrief1)
bot.add_command("show ip int br Branch" , "Look at the IP interface brief on Branch", showIpBrief2)
bot.add_command("config ospf", "Configure OSPF routing protocol", config_OSPF)
bot.add_command("config eigrp", "Configure EIGRP routing protocol", config_EIGRP)
bot.add_command("check ospf", "View OSPF Neighbors", checkOSPF)
bot.add_command("check eigrp", "View EIGRP Neighbors", checkEIGRP)
bot.add_command("monitor", "Begins Monitoring Process", monitor)
bot.add_command("show crypto isakmp policy", "Check Monitoring by Viewing Isakmp Policy", isakmp)
bot.remove_command("/echo")

# Run the Script
if __name__ == "__main__":
    bot.run(host="0.0.0.0", port=5000)