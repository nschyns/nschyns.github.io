---
layout: post
title: Wireless automation lab with Radkit
---

This lab is designed to introduce the fundamental concepts Radkit and how to use it to access wireless controllers (or any other device !)

![Radkit]({{ site.baseurl }}/images/radkit_logo.png)

# Introduction

In this lab, you will learn the basic concepts of Radkit and how to leverage this tool to access your lab devices. You also see how to run a python script using Radkit and how easy it is to configure devices using this tool, without the need for VPN, tunnels etc.

Here is a brief summary of the steps involved in this lab :  
1. Step 1 : Download and install the Radkit client on your laptop
2. Step 2 : Access your 9800 controller via CLI
3. Step 3 : Access your 9800 controller via GUI
4. Step 4 : Run a python script using Radkit
5. Step 5 : Verify the result of the script

## Topology

You can see here how Radkit works with the Radkit client. The Radkit client connects to a cloud service. The Radkit service is installed somewhere in your network (laptop, server, container) and also connects to the Radkit Cloud. Thanks to that, your radkit client is able to talk to the radkit service (and therefore, to all your devices which are allowed), without the need for a VPN !

![Radkit Topology]({{ site.baseurl }}/images/radkit_topology.png)

## Step 1 : Download and install the Radkit client

You will need to download and install the Radkit client on your computer for this lab.

### Windows

Download the Radkit client [here](https://radkit.cisco.com/downloads/release/1.6.9/cisco_radkit_1.6.9_win64_signed.exe). 

Execute the file and follow the instructions (Next, Accept etc.). The installation might take a few minutes to complete.

Add the following environment variable to your path `C:\Users\Administrator\AppData\Local\Programs\Cisco RADKit\env\Scripts\`. You can search for "Environment Variables" on Windows, click "Environment Variables", then click on the "Path" entry > Edit and then add this entry. 
 
#### Verify the installation

Open a command prompt (`Windows + R > cmd`) and type `radkit-client --version`. If you can see the version printed, you are good to go. If not, please reach out to an instructor.

### Mac 

Download the Radkit client using [this link](https://radkit.cisco.com/downloads/release/1.6.9/) and select the right file depending on your architecture. If you have an M1, M2, M3 Mac, download the arm64 version, otherwise download the x86_64 version.

Execute the ".pkg" file and follow the installation process.

#### Verify the installation

Open a command line interface and type `radkit-client --version`. If you can see the version printed, you are good to go. If not, please reach out to an instructor.

## Step 2 : Access your 9800 controller via CLI

The first thing is to open the **Radkit Network Console** (simplified version with no python and easier to use).

Once the console is open :
1. Type `login`. Your browser open a cisco.com SSO session, accept it
2. Type `service mk9h-kku8-p35k no-sr​`. This will connect you to the service that was setup for this lab. In case you would like to connect to your own service, replace the service name.

```
> login

[nschyns] > service mk9h-kku8-p35k no-sr
Connecting to Service: mk9h-kku8-p35k without SR context

[nschyns@mk9h-kku8-p35k] > show inventory
```

To access your device, simply type `interactive wlcX`, where X is the WLC number assigned to you :

```
[nschyns@mk9h-kku8-p35k] > interactive wlcX


Attaching to  wlc1  ... 
 Type:  ~.  to detach. 
        ~?  for other shortcuts. 
When using nested SSH sessions, add an extra  ~  per level of nesting. 

Warning: all sessions are logged. Never type passwords or other secrets, except at an echo-less password prompt.

WLC-X#
```

From there, you can access the 9800 wireless controller and check a few things : 

```
show version
show inventory
show wlan summary
```

You will now see that Radkit does not only allow CLI access !

## Step 3 : Access your 9800 controller via GUI

In the **Radkit Network Console**, you can start an HTTP proxy using the following command : 
```
[nschyns@mk9h-kku8-p35k] > proxy start http 4000
```

### Firefox users

You need to do a small configuration on the browser to make this working. Go to the Settings, search for "Proxy", then click "Settings". 
![Firefox proxy]({{ site.baseurl }}/images/firefox_proxy.png)

Under the "Automatic Proxy Configuration URL", enter the following value and click OK : https://prod.radkit-cloud.cisco.com/pac?port=4000&protocol=HTTP

![Firefox proxy]({{ site.baseurl }}/images/connection_settings.png)

Then access the following link : [https://index.proxy/](https://index.proxy/). Select the service number.

![HTTP proxy]({{ site.baseurl }}/images/http_proxy.png)

You should see the wireless controller that is assigned to you. Click on the "Go to web page" link.
![HTTP access]({{ site.baseurl }}/images/http_wlc.png)

Accept the security warning (self signed certificates) and you should now see the Day-0 Wizard to configure the wireless controller.

![Day 0 Wizard]({{ site.baseurl }}/images/day0.png)

## Step 4 : Run a python script using Radkit

Radkit has even more under the hood! You can actually build your own Python script (for example to reset or configure a network device with a specific configuration) and leverage Radkit to execute the script ! Check out how fast and easy this is.

### Download and check the script

First, download the following [python script]() on your computer.

You can open it and review it using your favorite python editor.

### Run the script

How can we run this script ? Easy ! Execute the following command from a command line interface :
`radkit-client script radkit-test-script.py myccoid@cisco.com wlcX`

Example :
`radkit-client script radkit-test-script.py ndarchis@cisco.com wlc1`

## Step 5 : Verify the result of the script

Once the script is executed, you can verify if it worked. Go to [https://index.proxy/](https://index.proxy/), select the service number, and open the Web page of your WLC. You should now see the dashboard of the wireless controller instead of the Day 0 wizard. This is because the script added a configuration (`wireless country XX`) which has the effect to disable the day 0 configuration wizard.

![9800 dashboard]({{ site.baseurl }}/images/9800_dashboard.png)
