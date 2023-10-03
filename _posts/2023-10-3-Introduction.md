---
layout: post
title: Introduction to the 9800 Wireless Controller
---

This lab is designed to introduce the concepts of deploying an enterprise wireless network using the 9800 controller.

![9800 Wireless controllers]({{ site.baseurl }}/images/9800.jpg)

# Introduction

In this lab, you will learn the basic concepts of the deployment of wireless network in an enterprise environment. You will learn how to join an access point to the 9800 controller, configure the access point, create a basic SSID configuration, analyze what is sent over-the-air when a wireless clients associate with an access point and many other things.

Here is a brief summary of the steps involved in this lab :
1. Access the 9800 controller using SSH and the GUI
2. Join the access point to the controller
3. Configure the access point in Flex connect mode
4. Create an open SSID
5. Create a SSID with PSK encryption 
6. Explore monitoring capabilties on the controller
7. Perform an OTA (Over the Air) capture (instructor led)
8. Use the Cubietruck and ZoiPer over wireless

## Step 1 : Access the 9800 wireless controller

The very first thing you will do during this session is to access the 9800 controller using SSH and the Graphical User Interface (GUI). Using the GUI is one of the preferred way to configure the controller, but SSH access is usually also required to perform some tasks.

In this lab, you can setup a static IP address on your laptop in the same range as the wireless controller (IP address will be given by the instructor). Make sure you have IP reachability towards the 9800 controller before going further in this lab.

### SSH access 

To access the 9800 controller using SSH, you will need to enable SSH on the device. The configuration is the same as on any other Cisco device. You will need to check the following things : 
- Is SSH enabled on the device ?
- Are the VTY lines configured to use SSH ? 

Then, from your laptop, use your terminal (or putty) to access the 9800 using SSH and check the version the 9800 controller is running :
```
#show version
Cisco IOS XE Software, Version 17.03.07
Cisco IOS Software [Amsterdam], C9800-CL Software (C9800-CL-K9_IOSXE), Version 17.3.7, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
```

### GUI access 

Once SSH access is established, check if you can access the 9800 GUI using a browser :
`https://<WLC_IP_ADRESS>`

Enter the username/password provided by your instructor to access the main dashboard. You should get a page similar to this one : 

![Main dashboard]({{ site.baseurl }}/images/dashboard.png)

You are now able to access the 9800 wireless controller and ready to start ! 

## Step 2 : Join the access point

The next step is to join your access point (AP) to your controller. To join a lightweight access point to the controller, the AP needs to have the following :
- An IP address
- Learn the IP address of the controller, using DHCP option 43
- IP reachability towards the controller

Therefore, to accomplish this task, you will need to do the following :
1. Create a DHCP pool for your managment VLAN (VLAN used for the access points, choose any VLAN)
2. In this DHCP pool, you will need to configure the option 43. This will be used by the AP to learn the IP address of the WLC. [How do I calculate option 43 ?](#option-43)
3. Once done, configure the switchport interface as a trunk interface and configure the native VLAN on this trunk to be the management VLAN. This will allow the AP to request a DHCP address in the pool configured earlier. 
4. Once the AP got an IP address, check that you can ping the WLC and that the AP learned the IP address of the controller. Use the command `show capwap client rcb` on the AP to see if it learned the IP address of the WLC.

#### Option 43

To calculate the option 43 value you will need to set in your DHCP pool, you need to convert the IP address of your controller in HEX format. Once done, the option 43 needs to be the following : 
`Type + Length + Value` where Type = f1, Length = 04 (you have 4 octets in the IP address) and value = the IP address converted in hex format.

Example : if the WLC's IP address is 192.168.1.1, the option 43 will be : f104c0a80101. 

Here is the command to configure it within the DHCP pool on a Cisco switch : 
```
option 43 hex <hexadecimal string>
```

[Official documentation for option 43, with example](https://www.cisco.com/c/en/us/support/docs/wireless-mobility/wireless-lan-wlan/97066-dhcp-option-43-00.html#anc9)

#### Check if the AP has joined the controller

If your AP can reach the WLC and started discovering the WLC, you should see the access point appearing in the dashboard of your 9800. However, it is possible that the AP might not have the right image running, and therefore, it will download the new image direclty from the controller itslef (upgrade is automatic). The controller and the AP need to run the same version at all times, otherwise they will not work with each other. 

After the AP downloaded the image from the controller, it should reboot and come up as "Registered" on the 9800 GUI.

Navigate to `Monitoring > Wireless > AP Statistics` to check if the AP has joined and is "Registered". You should be able to see the MAC/IP address of the access point, the AP model etc. 

![Main dashboard]({{ site.baseurl }}/images/ap_joined.png)

## Step 3 :Configure the access point 

## Step 4 : Open SSID

## Step 5 : PSK SSID

## Step 6 : Monitoring the AP and wireless clients

## Step 7 : Over the Air capture analysis

## Step 8 : Cubietruck & ZoiPer
