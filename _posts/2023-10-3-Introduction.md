---
layout: post
title: Introduction to the 9800 Wireless Controller
---

This lab is designed to introduce the concepts of deploying an enterprise wireless network using the 9800 controller.

![9800 Wireless controllers]({{ site.baseurl }}/images/9800.jpg)

# Introduction

In this lab, you will learn the basic concepts of the deployment of wireless network in an enterprise environment. You will learn how to join an access point to the 9800 controller, configure the access point, create a basic SSID configuration, analyze what is sent over-the-air when a wireless clients associate with an access point and many other things.

Here is a brief summary of the steps involved in this lab :
1. Step 1 : Access the 9800 controller using SSH and the GUI
2. Step 2 : Join the access point to the controller
3. Step 3 : Configure the access point in Flex connect mode
4. Step 4 : Create an open SSID
5. Step 5 : Create a SSID with PSK encryption 
6. Step 6 : Explore monitoring capabilties on the controller
7. Step 7 : Perform an OTA (Over the Air) capture (instructor led)
8. Step 8 : Use the Cubietruck and ZoiPer over wireless

## Lab topology

In this lab, we will used the following components : 
- A 9800 wireless controller, already deployed in a virtual infrastructure
- A 3750 PoE switch, on which you will connect the access point and wired devices
- A wireless client (mobile phone, laptop etc.)
- A wired client (laptop) to access the 9800 controller interface

![Topology]({{ site.baseurl }}/images/topology.png)

Each pod will get a different port assigned to which to connect to, shown in the diagram above.

### 3750 switch configuration
The first thing you will need to do is to connect your 3750 switch to your assigned port on the main 3750 switch. This interface on your pod switch will need to be in **access mode, accessing VLAN X (given by instructor)**.

However, there are no DHCP pool configured for this VLAN yet. Configure a DHCP pool for VLAN X on your switch : 
1. Create an SVI in VLAN X and assign the IP address : 192.168.2.254
2. Create a DHCP pool for VLAN X (network : 192.168.2.0/24, gateway : 192.168.2.254)
3. Set the interace where your wired client is connected to access mode, access VLAN X

At this point, your wired client should get an IP address in VLAN X and you should be able to ping your controller IP address (192.168.2.204). 

## Step 1 : Access the 9800 wireless controller

The very first thing you will do during this session is to access the 9800 controller using SSH and the Graphical User Interface (GUI). Using the GUI is one of the preferred way to configure the controller, but SSH access is usually also required to perform some tasks.

Make sure you have IP reachability towards the 9800 controller before going further in this lab.

### GUI access 

Check if you can access the 9800 GUI using a browser :
`https://<WLC_IP_ADRESS>`

Enter the username/password provided by your instructor to access the main dashboard. You should get a page similar to this one : 

![Main dashboard]({{ site.baseurl }}/images/dashboard.png)

You are now able to access the 9800 wireless controller and ready to start ! 

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

## Step 2 : Join the access point

The next step is to join your access point (AP) to your controller. To join a lightweight access point to the controller, the AP needs to have the following :
- An IP address
- Learn the IP address of the controller, using DHCP option 43 in this lab
- IP reachability towards the controller

![AP Join]({{ site.baseurl }}/images/ap-join.png)

