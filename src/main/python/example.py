from datetime import datetime
myFile = open('append111.txt', 'a') 
myFile.write('\nAccessed on ' + str(datetime.now()))