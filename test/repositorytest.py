#import statements
from core.repository import MovieRepository
import unittest

class TestMovieRepository(unittest.TestCase):

    def setUp(self):
        self.repository = MovieRepository()

    def test_findMovieByName(self):
        model = self.repository.findMovieByName("Test")
        
        print(model)
