Introduction
-------------

This package provides different code templates to customize and extend
`mFabrik Web & Mobile CMS <http://webandmobile.mfabrik.com>`_.

Please get familiar with Python paster templates and 
paster local commands to use these facilities.

Usage
-----

Include paster in buildout and include this egg as related to paster::

	[buildout]
	parts =
	   paster
	
	[paster]
	eggs = zc.recipe.egg
	eggs =
	   ZopeSkel
	   PasteScript
	   PasteDeploy
	   gomobile.templates
	   ${buildout:eggs}
	entry-points = paster=paste.script.command:run 

Templates
---------

gomobile_theme
==============

Create easily a code skeleton for your own theme.

Author
------

`mFabrik Research Oy <mailto:info@mfabrik.com>`_ - Python and Plone professionals for hire.

* `mFabrik Web & Mobile multichannel CMS solutions <http://webandmobile.mfabrik.com>`_ 

* `mFabrik web site <http://mfabrik.com>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 

       
       
