This is mobile equivalent for `Plone Twinapex Theme <http://plone.org/products/twinapex-theme>`_ product.

This also servers as example how to build your own mobile themes for Plone Go Mobile.

Changes
-------

This section describes how Twinapex theme modifies Plone Go Mobile default theme

* Override static resources (CSS/images) with Twinapex specific. This is just copy-paste
  from gomobiletheme.basic/static folder. CSS was hand-modified and images were replaced.

* Override logo viewlet to use Twinapex logo

* Override head viewlet to load Twinapex media

* Add new "header image" viewlet which renders the dynamic header image as set in plonetheme.twinapex

* Override Document and Folder renderers with Twinapex specific. They will place header image
  to the page if available.

* tests.py is copied from gomobiletheme.basic. Theme name specific parts are changed.
  Tests for header animation have been added.

Author
------

`Twinapex Team <mailto:info@twinapex.com>`_ - Python and Plone professionals for hire.

* `Twinapex company site <http://www.twinapex.com>`_ (`Twinapex-yritysryhm� <http://www.twinapex.fi>`_)

* `Twinapex company blog <http://blog.twinapex.fi>`_

* `Twinapex mobile site <http://www.twinapex.mobi>`_

* `More about Plone <http://www.twinapex.com/products/plone>`_ (`Lis�tietoa Plone-julkaisuj�rjestelm�st� <http://www.twinapex.fi/tuotteet/plone>`_)

* `Other open source Plone products by Twinapex <http://www.twinapex.com/for-developers/open-source/for-plone>`_




