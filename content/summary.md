Title: Outreachy: Summary
Date: 2018-08-31 21:00
Tags: outreachy, openstack

This is the last blog post about my Outreachy internship that will summarize what I have done.

These are the 'main' additions to sushy and sushy tools project:

* initial version for BIOS resource support in sushy
* initial version for @Redfish.Settings used by BIOS and other resources in sushy
* emulation of BIOS resource in sushy-tools for libvirt driver and openstacksdk driver
* emulation of Ethernet Interface resource in sushy-tools (took over another patch and added openstacksdk driver part)
* support for Message registries in sushy (some parts still in code review)

However, the implementation is not entirely complete for BIOS and @Redfish.Settings resource support. There are some additional fields that were left out for the first version. In BIOS there is Attribute Registry which currently is not exposed to sushy users but it can help to determine what are the allowed attributes for a particular BIOS and other metadata about the attributes. At the moment there is no input validation happening when setting new BIOS attributes and any failure messages are left until applying the settings and getting back the results in @Redfish.Settings.
In @Redfish.Settings at the moment there is nothing implemented related to @Redfish.SettingsApplyTime. If supported by the Redfish service, this would allow to indicate preferred time to apply the updates.
Also for @Redfish.Settings multi-threading support is not added. In cases if there were 2 or more users trying to update BIOS settings at the same time, for user it will be hard to determine if the update was successful or if failures in the results are caused by their update or one of the peers.
When sushy starts supporting these features, these can also be added to sushy-tools emulation.

In addition to these patches, I did some smaller ones which were followup to these patches or some things that I encountered while working on the 'main' patches. One of the things was that tox was configured to use these python environments: py27, py35, pypy. I believe these were some standard template copy-paste or taken from another project. When running tox, I encountered interpreters not found error for py35 and pypy. Though tox has a flag to skip them, I asked my mentors what's the intention with these. After conversation I removed pypy because it is not expected that anyone will run sushy under pypy and replaced py35 with py3 so that the latest version of py3 is used. On my machine it was py36. Though I installed py35 side by side before removing the exact version from tox. Anyway, with these updates I was testing with py36 locally and I encountered 2 cases where Zuul CI which was still using py35 was failing when my environment was passing. I haven't looked into this more but for some reason there is something with methods in py35 when it is working fine in py27 and py36. So I am not entirely sure that is was ok to remove py35 locally as long as it is necessary to support it. I started to run py35 environment explicitly locally before putting in code review just in case there is this another odd exception with py35 in my code. Recently py36 was also added to Zuul CI so py36 gets tested there too now.

In one of my first blog posts I draw a diagram to comprehend the bare metal server domain which was new to me and I want to look at this diagram again as the internship has ended.
There are not much changes - only 1 new component was introduced for sushy-emulator to start using openstacksdk which was added around the same time my internship started. I did not get to work on Ironic part and overall did not have to interact with other components in the diagram, but it was useful to explore the surroundings back then.

![diagram: Context of sushy, updated]({filename}/images/project_overview_updated.png)

I think sushy and sushy-tools is a good starting point for new contributors - the project is small and easy to get around, though it did not appear so at the beginning - had to spend some time to get familiar with Redfish and the building blocks of sushy. At the beginning of the internship I had this 'I have no idea what I'm doing' feeling (shadowed by excitement that I'm working on OpenStack), but now I feel comfortable in this domain.

Overall I learned a lot during this 3 months internship and I would like to thank everyone who made this happen, especially my mentors Ilya and Dmitry. Best summer ever.

If anyone else is interested in Outreachy and would like to participate in the next round, they can check their eligibility and start applying very soon - 10th September, see [Outreachy web page](https://www.outreachy.org/).
