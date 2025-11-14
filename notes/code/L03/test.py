import unittest

if __name__ == "__main__":
    name = "l03.test_suite"
    suite = unittest.defaultTestLoader.loadTestsFromNames([name])
    result = unittest.TextTestRunner().run(suite)
