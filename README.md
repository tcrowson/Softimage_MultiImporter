Softimage_MultiImporter
=======================


This addon was created as a test for using PyQt in Softimage. It essentially wraps native import commands into a single Qt interface, allowing you to import multple 3D formats at once.

___
*INSTALLATION for Softimage 2014*
- Download and install [PyQt](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10.3/PyQt4-4.10.3-gpl-Py2.7-Qt4.8.5-x64.exe/download ) to a location that can be access by the Softimage Python interpreter. If you're doing this locally on your personal machine, installing PyQt to your system Python should be sufficient. However, you can install it anywhere as long as your PYTHONPATH environment variable has been edited to include the path to PyQt. At launch, Softimage will load all modules referenced by PYTHONPATH.
- Install [PyQtForSoftimage](https://github.com/caron/PyQtForSoftimage)
- Restart Softimage
- ownload the zip of this repo and install 'MultiImporter.xsiaddon'.

___
*INSTALLATION for Softimage 2013 and earlier*
- Install [Python](http://www.python.org/download/releases/2.7.3/), preferably 2.7.3, but 2.6.x. should work as well.
- Install [PyWin32 217](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20217/)
- Download and install [PyQt](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10.3/PyQt4-4.10.3-gpl-Py2.7-Qt4.8.5-x64.exe/download ) to a location that can be access by the Softimage Python interpreter. If you're doing this locally on your personal machine, installing PyQt to your system Python should be sufficient. However, you can install it anywhere as long as your PYTHONPATH environment variable has been edited to include the path to PyQt. At launch, Softimage will load all modules referenced by PYTHONPATH.
- In Softimage, uncheck "Use Python Installed with Softimage (Windows Only)" from the Scripting preferences.
- Install [PyQtForSoftimage](https://github.com/caron/PyQtForSoftimage)
- Restart Softimage
- Download the zip of this repo and install 'MultiImporter.xsiaddon'.
