**tcconfig**

.. contents:: Table of Contents
   :depth: 2

Summary
=========
A Simple tc command wrapper tool. Easy to set up traffic control of network bandwidth/latency/packet loss/packet-corruption to a network interface.

.. image:: https://badge.fury.io/py/tcconfig.svg
    :target: https://badge.fury.io/py/tcconfig

.. image:: https://img.shields.io/pypi/pyversions/tcconfig.svg
   :target: https://pypi.python.org/pypi/tcconfig

.. image:: https://travis-ci.org/thombashi/tcconfig.svg?branch=master
   :target: https://travis-ci.org/thombashi/tcconfig
   :alt: Linux CI test status

.. image:: https://img.shields.io/github/stars/thombashi/tcconfig.svg?style=social&label=Star
   :target: https://github.com/thombashi/tcconfig
   :alt: GitHub repository

Traffic control features
------------------------

Traffic shaping target
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Apply traffic shaping rules to specific targets:

- Outgoing/Incoming packets
- Source/Destination IP-address/network (IPv4/IPv6)
- Source/Destination ports

Moreover, exclude from shaping rules from specific targets:

- Source/Destination IP-address/network (IPv4/IPv6)
- Source/Destination ports

Available parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following parameters can set to network interfaces:

- Network bandwidth rate ``[G/M/K bps]``
- Network latency ``[microseconds/milliseconds/seconds/minutes]``
- Packet loss rate ``[%]``
- Packet corruption rate ``[%]``
- Packet duplicate rate ``[%]``
- Packet reordering rate  ``[%]``

.. image:: docs/gif/tcset_example.gif

Usage
=======
Set traffic control (``tcset`` command)
-----------------------------------------
``tcset`` is a command to add traffic control rule to a network interface (device).

e.g. Set a limit on bandwidth up to 100Kbps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

    # tcset eth0 --rate 100Kbps

e.g. Set network latency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can use time units (such as us/sec/min/etc.) to designate delay time.

Set 100 milliseconds network latency
'''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: console

    # tcset eth0 --delay 100ms

Set 10 seconds network latency
'''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: console

    # tcset eth0 --delay 10sec

Set 0.5 minutes (30 seconds) network latency
'''''''''''''''''''''''''''''''''''''''''''''''''''
.. code-block:: console

    # tcset eth0 --delay 0.5min

You can also use the following units:

- m/min/mins/minute/minutes
- s/sec/secs/second/seconds
- ms/msec/msecs/millisecond/milliseconds
- us/usec/usecs/microsecond/microseconds

e.g. Set 0.1% packet loss
^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

    # tcset eth0 --loss 0.1

e.g. All of the above settings at once
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

    # tcset eth0 --rate 100Kbps --delay 100ms --loss 0.1

e.g. Specify the IP address of traffic control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

    # tcset eth0 --delay 100ms --network 192.168.0.10

e.g. Specify the IP network and port of traffic control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

    # tcset eth0 --delay 100ms --network 192.168.0.0/24 --port 80

Delete traffic control (``tcdel`` command)
------------------------------------------
``tcdel`` is a command to delete traffic shaping rules from a network interface (device).

e.g. Delete traffic control of ``eth0``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can delete all of the shaping rules for the ``eth0`` with ``-a``/``--all`` option:

.. code-block:: console

    # tcdel eth0 --all

Display traffic control configurations (``tcshow`` command)
-----------------------------------------------------------
``tcshow`` is a command to display the current traffic control settings for network interface(s).

Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    # tcset eth0 --delay 10 --delay-distro 2  --loss 0.01 --rate 0.25M --network 192.168.0.10 --port 8080
    # tcset eth0 --delay 1 --loss 0.02 --rate 500K --direction incoming
    # tcshow eth0
    {
        "eth0": {
            "outgoing": {
                "dst-network=192.168.0.10/32, dst-port=8080": {
                    "delay": "10.0",
                    "loss": "0.01",
                    "rate": "250K",
                    "delay-distro": "2.0"
                },
                "dst-network=0.0.0.0/0": {}
            },
            "incoming": {
                "dst-network=0.0.0.0/0": {
                    "delay": "1.0",
                    "loss": "0.02",
                    "rate": "500K"
                }
            }
        }
    }

For more information
----------------------
More examples are available at 
http://tcconfig.rtfd.io/en/latest/pages/usage/index.html



Installation
============
Install via pip (recommended)
------------------------------
``tcconfig`` can be installed from `PyPI <https://pypi.python.org/pypi>`__ via
`pip <https://pip.pypa.io/en/stable/installing/>`__ (Python package manager) command.

.. code:: console

    sudo pip install tcconfig


Install in Debian/Ubuntu from a deb package
--------------------------------------------
#. ``wget https://github.com/thombashi/tcconfig/releases/download/<version>/tcconfig_<version>_amd64.deb``
#. ``dpkg -iv tcconfig_<version>_amd64.deb``

:Example:
    .. code:: console

        $ wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
        $ sudo dpkg -i tcconfig_0.19.0_amd64.deb


Dependencies
============
Python 2.7+ or 3.4+

Linux packages
--------------
- mandatory: required for ``tc`` command:
    - `Ubuntu`/`Debian`: ``iproute2``
    - `Fedora`/`RHEL`: ``iproute-tc``
- optional: required to when you use ``--iptables`` option:
    - ``iptables``

Linux kernel module
----------------------------
- ``sch_netem``

Python packages
---------------
Dependency python packages are automatically installed during
``tcconfig`` installation via pip.

- `DataPropery <https://github.com/thombashi/DataProperty>`__
- `ipaddress <https://pypi.python.org/pypi/ipaddress>`__
- `logbook <http://logbook.readthedocs.io/en/stable/>`__
- `msgfy <https://github.com/thombashi/msgfy>`__
- `pyparsing <https://pyparsing.wikispaces.com/>`__
- `six <https://pypi.python.org/pypi/six/>`__
- `subprocrunner <https://github.com/thombashi/subprocrunner>`__
- `typepy <https://github.com/thombashi/typepy>`__
- `voluptuous <https://github.com/alecthomas/voluptuous>`__

Optional Python packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `netifaces <https://github.com/al45tair/netifaces>`__
    - Suppress excessive error messages if this package installed

Test dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- `allpairspy <https://github.com/thombashi/allpairspy>`__
- `pingparsing <https://github.com/thombashi/pingparsing>`__
- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__

Documentation
===============
http://tcconfig.rtfd.io/

Troubleshooting
=================
http://tcconfig.readthedocs.io/en/latest/pages/troubleshooting.html

