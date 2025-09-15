Data was collected by running a query on 
https://stathead.com/football/player-season-finder.cgi
    
rawSeasonsData.csv
    Find single seasons matching criteria
    Sort by descending season
    Seasons 1984 - 2024
    Position: RB only
    Game Type: Regular Season
    Statistical Filters (added so the correct stats appear on the chart): 
        Rushing attempts: 0
        Targets: 0
        Touches: 0
    Team Filers: None
    Biographical Filters: None
    Status Filters: None


rawPlayerData.csv
    Find players with most seasons matching criteria
    Sort by descending
    Seasons 2000 - 2024
    Position: RB only
    Game Type: Regular Season
    Statistical Filters: 
        Rushing attempts: 50
        Targets: 0
        Touches: 75
    Team Filers: None
    Biographical Filters: None
    Status Filters: None

Once queries were run, Export Data -> Get table as CSV (for Excel) was selected
and table was copied to a csv file. It was viewed in this form so the playerID 
column could be visible.


In order to get the other .csv files necessary to run analyses, run the 
dataCleaner.py file in the code folder. All of the .csv files can then be 
found in the data folder.