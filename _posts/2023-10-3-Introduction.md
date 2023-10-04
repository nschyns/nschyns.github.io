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

![AP join]({{ site.baseurl }}/images/ap_joined.png)


## Step 3 : Configure the access point 

As a quick test, change the AP name from the 9800 controller and check if this is reflected on the AP console. To change the AP name, go to `Configuration > Wireless > Access Points`, click on the access point and change the name, then click on "Update & Apply". 

Console/SSH to the access point and you should see the name of the access has changed.

![AP name]({{ site.baseurl }}/images/ap-name.png)

> If SSH is disabled on the access point (if you can ping it but cannot establish SSH connection to it), then go to `Configuration > Tags & Profile > AP Join`, select the "default-ap-profile" and configure the following : 
> - Under `Management > User`, configure a username and password + secret
> - Under `Management > Device`, check the "SSH" checkbox 
> - Update & Apply to device 

Next step will be to convert this access point from "Local" mode to "Flexconnect" mode. This will allow us to decide where the traffic will be released (at the controller level vs at the AP level) for each SSID configured.

To modify the mode of the access point, you will need to [**create a new "site tag"**](#create-a-new-site-tag), which will be configured as a remote site, to simulate the fact that your AP is in a remote location and that you want the AP to be in Flex connect mode. 

As a reminder, there are 3 types of tag : 
- **Policy Tag**: This tag links a WLAN Profile (SSID) to a Policy Profile.
- **Site Tag**: This tag defines the AP mode and other AP settings through the AP join profile and Flex profile.
- **RF Tag**: This tag sets the RF profiles with the settings for each band.

![Configuration model]({{ site.baseurl }}/images/config-model.png)

### Create a new site tag

To create a new site tag, go to `Configuration > Tags & Profiles > Tags > Site`, click "Add" and create new site tag called "flex-site-tag" and uncheck the "Enable Local Site" checkbox. You can leave other values as default.

![Flex site tag]({{ site.baseurl }}/images/flex-site-tag.png)

The next step is to apply this site tag to your access point to convert it to Flex mode. To do this, go to `Configuration > Wireless > Access Points`, click on the access point and change the site tag to the newly created site tag "flex-site-tag" and click "Update & Apply". This will reset the CAPWAP tunnel between the AP and the WLC, and in addition the AP will reboot to change its mode. After a few minutes, you should see the AP again under `Configuration > Wireless > Access Points` and you can verify its mode is changed to "Flex" :

![Flex mode]({{ site.baseurl }}/images/AP-flex-mode.png)

### Configure the flex profile

For this lab, we will decide to **switch the wireless client traffic locally**, meaning that all the traffic coming from the wireless client will be release at the AP level and forwared to the switch. Another possiblity is to centrally switch the traffic to the controller, and in this case all the wireless clients traffic is encapsulated inside a CAPWAP tunnel and forwared to the controller. 

Since all the wireless client traffic will be switched locally, the client VLANs needs to be configured on the access point. This is done through the "flex profile" (remember, everything is configured through the WLC, not on the AP direclty).

Here is a table showing the VLANs that will be used for the wireless clients :

| VLAN name  | VLAN ID  |
|----------|----------|

| VLAN30    | 30    |
| VLAN40    | 40    |

Note : you will need to configure an SVI in these VLANs on your switch and create a DHCP pool for both VLANs. This will allow the wirless clients to get an IP address when connecting to the SSIDs. 

Go to `Configuration > Tags & Profiles > Flex`, select the default-flex-profile and configure the following things : 
- Under the `General` tab, enter the native VLAN. This should be the native VLAN configured on the trunk interface where your AP is connected
- Under "the `VLAN` tab, add the VLANs that will be used for your clients (VLAN 30 and 40)

Sanity check : console/SSH to access point and verify the VLANs are present on the AP : `#show flexconnect vlan-name`

You are now ready to configure your very first SSID ! 

## Step 4 : Open SSID

Here is the interesting part : you will now learn how to create your very first SSID. This is fairly simple and does not require a lot of configuration. Your instructor will show you how to create a simple SSID and you will try to replicate this and be able to test it with your own devices.

There are three main components to configure on the 9800 controller when creating an SSID : 
1. The [**WLAN** configuration](#wlan-configuration) : SSID name, security (open, PSK, 802.1X) etc.
2. The [**policy profile** configuration](#policy-profile-configuration) : where you configure the VLAN used by the clients, timers etc.
3. The [**policy tag** configuration](#policy-tag-configuration), used to combine the WLAN and the policy profile. The current policy tag applied to your AP is the "default policy tag" and we will keep this one. 

### WLAN configuration 

You first need to create the WLAN ((`Configuration > Tags & Profile > WLANs`)) configuration with the following information :

| WLAN Name  | Security |
|----------|----------|

| Pod-X-Open   | None    |

Once done, you can move to the creation of the policy profile that you will link the WLAN with. 

### Policy profile configuration

You then need to create a new policy profile (`Configuration > Tags & Profile > Policy`) where you will configure the following information : 

| Name  | Status  | WLAN switching policy  | VLAN  |
|----------|----------|----------|----------|

| PP_VLAN_30    | Enabled    | Central switching : disabled<br />Central Authentication : enabled<br />Central DHCP : disabled| 30 |


### Policy tag configuration

Now, it's time to t**ie the WLAN configuration with the policy profile**. This is done using the "policy tags". Navigate to `Configuration > Tags & Profile > Tags > Policy`, select the default policy tag and add your newly create WLAN and associated policy profile and save.

Check that your access point is correclty configured : go to `Monitoring > Wireless > AP Statistics` and click the first blue icon next to your access point name. This will show you what is being broadcasted by your access point.




## Step 5 : PSK SSID

## Step 6 : Monitoring the AP and wireless clients

## Step 7 : Over the Air capture analysis

## Step 8 : Cubietruck & ZoiPer