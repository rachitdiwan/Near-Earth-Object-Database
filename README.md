# Near-Earth-Object-Database
Udacity Project for data analysis using Python STL( Standard Template Library) 

The Following Approach is used when input is recived via CLI:-
Database - This file initialises the given CSV file into an object with the help
           of objects from models.
Models - This File defines objects to be used in Database file.
Search - The Search works in the following steps:
          1. It first creates a list of NEOs/Paths(as specified, if not, taking NEO) which have 
             dates according to required criterea.
          2. If filters are provided, then each of them is applied, one at a time using a for loop,
             eliminating objects from the list which doesn't match the criterea.
          3. After all the filters are applied, a list of objects is returned to the main function.
Writer - It inputs a list of objects provided by main function(same list of ojects provided by search)
         and it either goes for stdout, Csv option as provided in the input, the CSV format is saved with
         file names OUTPUT.csv.