Therefore, to accomplish this task, you will need to do the following :
1. Create an SVI on the switch for VLAN 100 (random VLAN number, another can be used) and assign an IP address. Example : 192.168.10.254
2. Create a DHCP pool for your this network
3. In this DHCP pool, you will need to configure the option 43. This will be used by the AP to learn the IP address of the WLC. [How do I calculate option 43 ?](#option-43)
4. Once done, configure the switchport interface as a trunk interface and configure the native VLAN on this trunk to be the VLAN created above. This will allow the AP to request a DHCP address in the pool configured earlier. 
5. Once the AP got an IP address (`#show ip interface brief`), check that you can ping the WLC and that the AP learned the IP address of the controller. Use the command `show capwap client rcb` on the AP to see if it learned the IP address of the WLC.

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

Here are the VLANs that will be used for the wireless clients :
- **Vlan name** : VLAN30 (ID : 30)
- **Vlan name** : VLAN40 (ID : 40)

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

Instead of going on each component and configure them separately, you can use a wizard that will help you to configure them all in the same place. You can access the wizard by clicking this icon : 

![WLAN wizard]({{ site.baseurl }}/images/wlan-wizard.png)

Once on the wizard page, click "Start Now" at the bottom of the page and start configuring the following items : WLAN profile, policy profile and policy tag (for this last one, do not create a new one but use the default-policy-tag already created by default). 

### WLAN configuration 

You first need to create the WLAN configuration with the following information :
- **WLAN name** : Pod-X-Open
- **Security** : None

Once done, you can move to the creation of the policy profile that will be linked to the policy profile through the policy tag. 

### Policy profile configuration

You then need to create a new policy profile where you will configure the following information : 
- **Name** : PP_VLAN_30
- **Status** : Enabled
- **WLAN switching policy** :
    - Central switching : disabled
    - Central authentication : enabled 
    - Central DHCP : disabled
- **VLAN** : 30

### Policy tag configuration

Now, it's time to **tie the WLAN configuration with the policy profile**. This is done using the "policy tags". Under "Policy tags", select the default policy tag and add your newly created WLAN and associated policy profile and save.

**Check that your access point is correclty configured** : go to `Monitoring > Wireless > AP Statistics` and click the first blue icon next to your access point name. This will show you what is being broadcasted by your access point.

![APs SSIDs]({{ site.baseurl }}/images/ap-broadcast.png)

### Connect your wireless client

If you take your phone or laptop, you should see your SSID being broadcasted. You can attempt to connect to it. You should get an IP address from VLAN 30 and be able to access other ressources in this network. You can try to ping your gateway (which should be the SVI configured on the switch) to test the wireless connectivity. 

If you can ping your gateway, it means you successfully configured your SSID !

## Step 5 : PSK SSID

Sky is the limit! You can now configure any type of SSID. One of the most common securities seen on enterprise wireless networks are PSK and 802.1X. Configuring a 802.1X SSID requires the use of a RADIUS server, which we will do in our next lab session. 

You will configure here a PSK SSID. Here are the steps to do (you should be able to configure this pretty easily if you managed to create the open SSID) : 
1. Create a new SSID "Pod-X-PSK", using PSK as security. Define a password for this SSID.
2. Create a new policy profile "PP_VLAN_40", use the same switching policy and use VLAN 40
3. In the default-policy-tag, you can add this SSID/policy profile. Once added to the policy tag, you should see your new PSK SSID being broadcasted in addition to the open SSID. 

## Step 6 : Monitoring the AP and wireless clients

Once you connected a wireless client to your SSID, you should see it appearing under `Monitoring > Wireless > Clients`. This is where all clients connected to your wireless network will appear. 

By clicking on your client, you will get a lot of information : to which AP is it connected to, its received signal strength (RSSI), IP/MAC addresses, VLAN being used etc.

### Device profiling

It is also possible to get some profiling information about the clients connected to the controller and get more information about them. The 9800 is capable of using 3 differents methods to learn more about the clients :
- **MAC**
- **DHCP profiling** : uses information present in the DHCP packets 
- **HTTP profiling** : uses information present in the HTTP packets 

In order for Local profiling to work, simply enable "Device Classification" under Configuration > Wireless > Wireless Global. This option enables MAC OUI, HTTP and DHCP profiling at the same time :

![Device profiling]({{ site.baseurl }}/images/device-profiling.png)

You can then go to `Monitoring > Services > Local profiling` to see how the 9800 controller detected your devices.

Document explaining device profiling in details available [here](https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/215661-in-depth-look-into-client-profiling-on-9.html)


## Step 7 : Over the Air capture analysis

An interesting step in understanding the association/authentication flow between a wireless client and an access point is to take an Over the Air (OTA) capture when the client is associating to the SSID. 

![Wireless association]({{ site.baseurl }}/images/authentication-flow.png)

[Image credit](https://community.nxp.com/t5/Wireless-Connectivity-Knowledge/802-11-Wi-Fi-Security-Concepts/ta-p/1163551)

This can be done either using a laptop with the right wireless adapter (such as a MacBook), or using an AP in sniffer mode. Since not everyone might have such laptop, we will be working with sniffer mode access points. One group will setup its access point in sniffer mode, and the other group will initate the connection from one of their wireless device to their own SSID. 

Group 1 : Will configure the sniffer mode access point
Group 2 : Will configure the access point channel to a custom channel and handle client connections/disconnections

Odd pod number will configure their access point to sniff on a specific channel :
- **Pod 1** : Sniff on channel 36
- **Pod 3** : Sniff on channel 40
- **Pod 5** : Sniff on channel 44
- **Pod 7** : Sniff on channel 46
- **Pod 9** : Sniff on channel 52

Even pod number will configure their access point to broadcast on a specific channel :

- **Pod 2** : Broadcast on channel 36
- **Pod 4** : Broadcast on channel 40
- **Pod 6** : Broadcast on channel 44
- **Pod 8** : Broadcast on channel 46
- **Pod 10** : Broadcast on channel 52

### Group 1 : Configure an access point in sniffer mode

To configure an access point in sniffer mode, you will need to go to `Configuration > Wireless > Access Points`, select the access point, the change the "AP mode" to "Sniffer". The AP will rejoin the WLC and you will then be able to configure the sniffing channel and where to send the captured data.

To configure on which channel the AP will be listening, go to `Configuration > Wireless > Access Points`, expand the 5ghz band section, select the access point, then enable sniffing, select the channel you will sniff on and specify the IP address of the laptop on which Wireshark will run. 

In the "RF Channel Assignment" section, please make sure to set the assignment method to "Custom" and specify the channel width to 20Mhz and set the channel to the one you would like to sniff on (see table above). 

The data you will capture over the air needs to be sent somewhere. In our case, it will be a wired laptop (in the same VLAN of the controller) running Wireshark. 

Side note : ensure that the 9800 controller can reach the laptop running Wireshark, using a ping for example. 

#### Decode captured data

At this point, the AP is forwarding every packets seen on the channel you are sniffing on. However, these packets are encapsulated and you will need to decode them to see their content. To do this, you can stop the capture, right-click on a packet, select "Decode As" and then select "PEEKREMOTE".

![PEEKREMOTE]({{ site.baseurl }}/images/peekremote.png)

Wait for group 2 to finish its work and then try to start the capture, disconnect/connect a wireless client and stop the capture and try to find the following frames : 
- Beacons for your SSID
- Authentication request/response
- Association request/response
- 4-way handshake (M1, M2, M3, M4)

### Group 2 : Configure the channel of the access point

The point here will be to manually force the access point to broadcast on a specific channel (with a specific width). This will allow group 1 to sniff on the correct channel. 

To force an access point to broadcast on a specific channel, go to `Configuration > Wireless > Access Points`, in the "5Ghz band" section, select the access point, then go to the "RF Channel Assignment" section, select "Custom" for the assignment method and configure the channel as per the table above. Make sure to also configure the channel width to 20 Mhz in this case.

At this point, your AP will broadcast on the channel configured. You can verify this using a simple Wifi Analyzer tool on your laptop that analyzes the RF environment for example.

Once group 1 has configured its access point on sniffer mode, you can disconnect/reconnect a wireless client to generate the interesting traffic (association/authentication).

## Step 8 : Cubietruck & ZoiPer

This step consists of using your Cubietruck to handle call over wireless. You will need to have ZoiPer (softphone) installed on your wirless clients. 

You can connect your Cubietruck to your switch, place it in a specific VLAN (additionnal VLAN that you will create on the switch along with a SVI) and make sure it gets an IP address from a newly created DHCP pool.

Then, you can connect a wirless client to your SSID and try to reach the Cubietruck IP address. Once done, then you can start initiating phone calls between your wireless clients using the softphone.