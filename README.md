
# CNIT 381 Final Project Overview
This is Team 4's GitHub Repository for the CNIT 381 Final Project. This project aims to use a Cisco WebEx chatbot to monitor and configure devices.

# Setup
## WebEx Bot
The chatbot used for this project is a Cisco WebEx bot. To use a WebEx bot to monitor and configure devices create one through WebEx. After that note down its email, bot token, bot url, and its name. You will use this information to connect the skills/configurations to the bot.

## Install needed resources
- import routers
- import skills
- import ansible_runner
- import os
- import sys
- import sys
- import myParamiko as m
- import subprocess
- import time

## Python scripts
We started putting this bot together by using the 381bot.py file found on the Canvas page for this course. With that file we replaced the connecting information with that of our own bot. For this bot to work though, you will need to create a webhook for it. To do this enter the command ```ngrok http 5000```. After that copy the forwarding address that starts with https, this url will be used for the bot_url in the 381bot python file.
![Bot URL creation](/Images/ngrokHTTP.PNG)

In the 381bot.py file you will want to look for the bot details section of the code. In that section you will see one line start with bot_url. In the single quotation marks enter your the url for the webhook.
![Webhook URL entry](/Images/botURL.PNG)

## Bot commands
This bot allows you to run multiple commands. The commands that this bot allows you to run let you view the configuration of a device and configure a device. 

Bot commands:
- system info - Shows system information
- show ip route HQ - Looks at the routes on the HQ router with Netmiko
- show ip route Branch - Look at the routes on Branch router with Netmiko
- show ip int br HQ - Looks at the IP interfaces brief output of HQ router
- show ip int Branch - Looks at the IP interfaces brief output of Branch router
- config ospf - Configures OSPF
- config eigrp - Configures EIGRP
- check ospf - Views OSPF neighbors
- check eigrp - Views EIGRP neighbors
- monitor - Begins the monitoring process
- show crypto isakmp policy - Checks the monitoring process by viewing the Isakmp policy

## Device monitor
One of the things that this bot allows you to do is monitor when a device changes IP addresses. This feature is used to monitor when a router changes its IP address so that a VPN connection with a second router isn't dropped. When the first router changes its IP address the monitor takes note of that and sends a new configuration to the second router to maintain the VPN connection between the two.
![Device Monitor Diagram](/Images/vpndiag.PNG)

Footer
?? 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Se
