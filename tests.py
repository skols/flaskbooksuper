import os, sys
import unittest
from user.tests import UserTest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if __name__ == "__main__":
    unittest.main()
