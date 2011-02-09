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
           ...
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

For more information, see

* http://code.google.com/p/plonegomobile/source/browse/gomobile.docs/trunk/gomobile/docs/manual/developer-manual/theming.txt

After setting up buildout as instructed above, you can do::

        bin/paster create -t gomobile_theme src/gomobiletheme.mythemename


Author
------

`mFabrik Research Oy - Python and Plone professionals for hire. <http://mfabrik.com>`_

* `mFabrik Web & Mobile multichannel CMS solutions <http://webandmobile.mfabrik.com>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `More about Plone <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 

       
       
