Title: Outreachy: How I got started with OpenStack development
Date: 2018-05-20 18:00
Tags: outreachy, openstack

The first week has passed and in this post I will cover what I did to get my first contribution during application phase and some follow up reading afterwards. 
Here I will focus on general tools used in OpenStack development workflow. In next post I will write about the project I'm working on.

It was easy to start developing for OpenStack projects and almost everything I needed to know is well documented in one long page[[1]](https://docs.openstack.org/infra/manual/developers.html). The page contains some links to follow for more detailed information.
One of such pages that I find useful is about commit messages[[2]](https://wiki.openstack.org/wiki/GitCommitMessages) that not only writes about messages themselves, but about splitting commits in smaller patches where split is reasonable and somewhat isolated rather than creating one large patch which is harder to review for everyone involved. Also commit messages should be self-contained and hold enough information to understand what's being done and why without accessing other systems like issue/bug tracker. This also says that commit message bodies should be wrapped at 72 characters. The main page[[1]](https://docs.openstack.org/infra/manual/developers.html) only mentions commit message headers that should be 50 characters.

Then there are specific OpenStack code style guidelines for Python[[3]](https://docs.openstack.org/hacking/latest/user/hacking.html) that also references the general Python style guide, PEP 8[[4]](https://www.python.org/dev/peps/pep-0008/). Here I'm relying on `tox` to catch any violations.

To write some code, I cloned the necessary projects, branched, and made some changes. There were some tools missing from my development environment that I installed as I went by, and I did not encounter any setup related issues when running projects.

Once the changes are done, the next step is to submit it for code review. 

Gerrit is used  for code review, it used to be written in Python, but was rewritten in Java. Wikipedia says[[5]](https://en.wikipedia.org/wiki/Gerrit_(software)#History) that it was done to make it easier to run on different Linux systems, but it does not give any reference to source and a quick search online did not help me to find any historical discussions, but this is not so important here, was just curious.
More about Gerrit it is written at [[6]](https://review.openstack.org/Documentation/intro-quick.html). Gerrit distinguishes between core reviewers and regular reviewers, something that I have not seen in other tools where coders enforce it manually. In such cases, it is not like they try to bypass core reviewer requirement (as system does not enforce it), but it makes hard to identify open code reviews that are missing core reviewers, so it is nice that Gerrit has this built-in.

There is a handy tool git-review[[7]](https://docs.openstack.org/infra/git-review/) to make work with Gerrit easier - to submit code review just run `git review` instead of following instructions in Gerrit's quick intro[[6]](https://review.openstack.org/Documentation/intro-quick.html).

Once code review submitted Zuul[[8]](https://docs.openstack.org/infra/zuul/) gets involved. Don't have to interact with this much, but Zuul will be the one who will tell if there are tests failing and PEP 8 guidelines violated. This should have been checked locally before submitting code review, but there are always more integrations to run and other issues that might not show up in local environment. As there are many patches submitted within the same time frame, Zuul will queue them and test queued patches together according to their place in queue to catch any conflicts between patches before they get merged to master.
Then when code review is done and usually it requires 2 core code reviewers to approve, the Zuul will merge the changes to master.

That's all for now, if I encounter something new or something I misunderstood in relation to workflow and tools, will share it in further posts.


* [1] [OpenStack development manual - https://docs.openstack.org/infra/manual/developers.html](https://docs.openstack.org/infra/manual/developers.html)
* [2] [Git messages guidelines - https://wiki.openstack.org/wiki/GitCommitMessages](https://wiki.openstack.org/wiki/GitCommitMessages)
* [3] [OpenStack Python style guidelines - https://docs.openstack.org/hacking/latest/user/hacking.html](https://docs.openstack.org/hacking/latest/user/hacking.html)
* [4] [Python style guidelines - https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)
* [5] [Gerrit History in Wikipedia - https://en.wikipedia.org/wiki/Gerrit_(software)#History]( https://en.wikipedia.org/wiki/Gerrit_(software)#History)
* [6] [Gerrit quick intro - https://review.openstack.org/Documentation/intro-quick.html](https://review.openstack.org/Documentation/intro-quick.html)
* [7] [git-review tool - https://docs.openstack.org/infra/git-review/](https://docs.openstack.org/infra/git-review/)
* [8] [Zuul documentation - https://docs.openstack.org/infra/zuul/](https://docs.openstack.org/infra/zuul/)
