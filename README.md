[![Build status](https://travis-ci.org/QualiSystems/BreakingPoint-Controller-Shell-2G.svg?branch=dev)](https://travis-ci.org/QualiSystems/BreakingPoint-Controller-Shell-2G)
[![Coverage Status](https://coveralls.io/repos/github/QualiSystems/JBreakingPoint-Controller-Shell-2G/badge.svg)](https://coveralls.io/github/QualiSystems/BreakingPoint-Controller-Shell-2G)
[![PyPI version](https://badge.fury.io/py/BreakingPoint-Controller-Shell-2G.svg)](https://badge.fury.io/py/BreakingPoint-Controller-Shell-2G)
[![Dependency Status](https://dependencyci.com/github/QualiSystems/BreakingPoint-Controller-Shell-2G/badge)](https://dependencyci.com/github/QualiSystems/BreakingPoint-Controller-Shell-2G)
[![Stories in Ready](https://badge.waffle.io/QualiSystems/BreakingPoint-Controller-Shell-2G.svg?label=ready&title=Ready)](http://waffle.io/QualiSystems/BreakingPoint-Controller-Shell-2G)


![](https://github.com/stsuberi/SaraTest/blob/master/cloudshell_logo.png)

# Ixia BreakingPoint 2G Shells

**Release date:** February 2019

Shell version 1.0.0

Document version 1.0

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [Associating a CloudShell Service to a Non-Global Domain](#associating-a-cloudshell-service-to-a-non-global-domain)
* [Typical Workflows](#typical-workflows)
* [References](#references)
* [Release Notes](#release-notes)

## Overview
A shell integrates a device model, application or other technology with CloudShell. A shell consists of a data model that defines how the device and its properties are modeled in CloudShell, along with automation that enables interaction with the device via CloudShell.

### Traffic Generator Shells
CloudShell's traffic generator shells enable you to conduct traffic test activities on Devices Under Test (DUT) or Systems Under Test (SUT) from a sandbox. In CloudShell, a traffic generator is typically modeled using a chassis resource, which represents the traffic generator device and ports, and a controller service that runs the chassis commands, such as Load Configuration File, Start Traffic and Get Statistics. Chassis and controllers are modeled by different shells, allowing you to accurately model your real-life architecture. For example, scenarios where the chassis and controller are located on different machines.

For additional information on traffic generator shell architecture, and setting up and using a traffic generator in CloudShell, see the [Traffic Generators Overiew](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/LAB-MNG/Trffc-Gens.htm?Highlight=traffic%20generator%20overview) online help topic.

### Ixia BreakingPoint 2G Shells
To model an Ixia BreakingPoint device in CloudShell, use the following shells: 

▪ [BreakingPoint Chassis 2G Shell](https://community.quali.com/repos/1294/breaking-point-chassis-shell), which provides data model and autoload functionality to model and load the BreakingPoint Chassis to resource management.

▪ [BreakingPoint Controller 2G Shell (service)](https://community.quali.com/repos/1295/breaking-point-controller-shell), which provides functionality to load test configuration, run tests, get test results, etc.

### Standard version
The BreakingPoint 2G shells are based on the Traffic Shell standard version 2.0.0.

For detailed information about the shell’s structure and attributes, see the [Traffic Shell standard](https://github.com/QualiSystems/shell-traffic-standard/blob/master/spec/traffic_standard.md) in GitHub.

### Certified models
▪ BreakingPoint VE

### Requirements
Release: **Ixia BreakingPoint 2G shells**

▪ CloudShell version: 8.3 GA Patch 3 and above patches

▪ BreakingPoint application: 8.20 and above

## Data Model

The shell's data model includes all shell metadata, families, and attributes.

**BreakingPoint Families and Models**

The chassis families and models are listed in the following table:

|Family|Model|Description|
|:---|:---|:---|
|Traffic Generator Chassis|BreakingPoint Chassis|BreakingPoint Chassis|
|Module|Generic Traffic Generator Module|Modules located on the chassis|
|Port Group|Generic Port Group|Generic Port Group|
|Port|Generic Traffic Generator Port|Generic Traffic Generator Port|

**BreakingPoint Chassis Attributes**

The attribute names and types are listed in the following section of the Networking Shell Standard:

https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/Traffic%20Generator%20Chassis%20Standard.md#attributes

**BreakingPoint Controller Attributes**

The controller attribute names and types are listed in the following table:

|Attribute|Type|Description|
|:---|:---|:---|
|Test Files Location|String|Location for test related files.|

### Automation
This section describes the automation (drivers) associated with the data model. The shell’s driver is provided as part of the shell package. There are two types of automation processes, Autoload and Resource. Autoload is executed when creating the resource in the **Inventory** dashboard, while resource commands are run in the sandbox.

For Traffic Generator shells, commands are configured and executed from the controller service in the sandbox, with the exception of the Autoload command, which is executed when creating the resource.

The following commands are associated with a model inside the shell:

**BreakingPoint Chassis 2G Shell**

|Command|Description|
|:-----|:---------|
|Autoload|Discovers the chassis, its hierarchy and attributes when creating the resource. The command can be rerun in the Inventory dashboard and not in the sandbox, as for other commands.|

**BreakingPoint Controller 2G Shell**

|Command|Description|
|:-----|:-----|
|Load Configuration|Loads the configuration file prepared by your Admin. The load configuration file includes the settings to run the traffic test, for example, packet size, number of packets to send in parallel, interval at which to send packet batches, etc. The file also reserves the necessary ports. <br>**Note**: The load configuration file must be accessible from the Execution Server, see [Traffic Generators Overview](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/LAB-MNG/Trffc-Gens.htm?Highlight=traffic%20generator).|
|Start Traffic|Starts a test to generate and send traffic to the DUT, according to the settings provided in the configuration file.|
|Stop Traffic|Stops running the test to stop sending traffic from the traffic generator.|
|Get Result|Gets the test result file and attaches it to the sandbox.|
|Get Statistics|Gets real time statistics of the traffic test in either JSON or CSV format. <br>Set the command's inputs as follows: <br>▪ **View Name**: Type of statistics to return. For example, Port Statistics, Traffic Item Statistics, Flow Statistics, etc. The types may differ depending on the traffic generator. <br>▪ **Output Type (Enum)**: **JSON** or **CSV**. JSON prints the statistics to the sandbox's output, which is useful for API calls that can use the output; while CSV attaches a CSV file with the test's statistics to the sandbox.|
|Get Test File|Downloads the test file to the location specified in the **Test Files Location** attribute defined when you added the service to your blueprint.|

### Downloading the Shell
The BreakingPoint 2G shells are available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shells comprise:

|File name|Description|
|:-----|:-----|
|BreakingPoint Controller Shell 2G.zip|BreakingPoint Controller Shell package|
|BreakingPoint Chassis Shell 2G.zip|BreakingPoint Chassis Shell package|
|bp-offline-dependencies-2G-x.x.x.zip|Shell Python dependencies (for offline deployments only)|
|Cleanup.Reservation.zip|Teardown script for cleaning reservation|

## Importing and Configuring the Shell
This section describes how to import the BreakingPoint 2G shells and configure and modify the shell’s devices. 

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page.
  
  2. In CloudShell Portal, as Global administrator, open the **Manage – Shells** page.
  
  3. Click **Import**.
  
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**.

The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

### Offline installation of a shell

**Note:** Offline installation instructions are relevant only if CloudShell Execution Server has no access to PyPi. You can skip this section if your execution server has access to PyPi. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder. The dependencies folder may differ, depending on the CloudShell version you are using:

1. For CloudShell version 8.3 and above, see [Add Shell and script packages to the local PyPi Server repository](#add-shell-and-script-packages-to-the-local-pypi-server-repository).

2. For CloudShell version 8.2, perform the appropriate procedure: [Add Shell and script packages to the local PyPi Server repository](#add-shell-and-script-packages-to-the-local-pypi-server-repository) or [Set the python pythonOfflineRepositoryPath configuration key](#set-the-python-pythonofflinerepositorypath-configuration-key).

3. For CloudShell versions prior to 8.2, see [Set the python pythonOfflineRepositoryPath configuration key](#set-the-python-pythonofflinerepositorypath-configuration-key).

### Adding shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Servercomputer (by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offlinemode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
*pip download -r requirements.txt*. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the shell and click the shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Setting the python PythonOfflineRepositoryPath configuration key
Before PyPi Server was introduced as CloudShell’s python package management mechanism, the *PythonOfflineRepositoryPath* key was used to set the default offline package repository on the Quali Server machine, and could be used on specific Execution Eerver machines to set a different folder. 

**To set the offline python repository:**
1. Download the *bp-offline-package-1.0.7.zip* file, see [Downloading the Shell](#downloading-the-shell).

2. Unzip it to a local repository. Make sure the execution server has access to this folder. 

3.  On the Quali Server machine, in the *~\CloudShell\Server\customer.config* file, add the following key to specify the path to the default python package folder (for all Execution Servers):  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`

4. If you want to override the default folder for a specific Execution Server, on the Execution Server machine, in the *~TestShell\Execution Server\customer.config* file, add the following key:  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`

5. Restart the Execution Server.

### Configuring a new resource
In CloudShell, the component that models the device is called a resource. It is based on the shell that models the device and allows the CloudShell user and API to remotely control the device from CloudShell.

You can also modify existing resources, see [Managing Resources in the Inventory](http://help.quali.com/Online%20Help/8.3/Portal/Content/CSP/INVN/Mng-Rsrc-in-Invnt.htm?Highlight=managing%20resources).

**To create a resource for the chassis device:**
  1. In CloudShell Portal, **Inventory** dashboard, click **Add New**. 
     ![](https://github.com/stsuberi/SaraTest/blob/master/create_a_resource_device.png)
     
  2. From the list, select the **Breaking Point Chassis**.
  
  3. Enter the BreakingPoint chassis **Name** and **IP address**.
  
  4. Click **Create**.
  
  5. In the **Resource** dialog box, enter all the fields relevant for this device: 
  
|Attribute|Type|Description|
|:---|:---|:---|
|User|String|Admin user on the device.|
|Password|Password|Password for Admin user on the device.|
  6. Click **Continue**.

This command discovers the device, fills in its attribute values and creates the device’s structure in CloudShell (if the device has a structure).

## Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a Shell that uses new/updated dependencies. It applies to both online and offline dependencies.

### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.

2. Extract the zip file to the suitable offline package folder(s). 

3. Terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat).  

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.

## Typical Workflows

Workflow 1 - *Creating a new blueprint*
1. Create a new blueprint.
   * Log in to CloudShell Portal and create a new blueprint **Blueprint Catalog>Create Blueprint**.
   * Give the blueprint a name.
   
2. Add resources and services to the blueprint. 
   * Click the **Resource** button and add the BreakingPoint Chassis resource and all needed ports into the diagram. 
   * Associate the port's sub resources with the BreakingPoint Network Neighborhood Interfaces, by specifying the port's attribute **Logical Name** with the BP interface ID.
   * Click the **App/Services** tab and add the **BreakingPoint Controller 2G** service.
   * Specify the attribute **Test Files Location**, where test files will be downloaded.
   
3. Add a teardown script, which runs the driver command `cleanup_reservation` when the reservation ends. This command releases ports which were used by the sandbox. 
   * Go to the **Scripts** management page **Manage>Scripts>Environment**.
   * Click **Add New Script** and choose the **Cleanup Reservation.zip** file. 
   * Click **Edit** for the new added script and change **Script Type** to **Teardown**.
   * Return to the blueprint and open properties, **Blueprint>Properties**. 
   * In the **Driver** section, select **Python Setup & Teardown**, add **Estimated teardown duration** 1 min.
   * Click **Add Script** and chose **Cleanup Reservation** from the list. 
   * Click **Update** to save changes.

Workflow 2 - *Getting a test file with network configuration*

*You cannot change predefined Tests and Network Neighborhoods.  Predefined Network Neighborhoods will not be included in Test files.*

This scenario helps you use predefined Tests and Network Neighborhoods.

1. Duplicate the BreakingPoint Network Neighborhood configuration.
   * Open the BreakingPoint UI.
   * Go to **Control Center>Open Neighborhood**.
   * Find and select **Network Neighborhood** from the list.
   * Click **Save As** and enter **New Network Neighborhood Name**.
   * Click **Ok**.
   
2. Duplicate the BreakingPoint Test.
   * Go to **Test>Open Test**.
   * Find and select the **Test** from the list.
   * Press **Save As** and save it with a new name.
   
3. Change the Network Neighborhood in the duplicated test.
   * Find and select the duplicated test from the list and open it.
   * In the **Network Neighborhood** section, click ‘…’, find and select the duplicated Network Neighborhood.
   * Click **Save**.
   
4. Run the BreakingPoint Controller `GetTestFile` command.
   * Enter CloudShell Portal, and reserve the newly created blueprint.
   * Run the `BreakingPoint Controller service` command *GetTestFile* with the duplicated test name.
   * Open the folder specified in the attribute **Test Files Location**+<reservation_id> to view the file with the name of your duplicated test (extension “bpt”).

Workflow 3 - *Running a test*
1. Enter your blueprint.

2. Run the BreakingPointController service `Load Configuration` command.
   * Click BreakingPointController **Commands** and enter the service commands.
   * Find the `Load Configuration` command and enter the run menu.
   * Specify the **Breaking Point config file** with the path of your test configuration file. <br>It can be a full path, or relative path under the location specified in the attribute **Test Files Location**, such as *<reservation_id>/test_name.bpt*, or only *test_name.bpt*, if it is a current sandbox.
   * Click **Run**, to load the test and network configuration from this file and reserve necessary ports.
   
3. Run **Start Test**.
   * Click the BreakingPoint Controller **Commands** and enter the service commands.
   * Find the **Start Traffic** command and click **Enter** to run the menu.
   * Set **Blocking** to **True**, if you want subsequent commands to wait until the test finishes, or **False** to allow additional commands to run during the command's execution. 
   * Click **Run**.
   
4. Run **Stop Test**.
<br>If you ran the test with **Blocking** equals **False**, you can immediately stop the test.
   * Run the `Stop Traffic` command.
   
5. Get the test result file.
   * Run the `Get Result` command.
   * The test result file is attached to the sandbox.

## References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation, see [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 

## Release Notes
### What's New

* Added support for the Virtual Traffic Generator.
