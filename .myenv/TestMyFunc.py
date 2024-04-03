import unittest
import myFunc
import math


class Test_MyFunc(unittest.TestCase): # py testmyfunc.py -v
    def test_byteToTypeAndNumberOfChannel(self):
        self.assertEqual(myFunc.byteToTypeAndNumberOfChannel(0b00000100),'first channel - A/C')

    def test_TC11Message(self):
       self.assertEqual(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['n_lat_cpr'], 95454)
       self.assertEqual(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['n_lon_cpr'], 101614)
       self.assertEqual(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['format'], 1)
       self.assertEqual(math.floor(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['lat_cpr']*1000), 728)
       self.assertEqual(math.floor(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['lon_cpr']*1000), 775)
       self.assertEqual(math.floor(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['dlat']*10), 61)

    def test_pairOfMessages(self):
       self.assertEqual(myFunc.pairOfMessages(bytes([0x58,0xC3,0x82,0xD6,0x90,0xC8,0xAC]),1457996402,\
                                                    bytes([0x58,0xC3,0x86,0x43,0x5C,0xC4,0x12]),1457996400),(52.2572, 3.91937))

# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()