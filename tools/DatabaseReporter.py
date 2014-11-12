from core.Database import MovieDatabase
from core.MovieModel import MovieModel

columnFormat = "{:^5}|{:^20}|{:^10}|{:^15}|{:^30}"
class DatabaseReporter:
    
    def generateReport(self):
        reportFile = open("report", "w")
        
        try:
            md = MovieDatabase()
            movies = md.loadAllMovies()
            
            self.__writeToFile(reportFile, movies)

        finally:
            reportFile.close()
    
    def __writeToFile(self, reportFile, movies):
        if(reportFile == None):
            pass
        if(movies == None):
            pass
        if not isinstance(movies, list):
            pass
            
        self.__createHeaderTemplate(reportFile)
        
        for movie in movies:
            reportFile.write("\n")
            header = columnFormat.format(movie._id,movie.name,movie.status,movie.storage,movie.comments)
            reportFile.write(header)
            reportFile.write("\n")
            reportFile.write(self.__write_separator("-"))

    def __createHeaderTemplate(self, reportFile):
        reportFile.write(self.__write_separator())
        reportFile.write("\n")        
        header = columnFormat.format("ID", "Name", "Status", "Storage", "Comments")
        reportFile.write(header)
        reportFile.write("\n")        
        reportFile.write(self.__write_separator())
        
    def __write_separator(self, sepchar="="):
        separator = ""
        for char in range(80):
            separator = separator + sepchar
            
        return str(separator)
                    
                
def launch():
    
    dr = DatabaseReporter()
    
    dr.generateReport()

launch()

