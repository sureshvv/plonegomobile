plonecommunity.mobi is a demo site for Plone GoMobile product. It aggregates Plone community content for mobile site.

Strategy
--------

Feedburner is used to expose various Plone related feeds

Exposes feeds:

* *news* http://feeds.plone.org/plonenews
 
* *releases* http://feeds.plone.org/plonereleases http://feeds.plone.org/ploneaddons

* *blogs* http://feeds.plone.org/ploneblogs

* *forums* 

	* plone-users: http://n2.nabble.com/General-Questions-f293352.xml
	
	* add-on product developers: http://n2.nabble.com/Product-Developers-f293354.xml
	
* *Twitter* http://search.twitter.com/search.atom?q=%23plone

* *Events* http://feeds.plone.org/ploneevents

Configuration
-------------

SVN checkout w/Google code authentication::

	cd src
	svn co https://plonegomobile.googlecode.com/svn/trunk/gomobile gomobile
	svn co https://mobilesniffer.googlecode.com/svn/trunk/mobile.sniffer mobile.sniffer
	
Symlink config/buildout.cfg for yourself::

	cd ..
	ln -s src/gomobile/plonecommunity.mobi/config/buildout.cfg .
	bin/buildout



