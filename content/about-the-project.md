Title: Outreachy: About the project
Date: 2018-06-05 15:00
Tags: outreachy, openstack

When it came to choose a project for which to apply in Outreachy, I was looking for 3 things: mentors are in about the same timezone as me, the project is in tech stack I'm familiar with and want to expand my skills in it, and last but but not least, the project's domain is something interesting and completely new to me.

With the last point I set myself up for a lot of reading (and some videos). 

At first I felt like that dog in meme 'I have no idea what I'm doing'. To wrap my head around this, I started to draw a picture with some boxes. Here is the result: 

![diagram: Context of sushy]({filename}/images/project_overview.png)

The project I'm working on is `sushy` and `sushy-tools` project. 

`sushy` is related to, but not exactly part of, OpenStack Ironic project which deals with bare metal provisioning. Usually when talking about clouds, talk about virtual machines (VM), but there are cases where VMs do not provide necessary performance, so non-virtualized environment is necessary. Here comes Ironic project to manage bare metal servers in cloud environment - remotely. Ironic can be used independently or together with other OpenStack projects with whom it integrates. `sushy` is written in a way that it does not depend on Ironic and can be used by other projects. And Ironic can decide to use something else instead of `sushy`. But what does `sushy` do? Time to introduce Redfish. 

Redfish is a standard API to work with bare metal servers. It lives in BMC (Baseboard Management Controller) which is a microcontroller (small computer) attached to motherboard of industrial servers. BMC allows to manage servers remotely and Redfish is one of the protocols to do it. The Redfish standard is managed by DMTF (Distributed Management Task Force).

`sushy` is a client library in Python for Redfish RESTful web services communicating in JSON. `ironic` imports `sushy` and uses it as one of the drivers.
`sushy` is not the only Python library to consume Redfish API, there are alternatives named very similarly:
python-redfish [[5]](https://github.com/openstack/python-redfish)
python-redfish-library [[6]](https://github.com/DMTF/python-redfish-library)

Besides `sushy` there is also project `sushy-tools` which contains emulators for testing `sushy`. Otherwise it is challenging for developers to test Redfish as real server with BMC and Redfish is necessary. There are 2 emulators:
`sushy-static` which serves static JSON files provided by Redfish project. Mockups can be found at White Papers and Technical Notes section[[4]](https://www.dmtf.org/standards/redfish) looking for DSP2043. There is Redfish Mockup Creator[[7]](https://github.com/DMTF/Redfish-Mockup-Creator) to generate mockup files from a real Redfish service. But this is little use to me as I don't have access to real Redfish service, but nice to know just in case.

Static mockup file emulator is OK for read only testing, but it does not help much when want to test actions where some changes are necessary. In this case there is `sushy-emulator` which uses `libvirt` driver connecting to virtual machine mimicking real server. 

DMTF also provides similar emulators, both static mockup files[[8]](https://github.com/DMTF/Redfish-Mockup-Server) and dynamic[[9]](https://github.com/DMTF/Redfish-Interface-Emulator). I haven't tried these yet, but might try them out later.
With all the alternatives available, it appears that each project takes different approach, so it is not like they are copies of each other and in the end there is choice.

Lastly, there are some acronyms that I've seen floating around in relation to Ironic that are not directly related to sushy, but I had to find out what they are and how they are related.

PXE (Preboot eXecution Environment) is way to boot up servers from network. Computers supporting PXE has NIC (network interface controller) that is up and listening to commands from network even when server itself is turned off.

IPMI (Intelligent Platform Management Interface) is a way how to manage and monitor servers remotely. 

PXE and IPMI have been used together to deploy servers, but they are supposed to be replaced by newer technologies addressing some of their drawbacks - HTTP Boot and Redfish [[10]](https://www.youtube.com/watch?v=L-DQKEHX81Q).

`libvirt`, already mentioned above, is API to manage virtualization, supporting wide range of hypervisors, including VirtualBox, VMWare, Hyper-V.

As always, in hindsight this all speaks for itself, but then again while writing this I discovered new places to go though I can avoid them now - this is just enough for `sushy`. It will be interesting to revisit this at the end of project and see what has changed in my point of view.

Next time I will write about first tasks I'm working on that should allow me to tell more about `sushy` and Redfish.


* [1] [Ironic project wiki - openstack.org](https://wiki.openstack.org/wiki/Ironic)
* [2] [Ironic User Guide - openstack.org](https://wiki.openstack.org/wiki/Ironic)
* [3] [Sushy documentation - openstack.org](https://docs.openstack.org/sushy/latest/)
* [4] [Redfish API docs - dmtf.org](https://www.dmtf.org/standards/redfish)
* [5] [python-redfish - github.com](https://github.com/openstack/python-redfish)
* [6] [python-redfish-library - github.com](https://github.com/DMTF/python-redfish-library)
* [7] [Redfish Mockup Creator - github.com](https://github.com/DMTF/Redfish-Mockup-Creator)
* [8] [Redfish Mockup Server - github.com](https://github.com/DMTF/Redfish-Mockup-Server) 
* [9] [Redfish Interface Emulator - github.com](https://github.com/DMTF/Redfish-Interface-Emulator)
* [10] [Talk from 2015 UEFI Plugfest. Firmware in the Data Center: Goodbye PXE and IPMI. Welcome HTTP Boot and Redfish! - youtube.com](https://www.youtube.com/watch?v=L-DQKEHX81Q)
* [11] [In-browser Mockup file explorer -  dmtf.org](https://redfish.dmtf.org/redfish/v1)
* [12] [Intro videos about Redfish API - dmtf.org](https://redfish.dmtf.org/webinars)
* [13] [BMC - wikipedia.org](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface#Baseboard_management_controller)
* [14] [Microcontroller - wikipedia.org](https://en.wikipedia.org/wiki/Microcontroller)
* [15] [Preboot Execution Environment - wikipedia.org](https://en.wikipedia.org/wiki/Preboot_Execution_Environment)
* [16] [Libvirt - wikipedia.org](https://en.wikipedia.org/wiki/Libvirt)

