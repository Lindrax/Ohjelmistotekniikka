import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)
    
    def test_saldon_lataus(self):
        self.maksukortti.lataa_rahaa(100)

        self.assertEqual(self.maksukortti.saldo_euroina(), 11)
    
    def test_ota_rahaa(self):
        self.maksukortti.ota_rahaa(100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 9)

    def test_ota_rahaa_liikaa(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)
    
    def test_true(self):
        b = self.maksukortti.ota_rahaa(100)
        self.assertEqual(b, True)

    def test_false(self):
        b = self.maksukortti.ota_rahaa(10000)
        self.assertEqual(b, False)
    
    def test_str(self):
        print(self.maksukortti)
        self.assertEqual( str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")






### Kortin saldo alussa oikein
#Rahan lataaminen kasvattaa saldoa oikein
#Rahan ottaminen toimii:
#Saldo vähenee oikein, jos rahaa on tarpeeksi
#Saldo ei muutu, jos rahaa ei ole tarpeeksi
#etodi palauttaa True, jos rahat riittivät ja muuten False
