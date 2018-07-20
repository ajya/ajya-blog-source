Title: Outreachy: Redfish Message registry and other
Date: 2018-07-20 12:00
Tags: outreachy, openstack

This time I will not act surprised that 2 more weeks have passed because I paid attention to time passing by.

In my previous blog post I mentioned that my last patch was failing CI. It turned out that the function `assert_called_once` is missing in Python 3.5. (it has `assert_called_once_with` though, but I can't use it this time). Locally I run Python 3.6 where this function is back, and there were no issues in Python 2.7. I replaced this with asserting `call_count` for now, but this patch still has to pass code reviews.

With that patch put in code review all green, I returned to `@Redfish.Settings` that had parts left out previously because of too many things that still required clarification. As it stands now, sushy users can update BIOS attributes, but for now sushy does not expose the status of this update.
To get the ball rolling I started to write some code and encountered another dependency - Message Registries. In Redfish response there would be id-s of messages, e.g., `Base.1.2.Success`, `Base.1.2.PropertyValueTypeError` and in registry file `Base.1.2.0.json` that would correspond to section like this[[1]](http://redfish.dmtf.org/schemas/registries/Base.1.2.0.json):

    :::javascript
    "PropertyValueTypeError": {
        "Description": "Indicates that a property was given the wrong value type, such as when a number is supplied for a property that requires a string.",
        "Message": "The value %1 for the property %2 is of a different type than the property can accept.",
        "Severity": "Warning",
        "NumberOfArgs": 2,
        "ParamTypes": [
            "string",
            "string"
        ],
        "Resolution": "Correct the value for the property in the request body and resubmit the request if the operation failed."
    }

In order to determine if update is successful need to consult the registry and give user some friendly message. In the given sample above the message supports templates and it has placeholders for parameters. sushy would have to build an error message passing the parameters from `@Redfish.Settings` for specific case. This approach also supports translating and localizing the messages. But for all this to work I need the registries. None of the provided mockup files have sample of these registries included. According to the schema they can be provided via `ServiceRoot.Registry` property. I remember somewhere I read that they are optional, but then how should sushy handle the case where Redfish service does not provide them? There could be 2 options: download the files programmatically from [[2]](http://redfish.dmtf.org/schemas/registries/) as necessary or include them in sushy package as fallback. Downloading the files wouldn't be a reliable option because sushy might not have access to the external Internet or the site could be just down. Bundling the files together is the direction to go, but then the mentor queried about the license of these files. These standard registry files provided by DMTF have only copyright statement, but no license. That would mean that this is proprietary and cannot be included in OpenStack projects as they require OSI approved license. No-one was sure and I'm not a lawyer either so it was time to contact OpenStack legal mailing list to clarify this[[3]](https://wiki.openstack.org/wiki/LegalIssuesFAQ). Before this I talked with the mentors what could be other options if the files couldn't be included - e.g., manually or using a script parse the files, generate a Python dict and store this derived dictionary instead of the original file.
In the questions to legal mailing list I also included this approach as possible option. Pretty quickly an answer came back which said: NO, the files cannot be included without a license and the same goes for the derived code. As of this writing this is still on-going and DMTF might apply 3-clause BSD license which would be OK for OpenStack project[[4]](https://governance.openstack.org/tc/reference/licensing.html).

On other tasks I did some cleanup patches that emerged from previous code reviews - what usually happens in code reviews is that reviewers notice other thing that need improvement but are not related to the patch in review. Or the necessity for changes is not so big to block the patch but can be done as a followup patch.
One of those patches were to clean up sushy-tools documentation to consistently use the same term. Somehow the docs started to have 'simulator' to describe sushy-emulator and sushy-static. It might have been me because I though of 'simulator' to be more general term. Went through some discussions [[5]](https://stackoverflow.com/questions/1584617/simulator-or-emulator-what-is-the-difference)[[6]](https://english.stackexchange.com/questions/111787/what-is-the-difference-between-simulate-and-emulate) to understand which is the right term to use. Turns out it is 'emulator'. Which also means that the title of my previous blog post is incorrect.

Another thing, I took over a patch that emulated Ethernet Interfaces in sushy-emulator. It was rather an old patch from January this year and since it was created sushy-tools had introduced support for openstackdriver and thus changed some structure in the Flask app too. I rebased and updated with the new structure and added support for openstacksdk driver. Which led me to setting up OpenStack cloud locally. A bit funny, but I haven't had a need to have access to OpenStack cloud before. This time I needed a sample to see how openstacksdk returns data for network interfaces, which was not entirely clear from the docs. I used dev-stack[[7]](https://docs.openstack.org/devstack/latest/) on a VM and it worked without any problems. This patch too is in code-review.

* [1] [Standard message registry, v.1.2.0](http://redfish.dmtf.org/schemas/registries/Base.1.2.0.json)
* [2] [Redfish registries - dmtf.org](http://redfish.dmtf.org/schemas/registries/)
* [3] [Legal Issues FAQ - openstack.org](https://wiki.openstack.org/wiki/LegalIssuesFAQ)
* [4] [Licensing requirements - openstack.org](https://governance.openstack.org/tc/reference/licensing.html)
* [5] [Simulator or Emulator? What is the difference? - stackoverflow.org](https://stackoverflow.com/questions/1584617/simulator-or-emulator-what-is-the-difference)
* [6] [What is the difference between “simulate” and “emulate”? - english.stackexchange.com](https://english.stackexchange.com/questions/111787/what-is-the-difference-between-simulate-and-emulate)
* [7] [DevStack - openstack.org](https://docs.openstack.org/devstack/latest/)
