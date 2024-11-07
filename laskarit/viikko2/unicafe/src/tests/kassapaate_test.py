import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti 

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(500)  

    def test_init(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_edullinen_cash(self):
        change = self.kassa.syo_edullisesti_kateisella(300)
        self.assertEqual(change, 60)  
        self.assertEqual(self.kassa.kassassa_rahaa, 100240)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_edullinen_cash_false(self):
        change = self.kassa.syo_edullisesti_kateisella(200)
        self.assertEqual(change, 200) 
        self.assertEqual(self.kassa.kassassa_rahaa, 100000) 
        self.assertEqual(self.kassa.edulliset, 0)

    def test_maukas_cash(self):
        change = self.kassa.syo_maukkaasti_kateisella(500)
        self.assertEqual(change, 100) 
        self.assertEqual(self.kassa.kassassa_rahaa, 100400)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_maukas_cash_false(self):
        change = self.kassa.syo_maukkaasti_kateisella(350)
        self.assertEqual(change, 350)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000) 
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_edullinen(self):
        result = self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertTrue(result)
        self.assertEqual(self.kortti.saldo, 260) 
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_edullinen_false(self):
        kortti = Maksukortti(200) 
        result = self.kassa.syo_edullisesti_kortilla(kortti)
        self.assertFalse(result)
        self.assertEqual(kortti.saldo, 200) 

    def test_maukas(self):
        result = self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertTrue(result)
        self.assertEqual(self.kortti.saldo, 100) 
        self.assertEqual(self.kassa.maukkaat, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_maukas_false(self):
        kortti = Maksukortti(200) 
        result = self.kassa.syo_maukkaasti_kortilla(kortti)
        self.assertFalse(result)
        self.assertEqual(kortti.saldo, 200) 

    def test_lataus(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 1000)
        self.assertEqual(self.kortti.saldo, 1500)  
        self.assertEqual(self.kassa.kassassa_rahaa, 101000) 

    def test_lataa_rahaa_kortille_negative_amount(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kortti.saldo, 500)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000) 
    
    def test_euroina(self):
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)
