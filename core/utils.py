class StringUtils:
    """
    Contains convenient methods for operations on string objects
    """

    @staticmethod     
    def is_empty(value_to_check):
        value_to_check = str(value_to_check)
        empty = False
       
        if value_to_check is None:
            empty = True
        elif len(value_to_check.strip()) <= 0:
            empty = True

        return empty


################################################################################
# Tests
import unittest

class TestStringUtils(unittest.TestCase):

    def setUp(self):
        pass


    def test_is_empty(self):
        self.assertTrue(StringUtils.is_empty(""))
        self.assertTrue(StringUtils.is_empty(None))
        self.assertTrue(StringUtils.is_empty(" "))
        self.assertFalse(StringUtils.is_empty("Bob"))
        self.assertFalse(StringUtils.is_empty("  bob  "))


if __name__ == '__main__':
    unittest.main()

    
