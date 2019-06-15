import unittest

from src.cheaserDecrypt import decrypt
from src.cheaserEncrypt import encrypt
import src.rsa as rsa

decrypted = "Pijamalı hasta yağız şoföre çabucak güvendi."
cheaser_encrypted = {
    9: "Wqrhthşp öhzbh ghopğ aümvyl jhıcihs nçdlukq.",
    29: "Nğhxjxig fxprx vxegw qlçmöc axyszxı dştckbğ.",
    50: "Fxzöcöbw vöhiö oöüwö ıdteğş röpjqöa uklşçsx."
}
cheaser_encryption_numbers = [9, 29, 50]

rsa_arguments = {
    "encrypted": "10540899063307850109078506530211063706850785082801180785063711770785061702110793063700981145042703020841072206370902078509670259050607850926063706980747033207220110054008990282",
    "n": 1199,
    "e": 467,
    "d": 1043
}

class TestMethods(unittest.TestCase):
    def test_cheaserEncrypt(self):
        for i in cheaser_encryption_numbers:
            self.assertEqual(encrypt(decrypted, i), cheaser_encrypted[i], "Sezar şifreleme {0} numarada başarısız oldu.".format(i))
    
    def test_cheaserDecrypt(self):
        for i in cheaser_encrypted:
            self.assertEqual(decrypt(cheaser_encrypted[i], i), decrypted, "Sezar şifre çözme {0} numarada başarısız oldu.".format(i))
    
    def test_rsaEncryption(self):
        result = list(rsa.Sifrele(decrypted))

        self.encrypted = result[0]

        self.n = result[1]
        self.e = result[2]
        self.d = result[3]

        self.assertEqual(rsa.SifreCoz(self.encrypted, self.n, self.e, self.d), decrypted, "RSA şifreleme başarısız oldu.")
    
    def test_rsaDecryption(self):
        self.assertEqual(rsa.SifreCoz(rsa_arguments["encrypted"], rsa_arguments["n"], rsa_arguments["e"], rsa_arguments["d"]), decrypted, "RSA şifre çözme başarısız oldu.")

if __name__ == "__main__":
    unittest.main()