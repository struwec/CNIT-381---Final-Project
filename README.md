
# CNIT 381 Final Project Overview
This is Team 4's GitHub Repository for the CNIT 381 Final Project. This project aims to use a Cisco WebEx chatbot to monitor and configure devices.

# Setup
## WebEx Bot
The chatbot used for this project is a Cisco WebEx bot. To use a WebEx bot to monitor and configure devices create one through WebEx. After that note down its email, bot token, bot url, and its name. You will use this information to connect the skills/configurations to the bot.

## Install needed resources
---Fill in resources/libraries needed to make this run---

## Python scripts
We started putting this bot together by using the 381bot.py file found on the Canvas page for this course. With that file we replaced the connecting information with that of our own bot. For this bot to work though, you will need to create a webhook for it. To do this enter the command ```ngrok http 5000```. After that copy the forwarding address that starts with https, this url will be used for the bot_url in the 381bot.py file.

## Bot commands
This bot allows you to run multiple commands. The commands that this bot allows you to run let you view the configuration of a device and configure a device. 

Bot commands:
- Fill in command capabilities of the bot
-
-
-
-

## Device monitor
---Explain the monitoring skill point---
One of the things that this bot allows you to do is monitor when a device changes IP addresses. This feature is used to monitor when a router changes its IP address so that a VPN connection with a second router isn't dropped. When the first router changes its IP address the monitor takes note of that and sends a new configuration to the second router to maintain the VPN connection between the two.
![Device Monitor Diagram](/Images/vpndiag.png)

Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Se
