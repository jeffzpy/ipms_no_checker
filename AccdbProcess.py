
import pyodbc
	
def db_connect(db_location,passwd):
	if passwd != '':
		connStr = (
			r'DRIVER = {Microsoft Access Driver (*.mdb, *.accdb)};'
			r'DBQ = ' + db_location + ';'
			r'PWD = ' + passwd + ';'
		)
	else:
		connStr = (
			r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
			r'DBQ=' + db_location + ';'
		)
	conn = pyodbc.connect(connStr)
	return conn