webandgis
=========

A sample project to learn to build web based gis systems.

[![Build Status](https://travis-ci.org/ingenieroariel/webandgis.png?branch=master)](https://travis-ci.org/ingenieroariel/webandgis)

-------------------------
Installation instructions
-------------------------

Before installing, you need to install the Geospatial Data Abstraction Library (GDAL), in Ubuntu, you can do the following::

```
sudo apt-get install gdal-bin
```

After that, you just need to install webgis, in the root of the project, do:

```
 sudo pip install -e .
```

This will install Django, Inasafe (python-safe) and any other dependencies.


Then, you need to create a local database and run the server:

```
python manage.py syncdb
python manage.py runserver
```

And navigate to: http://localhost:8000/


-----
Other
-----

Optional software to install:

1. Sublime-text : Makes editing of codes/files easier

```
sudo add-apt-repository ppa:webupd8team/sublime-text-2
sudo apt-get update
sudo apt-get install sublime-text-2-dev
```

2. Git-gui

```
sudo apt-get install git-gui
```
