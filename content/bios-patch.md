Title: Outreachy: Adding support for Redfish BIOS resource in sushy
Date: 2018-06-24 18:00
Tags: outreachy, openstack

Time flies and this is my 6th week in Outreachy project. 
My first 'big' task is to implement support for BIOS resource in sushy library.

BIOS resource is one of the Redfish resources beside many others, like Ethernet Interface, Processor which are already implemented in sushy. To shortly describe BIOS resource - it returns a list of BIOS attributes and allows to update them, it also has 2 "actions": Reset the attributes to default value and change BIOS password.

My starting point was an API scheme PDF[[1]](https://www.dmtf.org/sites/default/files/standards/documents/DSP2046_2017.0a.pdf) referenced in the ticket and merged patch of Ethernet Interface [[2]](https://git.openstack.org/cgit/openstack/sushy/commit/?id=8fe2904a62b0f56dc3fc3fefc5a5a746911ce891) which gave me idea which parts of the project I need to touch: implement classes for BIOS resource, add a release note, add a BIOS property to parent resource called System and add unit tests for the new BIOS resource and for new parts of System.

Sounds straightforward, could take a day or two? Of course it did not.

One of the first things I encountered was that for action "Change Password" there are no parameters specified. How to pass new password then? Looked around and discovered that the PDF referenced in the ticket is not the latest version. Found the latest version[[3]](https://www.dmtf.org/sites/default/files/standards/documents/DSP2046_2018.1_0.pdf) released 14 May 2018, after the ticket was created and this spec has parameters for "Change Password": NewPassword, OldPassword and PasswordName. At least this makes sense now, but what to do with those who are still on previous version? At some point in freenode IRC #openstack-ironic channel I asked this question and people there knew that this was issue with generating JSON schemas from CSDL. Turns out there are CSDL files which are schemas in XML and they appear to be source of truth, not JSON. Good to know, but somehow I'm still sticking to JSON and if in doubt look at CSDL. But I started to look more at JSON schemas themselves, rather then generated PDF. For example, BIOS has it schema at [[4]](https://redfish.dmtf.org/schemas/Bios.json). There is also Schema index [[5]](https://redfish.dmtf.org/redfish/schema_index), but it is easy to guess the URL if know the resource name.
With this resolved I was preparing to submit this patch for code review and while pre-reviewing myself I took another look at sample JSON file for BIOS resource to check if everything is covered. Here is the sample:

    :::javascript
    {
      "@odata.type": "#Bios.v1_0_3.Bios",
      "Id": "BIOS",
      "Name": "BIOS Configuration Current Settings",
      "AttributeRegistry": "BiosAttributeRegistryP89.v1_0_0",
      "Attributes": {
        "AdminPhone": "",
        "BootMode": "Uefi",
        "EmbeddedSata": "Raid",
        "NicBoot1": "NetworkBoot",
        "NicBoot2": "Disabled",
        "PowerProfile": "MaxPerf",
        "ProcCoreDisable": 0,
        "ProcHyperthreading": "Enabled",
        "ProcTurboMode": "Enabled",
        "UsbControl": "UsbEnabled"
      },
      "@Redfish.Settings": {
        "@odata.type": "#Settings.v1_0_0.Settings",
        "ETag": "9234ac83b9700123cc32",
        "Messages": [
          {
            "MessageId": "Base.1.0.SettingsFailed",
            "RelatedProperties": [
              "#/Attributes/ProcTurboMode"
            ]
          }
        ],
        "SettingsObject": {
          "@odata.id": "/redfish/v1/Systems/437XR1138R2/BIOS/Settings"
        },
        "Time": "2016-03-07T14:44.30-05:00"
      },
      "Actions": {
        "#Bios.ResetBios": {
          "target": "/redfish/v1/Systems/437XR1138R2/BIOS/Actions/Bios.ResetBios"
        },
        "#Bios.ChangePassword": {
          "target": "/redfish/v1/Systems/437XR1138R2/BIOS/Actions/Bios.ChangePassword"
        }
      },
      "@odata.context": "/redfish/v1/$metadata#Bios.Bios",
      "@odata.id": "/redfish/v1/Systems/437XR1138R2/BIOS"
    }

`Id`, `Name`, `AttributeRegistry`, `Attributes` covered, `Actions` covered, but what is this `@Redfish.Settings`? It's not in the schema. I start searching and find this described in Redfish Scalable Platforms Management API Specification[[6]](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.5.0.pdf), this has also HTML version [[7]](http://redfish.dmtf.org/schemas/DSP0266_1.5.0.html), it's handier for me. The field is described in section 7.2.2[[8]](http://redfish.dmtf.org/schemas/DSP0266_1.5.0.html#settings). Turns out this field is used where resource cannot be updated directly, as is the case for BIOS attributes - updates would require system reboot. Ok, looks like a reusable field. I talk with mentors and we decide this should be implemented as a separate patch to keep the patches smaller and make the BIOS patch dependent on this, a chained patch.
Also speaking of this specification[[6]](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.5.0.pdf)[[7]](http://redfish.dmtf.org/schemas/DSP0266_1.5.0.html), this is better starting point for all Redfish things than Schema PDF, schema PDF is just a human-readable presentation of JSON/CSDL schemas, but then again if reading this first it might be hard to relate to anything in it.
With only few days in I still was not comfortable with sushy project and was confusing myself how I should implement this re-usable field. In hindsight there is nothing to be confused about, but until I got there I peeked at base modules of sushy library to see what's happening there, otherwise I was just copying whatever was done in Ethernet Interface without really knowing and understanding what's happening under the hood.
One thing to mention, which I did not see at the beginning, is that sushy is not a serialization library that serializes JSON to Python classes and back - it does more. sushy users wouldn't have to know Redfish to use sushy with bare metals. It adds some processing where necessary to make its use handy and hides all the web service details. At least that's how I see it now.

With the Settings field done and submitted for code review I returned to the original BIOS patch to make it dependent on Settings patch and update to use Settings field. Then I noticed that there might be a thing that should have been implemented differently in Settings patch. The Settings object holds a URI (see `SettingsObject/@odata.id` in the sample above) where clients should PATCH and where committed attributes are visible. Committed attributes are those that user updated, but haven't been applied yet as they are waiting for the system reboot. Having this realization that sushy is not just a dumb serialization library, an idea came that sushy should load this resource automatically when user accesses the property in Python. And I made the update to do it. As the Settings field is re-usable field I had to support that it can create a new instance of its parent type. The code introduced some structures and approaches that were not seen anywhere in the project, so I was not sure that this was the way to go, but the only way to find this out is to submit it for code review. So in the next patch update for Settings field I have a re-usable field that could load a settings resource automatically and dynamically based on parent resource type.

With both patches updated and submitted I started to wait for code reviewer feedback. I have been warned that code reviews can take a while, so during that I had some other smaller tickets to work on, and later I started to look at the next bigger ticket.

Looong story short, there were many suggestions how to improve this (still keeping in mind that this is not just serialization library), how to change some things, at one point there was a `dict` inherited with `__setitem__` override that instead of updating the `dict` values, did PATCHing so that sushy user can write `attributes['ProcTurboMode'] = 'Disabled'` seamlessly without knowing what magic happens behind. This again introduced a lot of structures not seen anywhere else in the project and in the end it was deemed to be too confusing for user instead of being helpful, for example, with code above why does not attribute value in the dictionary change in the end?

Somewhere in between, one question remained unanswered regarding `@Redfish.Settings` - why isn't this field in the schema of BIOS? What are the other resources that could have this field? `grep`ing within provided mockup samples, found another case where Ethernet Interface[[9]](https://redfish.dmtf.org/redfish/mockups/v1/863#Managers--BMC--NICs--Dedicated) has this field, while other samples of Ethernet Interface did not have this property (e.g., [[10]](https://redfish.dmtf.org/redfish/mockups/v1/862#Managers--Blade1BMC--EthernetInterfaces--1)). Also in one of the older versions of mockup sample file Readme[[11]](https://www.dmtf.org/sites/default/files/standards/documents/DSP2043_1.1.0.zip) there was a short intro in Redfish, and it mentioned that this can also be applied to Storage resources, but I haven't any mockup samples for it so far. This raised another question - what does it mean that `@Redfish.Settings` field is not present? Does it mean that settings are read-only or that user should patch at the resource itself? The spec was not entirely clear and the Redfish implementations being available on servers which I don't have or have access to, I was not able to check how it works in real life. Talked with mentors, should this be asked in Redfish user forum or are there any other options to find this out, an e-mail thread was started where people with more knowledge on Redfish promptly clarified this - `@Redfish.Settings` is payload annotation field that can appear in any resource, but practically it will appear where immediate updates are not possible but restart of a system or a service is necessary. When the field is not present, it means that user can patch against the resource itself (not that it is read-only). BIOS will always have this field, because there are no known BIOS that can apply changes without reboot and not expecting to have any in near future. Ethernet Interfaces and Storage might have it or not, and now it is not expected to appear in any other resources.

Another thing that came up this week is, how to determine and inform sushy user of attribute update outcome. In the `@Redfish.Settings` field there are list of messages returned, time when changes were applied and `ETag` of the version the changes were applied. How to know when to check for the messages? Could there be some notifications received when updates are done? As there were more questions than answers, it was decided that in this patch this will not be exposed to sushy user to find a good solution in the next patch.

In the end with all the magic removed and even both patches merged back together (it was hard to review as it was changing back and forth), current patch versions are very close to the first versions I proposed. They still are in review, but hopefully will be done soon. I feel like I walked around the world to return at the same point, but during the trip I saw places and had some fun with Python.


* [1] [Redfish Resource and Schema Guide, v.2017.0a (PDF) - dmtf.org](https://www.dmtf.org/sites/default/files/standards/documents/DSP2046_2017.0a.pdf)
* [2] [Ethernet Interface sushy patch - git.openstack.org](https://git.openstack.org/cgit/openstack/sushy/commit/?id=8fe2904a62b0f56dc3fc3fefc5a5a746911ce891)
* [3] [Redfish Resource and Schema Guide (PDF), v.2018.1 - dmtf.org](https://www.dmtf.org/sites/default/files/standards/documents/DSP2046_2018.1_0.pdf)
* [4] [Redfish BIOS JSON schema - dmtf.org](https://redfish.dmtf.org/schemas/Bios.json)
* [5] [Redfish Schema Index - dmtf.org](https://redfish.dmtf.org/redfish/schema_index)
* [6] [Redfish Scalable Platforms Management API Specification (PDF) v.1.5.0 - dmtf.org](https://www.dmtf.org/sites/default/files/standards/documents/DSP0266_1.5.0.pdf)
* [7] [Redfish Scalable Platforms Management API Specification (HTML) v.1.5.0 - dmtf.org](http://redfish.dmtf.org/schemas/DSP0266_1.5.0.html)
* [8] [@Redfish.Settings - dmtf.org](http://redfish.dmtf.org/schemas/DSP0266_1.5.0.html#settings)
* [9] [Simple Rack-mounted Server mockup, Ethernet Interface - dmtf.org](https://redfish.dmtf.org/redfish/mockups/v1/863#Managers--BMC--NICs--Dedicated)
* [10] [Bladed System mockup, Ethernet Interface - dmtf.org](https://redfish.dmtf.org/redfish/mockups/v1/862#Managers--Blade1BMC--EthernetInterfaces--1)
* [11] [Scalable Platforms Management API Mockup Readme (ZIP), v.1.1.0 - dmtf.org](https://www.dmtf.org/sites/default/files/standards/documents/DSP2043_1.1.0.zip)
