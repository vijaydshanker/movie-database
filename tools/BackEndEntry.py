#!/usr/bin/python
################################################################################
# Parser and undator from backend.

################################################################################
# Import Statements.

from core.Database import MovieDatabase
from core.MovieModel import MovieModel
from core.Constants import *

import os

################################################################################
class BackEndEntry:
    
    def __init__(self):
        self.moviedb = MovieDatabase()

    def doImport(self, location):


        if(os.path.exists(location)):
            print "Loading movies."                
            print "Directory Exists:"
            
            #load hindi movies
            self.load(location, "/hindi")
            
            #load english movie
            self.load(location, "/english")
        else:    
            print "Direcoty not found: " + str(location)

    def load(self, location, language):
        
        movieLocation = location + language
        
        if(os.path.exists(movieLocation)):
            for root, dirs, files in os.walk(movieLocation):
                for f in files:
                    parts = os.path.splitext(f)
                    
                    extention = parts[1]
                    if(self.isMovieFile(extention)):
                        movie = MovieModel()                                
                        movie.name = parts[0]
                        movie.status = Status.DOWNLOADED
                        movie.storage = Storage.MY_EXT_HARD_DISK
                        if(language == "/hindi"):
                            movie.spokenLanguage = SpokenLanguage.HINDI
                        elif(language == "/english"):
                            movie.spokenLanguage = SpokenLanguage.ENGLISH
                        
                        self.moviedb.addMovie(movie)


    def isMovieFile(self, extention):
        movieExtentions = [".avi", ".mkv"]
        
        for ext in movieExtentions:
            if(extention.lower() == ext.lower()):
                return True
    
BackEndEntry().doImport("/media/My Passport/home/ents/video/")
        
