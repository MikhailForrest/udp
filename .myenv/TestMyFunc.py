import unittest
import myFunc


class Test_MyFunc(unittest.TestCase): # py testmyfunc.py -v
    def test_byteToTypeAndNumberOfChannel(self):
        self.assertEqual(myFunc.byteToTypeAndNumberOfChannel(0b00000100),'first channel - A/C')

    def test_TC11Message(self):
       self.assertEqual(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['n_lat_cpr'], 95454)
       self.assertEqual(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['n_lon_cpr'], 101614)
       

# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()