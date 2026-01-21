import unittest

if __name__ == "__main__":
    name = "a1q2c.test_suite"
    suite = unittest.defaultTestLoader.loadTestsFromNames([name])
    result = unittest.TextTestRunner().run(suite)
