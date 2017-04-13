A script to generate SNMPv3 keys as detailed by rfc3414 (passphrases
expanded with a kdf, then hashed with the engine id). All key generation
is done using the new cryptographically secure *secrets* library.

As I wrote this with ESXi in mind, it also emits a string suitable for
configuring the SNMP daemon via esxcli/PowerCLI, but the hashes are
standard and compatible with other SNMPv3 implementations.

With no arguments, it will generate an authentication and privacy
passphrase with associated random engine ID in text form. *--json* will
format the output as json.

The script is fully idempotent; if you take the parameters it generates
randomly and re-enter them, you will get the same output a second time.

Dependencies
============

Runtime: Python 3.6 or greater.

Sample Output
=============

Standard
--------

::

    User: observium
    Auth: gaYA82XVtNaf3WLwRgoIs544ghP6f80S / f78359764ca382922fa382cf884e588031de575a
    Priv: H5XEtRpxXVaGzXU5i2rFwPnYGr8SEzTp / 31a001a56a225fdfc1916bd60190405a1aa22ff0
    Engine: 7ae1b0ff0aa2f3950566d3de2274d05a
    ESXi USM String: observium/f78359764ca382922fa382cf884e588031de575a/31a001a56a225fdfc1916bd60190405a1aa22ff0/authpriv

JSON
----

::

    {
      "user": "observium",
      "engine": "b2a50167b7c8512ddfc9d5765a3490af",
      "phrases": {
        "auth": "71rOhjfj6QVSy2mw5tBo7PueZ8KWSv60",
        "priv": "xwsvzht8NEcuwAlEpUKzMxKFWeH72sK9"
      },
      "hashes": {
        "auth": "fa0d5249293404502f9953b9514d0636a96c2cbc",
        "priv": "cccbdcfa603817df340514ecc22dfae8c4c412e8"
      },
      "esxi": "observium/fa0d5249293404502f9953b9514d0636a96c2cbc/cccbdcfa603817df340514ecc22dfae8c4c412e8/authpriv"}

It should go without saying, but **DO NOT** use the engine id or
passphrases in the samples.

Usage
=====

::

    usage: snmpv3-hashgen [-h] [--auth AUTH] [--priv PRIV] [--engine ENGINE]
                          [--user USER] [--mode {authpriv,auth,priv,none}]
                          [--hash {md5,sha1}] [--json]

    Convert an SNMPv3 auth or priv passphrase to sha1 or md5 hashes

    optional arguments:
      -h, --help            show this help message and exit
      --auth AUTH           Authentication passphrase to be derived as a string
      --priv PRIV           Privacy passphrase to be derived as a string
      --engine ENGINE       Engine ID as hex string
      --user USER           SNMPv3 USM username (default "observium")
      --mode {authpriv,auth,priv,none}
                            SNMPv3 mode (default "authpriv")
      --hash {md5,sha1}     Hash algorithm to use (default "sha1")
      --json                Emit output as json
