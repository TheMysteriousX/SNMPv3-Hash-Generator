import unittest

from snmpv3_hashgen.hashgen import Hashgen

# flake8: noqa: E501


class TestLibrary(unittest.TestCase):
    kdf_maplesyrups = {
        "md5": "9faf3283884e92834ebc9847d8edd963",  # RFC 3413 §A.3.1
        "sha1": "9fb5cc0381497b3793528939ff788d5d79145211",  # RFC 3413 §A.3.2
        "sha224": "282a5867ee9aac639ad59df9572c7d3ac0fbc13a905b6df07dbbf00b",  #  Unverified
        "sha256": "ab51014d1e077f6017df2b12bee5f5aa72993177e9bb569c4dff5a4ca0b4afac",  # Unverified
        "sha384": "e06eccdf2c68a06ed034723c9c26e0db3b669e1e2efed49150b55377a2e98f383c86fb836857444654b287c93f51ff64",  # Unverified
        "sha512": "7e4396de5aadc77be853819b98c9406265b3a9c37cc3176569847a4e4f6fba63dd3a73d04924d31a63f95a601f9385af6be4ed1b37f87d040f7c6ed6f8d38a91",  # Unverified
    }

    final_maplesyrups = {
        "md5": "526f5eed9fcce26f8964c2930787d82b",  # RFC 3413 §A.3.1
        "sha1": "6695febc9288e36282235fc7151f128497b38f3f",  # RFC 3413 §A.3.2
        "sha224": "0bd8827c6e29f8065e08e09237f177e410f69b90e1782be682075674",  # Unverified
        "sha256": "8982e0e549e866db361a6b625d84cccc11162d453ee8ce3a6445c2d6776f0f8b",  # Unverified
        "sha384": "3b298f16164a11184279d5432bf169e2d2a48307de02b3d3f7e2b4f36eb6f0455a53689a3937eea07319a633d2ccba78",  # Unverified
        "sha512": "22a5a36cedfcc085807a128d7bc6c2382167ad6c0dbc5fdff856740f3d84c099ad1ea87a8db096714d9788bd544047c9021e4229ce27e4c0a69250adfcffbb0b",  # Unverified
    }

    test_string = "maplesyrup"
    engine_id = "000000000000000000000002"

    def test_kdf(self):
        for alg, fptr in Hashgen.algs.items():
            self.assertEqual(Hashgen.kdf(self.test_string, fptr).hex(), self.kdf_maplesyrups[alg])

    def test_concat(self):
        for alg, fptr in Hashgen.algs.items():
            self.assertEqual(Hashgen.derive_msg(self.test_string, self.engine_id, fptr).hex(), "".join([self.kdf_maplesyrups[alg], self.engine_id, self.kdf_maplesyrups[alg]]))

    def test_final(self):
        for alg, fptr in Hashgen.algs.items():
            self.assertEqual(fptr(Hashgen.derive_msg(self.test_string, self.engine_id, fptr)), self.final_maplesyrups[alg])
