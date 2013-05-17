webandgis
=========

A sample project to learn to build web based gis systems.

-------------------------
Installation instructions
-------------------------

In the root of the project, do:

```
 sudo pip install -e .
```

------------------
Inasafe workaround
------------------

If you have inasafe already installed in qgis, you can do the following to enable it's use from python scripts:

```
sudo ln -s ~/.qgis/python/plugins/inasafe/safe /usr/lib/python2.7/dist-packages/safe
```

-----------------------------
Optional softwares to install
-----------------------------

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