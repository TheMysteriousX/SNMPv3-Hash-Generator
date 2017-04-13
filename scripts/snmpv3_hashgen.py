#! /usr/bin/env python3

import sys

if (sys.version_info < (3, 6)):
    print("Python 3.6 or higher is required, please see https://www.python.org/ or your OS package repository", file=sys.stderr)
    sys.exit(2)

import argparse
import json

from snmpv3_hashgen import Hashgen

parser = argparse.ArgumentParser(description='Convert an SNMPv3 auth or priv passphrase to sha1 or md5 hashes')
parser.add_argument('--auth', type=str, help='Authentication passphrase to be derived as utf8 string')
parser.add_argument('--priv', type=str, help='Privacy passphrase to be derived as utf8 string')
parser.add_argument('--engine', type=str, help='Engine ID as hex string')
parser.add_argument('--user', type=str, help='SNMPv3 USM username (default "observium")')
parser.add_argument('--mode', type=str, choices=['authpriv', 'auth', 'priv', 'none'],  help='SNMPv3 mode (default "authpriv")')
parser.add_argument('--hash', type=str, choices=['md5', 'sha1'],  help='Hash algorithm to use (default "sha1")')
parser.add_argument('--json', action='store_true', help='Emit output as json')

def format_esxi(user, Kul_auth, Kul_priv, mode, hash):
    if mode == "authpriv":
        return f"{user}/{hash(Kul_auth)}/{hash(Kul_priv)}/{mode}"
    elif mode == "auth":
        return f"{user}/{hash(Kul_auth)}/-/{mode}"
    elif mode == "priv":
        return f"{user}/-/{hash(Kul_priv)}/{mode}"
    else:
        return f"{user}/-/-/{mode}"

def main(*args, **kwargs):
    # Argument setup
    args = parser.parse_args()

    user = "observium" if not args.user else args.user
    mode = "authpriv" if not args.mode else args.mode
    auth = Hashgen.random_string() if not args.auth else args.auth
    priv = Hashgen.random_string() if not args.priv else args.priv
    engine = Hashgen.random_engine() if not args.engine else args.engine
    hash = Hashgen.sha1 if not args.hash else Hashgen.algs[args.hash]

    # Derive Kul from passphrases
    try:
        Kul_auth = Hashgen.derive_msg(auth, engine) if "auth" in mode else None
        Kul_priv = Hashgen.derive_msg(priv, engine) if "priv" in mode else None
    except ValueError as e:
        print("Error: Engine ID seems invalid; ensure that it is entered as a hex character string", file=sys.stderr)
        sys.exit(1)

    esxi = format_esxi(user, Kul_auth, Kul_priv, mode, hash)

    if args.json:
        print(json.dumps({
            'user': user,
            'engine': engine,
            'phrases': {
                'auth': auth if "auth" in mode else None,
                'priv': priv if "priv" in mode else None,
            },
            'hashes': {
                'auth': hash(Kul_auth) if "auth" in mode else None,
                'priv': hash(Kul_priv) if "priv" in mode else None,
            },
            'esxi': esxi,
        }))
    else:
        print(f"User: {user}")
        if "auth" in mode:
            print(f"Auth: {auth} / {hash(Kul_auth)}")
        if "priv" in mode:
            print(f"Priv: {priv} / {hash(Kul_priv)}")
        print(f"Engine: {engine}")
        print(f"ESXi USM String: {esxi}")

if __name__ == "__main__":
    main()
