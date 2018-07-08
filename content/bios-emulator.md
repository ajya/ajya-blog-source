Title: Outreachy: Simulating BIOS for sushy-tools
Date: 2018-07-08 18:00
Tags: outreachy, openstack

I can't believe that another 2 weeks have passed since the last blog post.
Shortly after my previous blog post about adding support for BIOS resource in `sushy` library it got merged \o/. The next thing was to add BIOS support for `sushy-tools` so that developers can use it during development to test against as bare metals with Redfish are not readily available. Also `sushy-tools` could be used in CI when running automated tests. There is another developer working on adding BIOS-Redfish support in Ironic.

To re-iterate on `sushy-tools`, it consists of two simulators `sushy-static` and `sushy-emulator`, Sushy static is straightforward - it serves JSON files from provided mockup folder where mockup files can be downloaded from DMTF Redfish page. Whatever is in those JSON files, is returned back to client. `sushy-emulator` is more dynamic and uses actual systems to emulate what is necessary for Redfish API. Now it supports 2 drivers - libvirt[[1]](https://libvirt.org/) and openstacksdk[[2]](https://docs.openstack.org/openstacksdk/latest/) (interchangeably also called nova driver).

And to re-iterate on Redfish BIOS resource - it provides BIOS attributes, updating those attributes, resetting the attributes to default and changing BIOS password.

I started to look at implementing BIOS support and writing up a story for storyboard, but stopped when decided to check what there is for libvirt and openstacksdk in relation to BIOS. Because at first I made assumption that there would be some API functions in libvirt and openstack libraries same as there were for parts already implemented. tl;dr; There is none.

Browsing through libvirt and openstack sdk I couldn't see anything that stand out as BIOS API.
Ok, so maybe there is nothing for BIOS, but maybe I don't know what I'm looking for (I don't have much experience with BIOS - as a computer user I have accessed BIOS to change boot order and enable hardware virtualization, if there was anything else I don't remember it). What are these "BIOS attributes"? Looking at the samples provided by DMTF, there are attributes like 'AdminPhone', 'BootMode', 'PowerProfile', 'UsbControl'. I take a look at my BIOS and cannot map these, probably there is something like that, but named slightly different (not expecting to see AdminPhone though).
Still I don't want this let go, and I want to find out how this should work on real servers that support Redfish.

This presentation[[3]](https://www.dmtf.org/sites/default/files/Dong_Wei_UEFI_APTS2017.pdf) comes handy and introduces me to UEFI HII (Human Interface Infrastructure) which would be the source for UEFI variables mapped to Redfish BIOS attributes. I read more about it at[[4]](https://uefi.blogspot.com/2009/09/uefi-hii-part-1.html) and then go back to libvirt. For openstacksdk it is already clear that there is nothing for BIOS.

A side note, here I'm not looking at legacy BIOS, but UEFI. BIOS is being replaced by UEFI and one day will be gone, however its name still will live in Redfish, Ironic and elsewhere, because at least for Ironic this name is chosen as better cannot be identified[[5]](https://specs.openstack.org/openstack/ironic-specs/specs/not-implemented/generic-bios-config.html#proposed-change).

Back to libvirt, I find that for virtual machines' UEFI, the term OVMF or AAVMF is used[[6]](http://blog.wikichoon.com/2016/01/uefi-support-in-virt-install-and-virt.html). Start searching using OVMF, find a doc about it, go through it[[7]](http://www.linux-kvm.org/downloads/lersek/ovmf-whitepaper-c770f8c.txt), and there it mentions NVRAM config file that contains something and my mentor had mentioned it. I need to take a look what is there. I create a VM with UEFI/OVMF[[8]](https://fedoraproject.org/wiki/Using_UEFI_with_QEMU) and get the sample file. Its extension is '.fd' and it's binary file. I try to find if there is some utility to read just to see if something useful is there. Couldn't find it, and even if there is such, it is not part of libvirt API - so `sushy-emulator` would bypass libvirt API and would have to work with it directly which is not ideal.

OK, here I give up and look at backup plan - have a set of string mimicking BIOS attributes with no effect on VM and stored at libvirt domain XML so that it is persisted between VM and sushy-tools reboots. Where would that be? I cannot find a place for it, but there is section named SMBIOS[[9]](https://libvirt.org/formatdomain.html#elementsSysinfo) in libvirt.
> System Management BIOS (SMBIOS) specification defines data structures (and access methods) that can be used to read management information produced by the BIOS of a computer

Sounds close enough? SBMBIOS has section `oemStrings` where it can store custom information. But it is added in the latest version released this spring, even I don't have it on my a little bit outdated Fedora (I will upgrade when Outreachy is over :)). And still this is not ideal place for custom data.
Talk with mentors and then we decide that we will start with storing this in emulator's memory that would not be persisted accross reboots. I promise to take another look if really, really there is nothing better in libvirt.
Next time I look and start reading the XML spec from the very beginning (not looking at table of contents which I did before) and here it is - under General data section, there is `metadata` section that allows to store whatever is necessary using own XML namespace. That is the perfect place for what we need.

There were some other obstacles before I could get to implementing this - due to Flask upgrade tests started to fail in `sushy-tools` and I tried to fix it (that would be another paragraph about this, but I'm leaving this out so the blog post does not get too long). Once I got back to implementation I did it in less than a day, but there were and still are other patches for sushy-tools which introduce new and restructure existing tests with which I need to align. After the direction to go was clarified I updated my tests.  
As of writing this, the patch is submitted and fails CI jobs.  
I fixed the first time it failed CI - it was concurrency issue which was not visible locally because I had `libvirtd` running. I stopped the service and was able to reproduce the test failures. But only when I run full test suite. When I tried to isolate the issue, the tests passed. I found the missing piece and fixed my test setup (had to nullify global driver) and it passed again, but then CI failed again with different errors. Perhaps more concurrency issues, suspecting global variable (everything fine locally).

Overall, it does not feel like already 2 weeks have passed but when I start writing about it a lot of interruptive things come up which I will leave out for brevity. One thing that stands out for me is that I was not noticing some things that I feel I should have. Better attention next time. The good thing - when I was researching UEFI BIOS thing I remembered about and used the Pomodoro technique[[10]](https://en.wikipedia.org/wiki/Pomodoro_Technique) with Gnome app[[11]](http://gnomepomodoro.org/) to keep myself focused. Worked flawlessly.


* [1] [Libivrt - libvirt.org](https://libvirt.org/)
* [2] [openstacksdk - openstack.org](https://docs.openstack.org/openstacksdk/latest/)
* [3] [Overview of the UEFI Forum - dmtf.org](https://www.dmtf.org/sites/default/files/Dong_Wei_UEFI_APTS2017.pdf)
* [4] [UEFI HII (Part 1) - uefi.blogspot.com](https://uefi.blogspot.com/2009/09/uefi-hii-part-1.html) 
* [5] [Hardware interface for BIOS configuration, Proposed change - openstack.org](https://specs.openstack.org/openstack/ironic-specs/specs/not-implemented/generic-bios-config.html#proposed-change)
* [6] [UEFI support in virt-install and virt-manager - blog.wikichoon.com](http://blog.wikichoon.com/2016/01/uefi-support-in-virt-install-and-virt.html)
* [7] [Open Virtual Machine Firmware (OVMF) Status Report - linux-kvm.org](http://www.linux-kvm.org/downloads/lersek/ovmf-whitepaper-c770f8c.txt)
* [8] [Using UEFI with QEMU - fedoraproject.org](https://fedoraproject.org/wiki/Using_UEFI_with_QEMU)
* [9] [SMBIOS System Information - libvirt.org](https://libvirt.org/formatdomain.html#elementsSysinfo)
* [10] [Pomodor Technique - wikipedia.org](https://en.wikipedia.org/wiki/Pomodoro_Technique)
* [11] [Gnome Pomodoro](http://gnomepomodoro.org/)
