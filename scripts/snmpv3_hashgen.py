#! /usr/bin/env python3

import sys

if sys.version_info < (3, 6):
    print("Python 3.6 or higher is required, please see https://www.python.org/ or your OS package repository", file=sys.stderr)
    sys.exit(2)

import argparse
import json

from snmpv3_hashgen import Hashgen

help_text = """
Convert an SNMPv3 auth or priv passphrase to hashes.
"""

epilog_text = """
RFC 7630 defines no test data for sha[2-9]{3} - these should be considered experimental.
Report bugs at https://github.com/TheMysteriousX/SNMPv3-Hash-Generator/issues
"""

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=help_text, epilog=epilog_text,)
parser.add_argument("--auth", type=str, help="Authentication passphrase to be derived as utf8 string")
parser.add_argument("--priv", type=str, help="Privacy passphrase to be derived as utf8 string")
parser.add_argument("--engine", type=str, help="Engine ID as hex string")
parser.add_argument("--user", type=str, help='SNMPv3 USM username (default "librenms")')
parser.add_argument("--mode", type=str, choices=["auth", "priv", "none"], help='SNMPv3 mode (default "priv")')
parser.add_argument("--hash", type=str, choices=["md5", "sha1", "sha224", "sha256", "sha384", "sha512"], help='Hash algorithm to use (default "sha1")')

fmt = parser.add_mutually_exclusive_group()
fmt.add_argument("--json", action="store_true", help="Emit output as json")
fmt.add_argument("--yaml", action="store_true", help="Emit output as yaml")
fmt.add_argument("--toml", action="store_true", help="Emit output as toml")


def format_esxi(user, Kul_auth, Kul_priv, mode, hash):
    if mode == "priv":
        return f"{user}/{hash(Kul_auth)}/{hash(Kul_priv)}/{mode}"
    elif mode == "auth":
        return f"{user}/{hash(Kul_auth)}/-/{mode}"
    else:
        return f"{user}/-/-/{mode}"

def format_sros(user, Kul_auth, Kul_priv, mode, hash):
    hashmode = "sha" if hash.keywords['name'] == "sha1" else hash.keywords['name']

    if mode == "priv" and (hashmode == "sha" or hashmode == "md5"):
        return f"configure system security user {user} snmp authentication {hashmode} {hash(Kul_auth)} privacy aes-128-cfb-key {hash(Kul_priv)}"
    elif mode == "auth" and (hashmode == "sha" or hashmode == "md5"):
        return f"configure system security user {user} snmp authentication {hashmode} {hash(Kul_auth)}"
    else:
        return f"unsupported hash algorithm"

def main(*args, **kwargs):
    # Argument setup
    args = parser.parse_args()

    if args.priv and not args.auth:
        print("Error: privacy passphrase supplied without auth passphrase", file=sys.stderr)
        sys.exit(3)

    user = "librenms" if not args.user else args.user
    mode = "priv" if not args.mode else args.mode
    auth = Hashgen.random_string() if not args.auth else args.auth
    priv = Hashgen.random_string() if not args.priv else args.priv
    engine = Hashgen.random_engine() if not args.engine else args.engine
    hash = Hashgen.algs["sha1"] if not args.hash else Hashgen.algs[args.hash]

    # Derive Kul from passphrases
    try:
        Kul_auth = Hashgen.derive_msg(auth, engine, hash) if "none" not in mode else None
        Kul_priv = Hashgen.derive_msg(priv, engine, hash) if "priv" in mode else None
    except ValueError:
        print("Error: Engine ID seems invalid; ensure that it is entered as a hex character string", file=sys.stderr)
        sys.exit(1)

    esxi = format_esxi(user, Kul_auth, Kul_priv, mode, hash)
    sros = format_sros(user, Kul_auth, Kul_priv, mode, hash)
    output = {
        "user": user,
        "engine": engine,
        "phrases": {"auth": auth if "none" not in mode else None, "priv": priv if "priv" in mode else None},
        "hashes": {"auth": hash(Kul_auth) if "auth" in mode or "priv" in mode else None, "priv": hash(Kul_priv) if "priv" in mode else None},
        "esxi": esxi,
        "sros": sros
    }

    if args.json:
        print(json.dumps(output))
    elif args.yaml:
        try:
            import yaml

            print(yaml.dump({"snmpv3": output}, explicit_start=True))
        except ImportError:
            print("YAML output requires a YAML library")
            print("Try running pip3 install PyYAML")
            sys.exit(4)
    elif args.toml:
        try:
            import toml

            print(toml.dumps(output))
        except ImportError:
            print("TOML output requires a TOML library")
            print("Try running pip3 install toml")
            sys.exit(5)
    else:
        print(f"User: {user}")
        if "none" not in mode:
            print(f"Auth: {auth} / {hash(Kul_auth)}")
        if "priv" in mode:
            print(f"Priv: {priv} / {hash(Kul_priv)}")
        print(f"Engine: {engine}")
        print(f"ESXi USM String: {esxi}")
        print(f"SR-OS Config: {sros}")


if __name__ == "__main__":
    main()
