Introduction
------------

This Python package provides `plonecommunity.mobi site <http://plonecommunity.mobi>`_.
plonecommunity.mobi is a demo site for `Go Mobile for Plone <http://webandmobile.mfabrik.com>`_ product. 
It aggregates Plone community content for mobile site.

Strategy
--------

Feedburner is used to expose various Plone related feeds

Exposes feeds:

* news http://feeds.plone.org/plonenews
 
* releases http://feeds.plone.org/plonereleases http://feeds.plone.org/ploneaddons

* blogs http://feeds.plone.org/ploneblogs

* *forums* 

	* forums/general-discussion http://n2.nabble.com/General-Questions-f293352.xml
	
	* forums/add-on-product-developers http://n2.nabble.com/Product-Developers-f293354.xml
	
* twitter http://search.twitter.com/search.atom?q=%23plone

* *Events* http://feeds.plone.org/ploneevents

Configuration
-------------

SVN checkout w/Google code authentication::

	cd src
	svn co https://plonegomobile.googlecode.com/svn/trunk/gomobile gomobile
	svn co https://mobilesniffer.googlecode.com/svn/trunk/mobile.sniffer mobile.sniffer
	svn co https://svn.plone.org/svn/collective/collective.templateengines/trunk collective.templateengines
	svn co https://svn.plone.org/svn/collective/collective.easytemplate/trunk collective.easytemplate
	
Symlink config/buildout.cfg for yourself::

	cd ..
	ln -s src/gomobile/plonecommunity.mobi/config/buildout.cfg .
	bin/buildout


Author
------

`mFabrik Research Oy <mailto:research@mfabrik.com>`_ - Python and Plone professionals for hire.

* `Web and mobile project - mobilize your Plone site in an instant <http://webandmobile.mfabrik.com>`_

* `mFabrik web site <http://mfabrik.com>`_ 

* `mFabrik mobile site <http://mfabrik.mobi>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 



