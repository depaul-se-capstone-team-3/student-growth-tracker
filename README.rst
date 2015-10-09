.. This is the README file for the github project. It should also be included in
   the documentation.


========================
 Student Growth Tracker
========================

.. rubric:: *Add the mission statement here*

Student Growth Tracker is an enhanced gradebook application that allows educators
to track and monitor students' progress with respect to the Common Core standards.


About
=====

Student Growth Tracker is a `web2py`_ application.


Authors
=======


* Lawrence Graves
* `Allan Guan <https://github.com/forevaufo>`_
* `Bryan Patzke <https://github.com/bpatzke>`_
* Joesph Richard

.. _setup_tutorial:


Environment Setup Tutorial
==========================

Write up a brief tutorial on how to set up the environment to work on web2py.
(Can I make this a video?) It should include the following:

- git (if you don't have it) Make sure it has the command-line tools.
- git flow (On Mac you can install with MacPorts, or another package
  manager.)
- Download and install python (probably just a link to the documentation)
- Using pip
- What to install with pip (before you set up your virtual environment)

  - virtualenv
  - virtualenvwrapper (-win for windows)

- Set up your virtual environment.
- What to install with pip (after you set up your virtual environment)

  - pyDAL
  - sphinx
  - sphinx-bootstrap-theme

- web2py (if you clone the github repository, delete the git stuff)

---------------------------
 What you'll need (Part 1)
---------------------------

These are the tools you'll need to work on web2py applications. The list isn't
comprehensive, but it will give you what you need to get started.

- Python (`version 2.x`_ - the latest is Python 2.7.10)\ [1]_
- `git`_
- `git-flow`_
- `web2py`_\ [2]_


---------------------------
 What you'll need (Part 2)
---------------------------

Once you get Python, git, and git-flow installed, You'll need to install a few
extra pieces -- some to make your life easier, and some for the project.


pip
---

Pip is a package manager for Python. If you need something that doesn't come
with Python, you'll use pip to install it. To make sure you have pip installed,
just type the following at the command prompt: ::

  $ pip --version
  pip 7.1.0 from /path/to/pip/directory (python 2.7)

You should see something like the second line. If you get an error, you can
download `pip`_ from `pypi`_.


Safety first
------------

Before we install the packages we'll need for the project, you should install
the `virtualenv`_ and `virtualenvwrapper`_ (the Windows version is called
`virtuaenvwrapper-win`_) packages with pip. ::

  $ pip install virtualenv
  <lots of install information>

  $ pip install virtualenvwrapper
  <lots of install information>

Virtual environment -- as the name implies -- allows you to set up isolated
Python environments, each with its own set of packages installed. The
`documentation <https://virtualenv.pypa.io/en/latest/>`_ for virtualenv can give
you all the gory details, but it's probably best to leave that for another time.

Virtual environment wrapper hides the sometimes messy details of working with
virtualenv behind a much nicer user interface. Both `virtualenvwrapper
<http://virtualenvwrapper.readthedocs.org/en/latest/>`_ and `virtualenvwrapper-win
<https://pypi.python.org/pypi/virtualenvwrapper-win>`_ have good introductions,
so your best bet for getting started is to follow the appropriate link for your
version.


-------------------------------------
 Setting up your virtual environment
-------------------------------------

Now we can set up a virtual environment for working on the project. I chose to
call my virtual environment ``capstone`` as it's descriptive enough and short.
It doesn't matter what you name it -- we don't all have to use the same name as
the virtual environment is strictly a local tool -- so choose a name that you'll
remember. Since web2py requires python2, we need to make sure that our virtualenv
uses python2 instead of python3. To create the ``capstone`` environment, type::

  $ mkvirtualenv -p /path/to/python2 capstone

OR::

  $ mkvirtualenv --python=/path/to/python2 capstone
  ...
  <lots of output>

If python2 is the default version of python -- or the only version -- then you
don't need to specify it in the ``mkvirtualenv`` command.

Once you issue the command, your prompt should look something like this::

  (capstone) $ _

The ``(capstone)`` prefix on your prompt tells you what environment you're using
at the moment. To exit the virtual environment, just type::

  (capstone) $ deactivate

To work in the ``capstone`` environment, type::

  $ workon capstone

Working with virtual environments takes some getting used to, but ultimately it
can save the time wasted on chasing bugs related to library versions, and other
dependency issues. Essentially, it lets you freeze your python environment to
protect it from interference.


-------------------
 Finishing Touches
-------------------

There are only a few more things that need to be installed so we can get started.
You'll use pip to install all of them. Don't forget to make sure that you have
your ``virtualenv`` activated -- as indicated by the ``(env-name)`` tag in front
of your command prompt. If it's not, just use the ``workon env-name`` command
to activate the environment.

pyDAL
-----

`pyDAL`_ is the Python Database Abstraction Layer. pyDAL makes the web2py
framework database agnostic. It provides an object-oriented framework for
building and working with your data models. It transparently transforms your
method calls into database commands, and returns results as python objects.

To install pyDAL, type::

  (capstone) $ pip install pyDAL

Sphinx
------

`Sphinx`_ is a documentation tool that makes creating documentation nearly
effortless. As long as your code has `docstrings`_ -- they're the python version
of java doc comments -- for all of your public interface items, Sphinx can use
them to build the documentation for the project automatically. It can also run
tests and check the documentation coverage of your code.

To install sphinx, type::

  (capstone) $ pip install pyDAL

sphinx-bootstrap-theme
----------------------

While this isn't strictly necessary, this theme provides support for the
`bootstrap`_ UI framework. This is important since web2py uses `bootstrap`_ as
well, which means we'll have a consistent user interface between the application
and the documentation.

To install sphinx-bootstrap-theme, type::

  (capstone) $ pip install pyDAL


------------------------
 Set up the application
------------------------

Once you've downloaded the `source`_ version of web2py\ [2]_, unzip it to a
convenient location. Poke around a little bit to see what's what. Almost all of
the built-in functionality of the framework is in the gluon\ [3] directory. We
won't ever have to touch anything in the gluon directory.

All of our code will go into a subdirectory of the applications directory named
student-growth-tracker. This will also be the root of your git repository, but
we'll get to that shortly. To start web2py, all you have to do is type::

  /path/to/web2py $ python web2py.py

Enter an admin password -- it's only used for this session, so feel free to make
it something really simple -- and -- if your browser doesn't open the Welcome
application automatically -- open your favorite browser and go to
``http://127.0.0.1:8000``.

The `overview`_ chapter in the `web2py documentation`_ provides a good
introduction to working with web2py. It covers what I did here, but in more
detail. It also walks you through creating a basic application, and working with
some of the features of the framework. I suggest you go through this introduction
before moving on with the rest of the setup.

-----------------------------
 Working with git and Github
-----------------------------

You're almost ready to start working on the application, but you have a few final
steps first.

Fork the master repository
--------------------------

.. topic:: A word of caution...

           No one should ever work directly with the ``master`` repository.
           Code is only merged into ``master`` once it has been thoroughly
           tested and vetted.

           It's also probably a good idea to have one person responsible for
           merging pull requests to ``master``. While we all have ``push`` access
           to the ``master`` repository, it should be used with caution. Unless
           it's necessary to do a push, create a pull request instead.

You should make a fork of the ``master`` repository in your personal account.
All you need to do is go to the `project page`_ and click the ``Fork`` button on
the right-hand side, near the top of the page. Github will show you an animation
while it copies things over, and then you'll be take to your own shiny new copy
of the student-growth-tracker repository.

.. topic:: Branches

           In keeping with the `git-flow`_ branching model, there are two main
           branches in the project -- ``master`` and ``develop``. Right now
           (2015-10-01) they two branches are in sync. All of the work will be
           done on the ``develop`` branch, or a ``feature`` branch from
           ``develop``. The ``master`` branch is only for released code. The
           only exception to that rule is right now as we're getting started
           since you **have to** have a ``master`` branch on Github, so I needed
           to put something there.


Get your copy
-------------

You need to clone your Github repository to your local system. First, navigate
to the ``web2py/applications`` directory. Then, type::

  (capstone) $ git clone https://github.com/<username>/student-growth-tracker.git

Where ``<username`` is your Github user name. You should see something like::

  Cloning into 'student-growth-tracker'...
  remote: Counting objects: 115, done.
  remote: Compressing objects: 100% (92/92), done.
  Receiving objects:  85% (98/115)
  Receiving objects: 100% (115/115), 998.58 KiB | 0 bytes/s, done.
  Resolving deltas: 100% (16/16), done.
  Checking connectivity... done.

You should now have a directory named ``student-growth-tracker`` in your
applications directory.

If you start web2py, the application should be ready for use. You'll have to go
to the admin interface, or go to ``http://127.0.0.1:8000/student-growth-tracker``.


------------
 Next Steps
------------

That should get you going. I'll add more as I think of it.


.. rubric:: Footnotes

.. [1] web2py uses language features that were removed in Python 3.
.. [2] I recommend getting the `source`_ distribution.

       You can pull a copy from Github, but that complicates things with respect
       to source control. Since our working directory will be a sub-directory of
       web2py, you'll end up with web2py as your root project, and have to
       figure out how to work with our application as a sub-project.

       If you **do** pull the source from Github, just delete all of the .git*
       files in the web2py root directory. Then git won't recognize that as a
       repository anymore.
.. [3] Massimo DiPierro -- the creator of web2py and a professor at DePaul --
       took his PhD in high energy physics. My guess is that's why he named the
       core "gluon" -- because it forms the basic building blocks of the
       framework.

.. _web2py: https://web2py.com
.. _version 2.x: https://www.python.org/downloads/release/python-2710/
.. _git: http://git-scm.com/
.. _git-flow: https://github.com/nvie/gitflow
.. _pip: https://pypi.python.org/pypi/pip/
.. _pypi: https://pypi.python.org/pypi/
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: https://pypi.python.org/pypi/virtualenvwrapper
.. _virtualenvwrapper-win: https://pypi.python.org/pypi/virtualenvwrapper-win
.. _pyDAL: https://github.com/web2py/pydal
.. _Sphinx: http://sphinx-doc.org/
.. _docstrings: https://www.python.org/dev/peps/pep-0287/
.. _bootstrap: http://getbootstrap.com/
.. _source: http://www.web2py.com/examples/static/web2py_src.zip
.. _overview: http://web2py.com/books/default/chapter/29/03/overview
.. _web2py documentation: http://web2py.com/book
.. _project page: https://github.com/depaul-se-capstone-team-3/student-growth-tracker
