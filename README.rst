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
* Allen Guan
* `Bryan Patzke <https://github.com/bpatzke>`_
* Joeseph Richard

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
- What to install with pip (before you set up your virutal environment)

  - virtualenv
  - virtualenvwrapper (-win for windows)

- Set up your virtual environment.
- What to install with pip (after you set up your virtual environment)

  - pyDAL
  - sphinx
  - sphinx-bootstrap-theme

- web2py (if you clone the github respitory, delete the git stuff)

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

You should see someting like the second line. If you get an error, you can
download `pip`_ from `pypi`_.


Safety first
------------

Before we install the packages we'll need for the project, you should install
the virtualenv and virtualenvwrapper (the Windows version is called
virtuaenvwrapper-win) packages with pip. ::

  $ pip install virtualenv
  <lots of install information>
  $ pip install virtualenvwrapper
  <lots of install information>

Virtual environment -- as the name implies -- allows you to set up different
Python environments, each with its own set of packages installed.

Virtual environment wrapper hides the sometimes messy details of working with
virtualenv behind a much nicer user interface.


-------------------------------------
 Setting up your virtual environment
-------------------------------------

Now we can set up a virtual environment for working on the project.

.. rubric:: Footnotes

.. [1] web2py uses language features that were removed in Python 3.
.. [2] I recommend getting the `source <http://www.web2py.com/examples/static/web2py_src.zip>`_
       distribution.

       You can pull a copy from Github, but that complicates things with respect
       to source control. Since our working directory will be a sub-directory of
       web2py, you'll end up with web2py as your root project, and have to
       figure out how to work with our application as a sub-project.

       If you **do** pull the source from Github, just delete all of the .git*
       files in the web2py root directory. Then git won't recognize that as a
       repository anymore.


.. _web2py: https://web2py.com
.. _version 2.x: https://www.python.org/downloads/release/python-2710/
.. _git: http://git-scm.com/
.. _git-flow: https://github.com/nvie/gitflow
.. _pip: https://pypi.python.org/pypi/pip/
.. _pypi: https://pypi.python.org/pypi/
