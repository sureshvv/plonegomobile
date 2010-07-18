.. contents ::

Introduction
------------

``gomobile.imageinfo`` is abstraction layer to access image data in different Zope image objects. 
It takes in any image object or traversable path and returns Python Imaging Library object for it.
    
Supported different image objects include
    
* Skin layer images, both file system based and ZMI uploads
    
* Archetypes ATImage
    
* Resource folder images (static media)

* Images hosted on another server (http:// download)

This package is mainly used with Go Mobile for Plone project to dynamically resize images for mobile presentation,
regardless what kind of image there was in the source code. It is used to extract image width and height,
calculate proper mobile image size and then resize the image for that size on a second pass.

Usage
-----

See tests for code examples.

TODO
----

* Tests depends on ``gomobile.mobile`` presence

Source code
------------

Source code is available via Google Code.

* http://code.google.com/p/plonegomobile/source/browse/#svn/trunk/gomobile/gomobile.imageinfo

Beta software
-------------

This software is still in much development and aimed for advanced Python developers only.

Author
------

`mFabrik Research Oy <mailto:info@mfabrik.com>`_ - Python and Plone professionals for hire.

* `mFabrik web site <http://mfabrik.com>`_ 

* `mFabrik mobile site <http://mfabrik.mobi>`_ 

* `Blog <http://blog.mfabrik.com>`_

* `About Plone CMS <http://mfabrik.com/technology/technologies/content-management-cms/plone>`_ 



