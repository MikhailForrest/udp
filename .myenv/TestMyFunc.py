import unittest
import myFunc

class TestMyFunc(unittest.TestCase): # py testmyfunc.py -v
    def test_byteToTypeAndNumberOfChannel(self):
        self.assertEqual(myFunc.byteToTypeAndNumberOfChannel(0b00000100),'first channel - A/C')

# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()