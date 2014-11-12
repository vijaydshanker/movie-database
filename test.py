#!/usr/bin/python

import unittest
from test.repositorytest import TestMovieRepository

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMovieRepository)
    unittest.TextTestRunner(verbosity=2).run(suite)    

if __name__ == '__main__':
    main()
