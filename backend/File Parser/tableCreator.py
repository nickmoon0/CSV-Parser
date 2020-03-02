import mysql.connector
from mysql.connector import errorcode

from ConfigReader import ConfigReader

class tableCreator():
	def __init__(self):
		self.hsi_db = "hsi"
		self.errors_db = "errorList"
		self.accounts_db = "accounts"
		self.filePath = "../../config/ProjectConfig.ini"
		
		self.config = {
			'user': ConfigReader.read_file(self.filePath, 'DatabaseCredentials', 'user'),
			'password': ConfigReader.read_file(self.filePath, 'DatabaseCredentials', 'password'),
			'host': ConfigReader.read_file(self.filePath, 'DatabaseCredentials', 'host')
		}
	
	def create_connection(self, dbName):
		if dbName:
			self.config['database'] = dbName
		
		cnx = None
		try:
			cnx = mysql.connector.connect(**self.config)
		except mysql.connector.Error as err:
			raise err
			return None
		return cnx
	
	
	def create_all(self):
		print("Creating databases...")
		self.create_databases()
		
		print("Creating tables...")
		self.create_HSI_tables()
		self.create_errors_tables()
	
	def create_databases(self):
		cnx = self.create_connection(None)
		cursor = cnx.cursor()
		
		dbList = [self.hsi_db, self.errors_db, self.accounts_db]
		
		for db in dbList:
			try:
				cnx = self.create_connection(None)
				cursor = cnx.cursor()
				cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET utf8mb4".format(self.hsi_db))
				cnx.commit()
				print(f"Created database: {db}")
				
			except mysql.connector.Error as err:
				if err.errno == errorcode.ER_DB_CREATE_EXISTS:
					print(f"Database: {db} already exists")
					dropDb = input("Drop database and create again (y/n)? (All data will be lost): ")
					if dropDb[0].lower() == 'y':
						cursor.execute(f"DROP DATABASE {db}")
						cursor.execute(f"CREATE DATABASE {db} DEFAULT CHARACTER SET utf8mb4")
						cnx.commit()
						print(f"Created database: {db}")
					else:
						print("Continuing...")
						continue
				else:
					print(f"An error has occured creating database: {db}")
					print(err)	
			finally:
				cursor.close()
				cnx.close()
			
		print("Created all databases")
			
	def create_accounts_table(self):
		tables = {}
		
		tables['UserDetails'] = (
			"CREATE TABLE `UserDetails` ("
			"	`username` VARCHAR(30) NOT NULL,"
			"	`password` VARCHAR(60) NOT NULL,"
			"	`firstName` VARCHAR(30),"
			"	`lastName` VARCHAR(30),"
			"	`email` VARCHAR(30) NOT NULL,"
			"	`isAdmin` BOOLEAN NOT NULL,"
			"	PRIMARY KEY (`username`)"
			")"
		)
		self.create_table(self.accounts_db, tables)
		
		cnx = create_connection(self.accounts_db)
		cursor = cnx.cursor()
		
		data = ('admin', '$2b$10$3Lm1DBK23PvWlLERIQyfXeuQU7Lfb8Ub8prDkQHpUDxts8.mb3nsm', 'admin@admin.com', 1)
		cursor.execute("INSERT INTO UserDetails (username, password, email, isAdmin) VALUES (%s, %s, %s, %s)")
		cnx.commit()
		cursor.close()
		cnx.close()
			
	def create_errors_tables(self):
		tables = {}
		
		tables['ErrorCode'] = (
			"CREATE TABLE `ErrorCode` ("
			"	`errorNum` INT NOT NULL,"
			"	PRIMARY KEY (`errorNum`)"
			")"
		)
		
		tables['ErrorTable'] = (
			"CREATE TABLE `ErrorTable` ("
			"	`ErrorReference` INT AUTO_INCREMENT,"
			"	`ErrorCodeFk` INT,"
			"	`incorrectRow` TEXT,"
			"	`errorMessage` VARCHAR(1000),"
			"	`resolved` BOOLEAN DEFAULT 0 NOT NULL,"
			"	`TimeOccured` DATETIME NOT NULL,"
			"	PRIMARY KEY (`ErrorReference`),"
			"	FOREIGN KEY (`ErrorCodeFk`) REFERENCES `ErrorCode` (`errorNum`)"
			")"
		)
		self.create_table(self.errors_db, tables)

	def create_HSI_tables(self):
		tables = {}
		
		tables['Parent'] = (
			"CREATE TABLE `Parent` ("
			"	`ParentNumber` INT NOT NULL,"
			"	`FirstName` VARCHAR(40) NOT NULL,"
			"	`Surname` VARCHAR(40) NOT NULL,"
			"	`Email` VARCHAR(40),"
			"	PRIMARY KEY (`ParentNumber`)"
			")"
		)
		
		tables['Student'] = (
			"CREATE TABLE `Student` ("
			"	`StudentNumber` INT NOT NULL,"
			"	`FirstName` VARCHAR(40) NOT NULL,"
			"	`Surname` VARCHAR(40) NOT NULL,"
			"	`YearGroup` INT,"
			"	`ParentFk` INT NOT NULL,"
			"	PRIMARY KEY (`StudentNumber`),"
			"	FOREIGN KEY (`ParentFk`) REFERENCES `Parent` (`ParentNumber`) ON UPDATE CASCADE"
			")"
		)
		
		tables['Title'] = (
			"CREATE TABLE `Title` ("
			"	`TitleId` INT AUTO_INCREMENT UNIQUE NOT NULL,"
			"	`TitleName` VARCHAR(3) NOT NULL UNIQUE,"
			"	PRIMARY KEY (TitleId)"
			")"
		)
		
		tables['Teacher'] = (
			"CREATE TABLE `Teacher` ("
			"	`TeacherCode` INT NOT NULL,"
			"	`TitleFk` INT,"
			"	`Surname` VARCHAR(40) NOT NULL,"
			"	PRIMARY KEY (`TeacherCode`),"
			"	FOREIGN KEY (`TitleFk`) REFERENCES `Title` (`TitleId`) ON UPDATE CASCADE"
			")"
		)
		
		tables['Subject'] = (
			"CREATE TABLE `Subject` ("
			"	`SubjectCode` VARCHAR(5) NOT NULL,"
			"	`SubjectName` VARCHAR(20) NOT NULL,"
			"	PRIMARY KEY (`SubjectCode`)"
			")"
		)
		
		tables['Class'] = (
			"CREATE TABLE `Class` ("
			"	`SubjectFk` VARCHAR(5) NOT NULL,"
			"	`TeacherFk` INT NOT NULL,"
			"	FOREIGN KEY (`SubjectFk`) REFERENCES `Subject` (`SubjectCode`) ON UPDATE CASCADE,"
			"	FOREIGN KEY (`TeacherFk`) REFERENCES `Teacher` (`TeacherCode`) ON UPDATE CASCADE,"
			"	PRIMARY KEY (`SubjectFk`, `TeacherFk`)"
			")"
		)
		
		tables['ClassEnrolement'] = (
			"CREATE TABLE `ClassEnrolement` ("
			"	`StudentFk` INT NOT NULL,"
			"	`enrolementSubjectFk` VARCHAR(5) NOT NULL,"
			"	`enrolementTeacherFk` INT NOT NULL,"
			"	FOREIGN KEY (`StudentFk`) REFERENCES `Student` (`StudentNumber`) ON UPDATE CASCADE,"
			"	FOREIGN KEY (`enrolementSubjectFk`) REFERENCES `Subject` (`SubjectCode`) ON UPDATE CASCADE,"
			"	FOREIGN KEY (`enrolementTeacherFk`) REFERENCES `Teacher` (`TeacherCode`) ON UPDATE CASCADE,"
			"	PRIMARY KEY (`StudentFk`, `enrolementSubjectFk`, `enrolementTeacherFk`)"
			")"
		)
		
		self.create_table(self.hsi_db, tables)
					
	def create_table(self, dbName, tables):
		cnx = self.create_connection(dbName)
		cursor = cnx.cursor()
		
		for table in tables:
			toAdd = tables[table]
			try:
				print(f"Creating table: {table}")
				cursor.execute(toAdd)
			except mysql.connector.Error as err:
				if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
					print(f"Table {table} already exists")
					deleteTable = input("Drop table and create again? (y/n) ")
					if deleteTable[0].lower() == 'y':
						toAddDict = {}
						toAddDict[table] = toAdd
						
						try:
							cursor.execute(f"DROP TABLE {table}")
							self.create_table(dbName, toAddDict)
						except mysql.connector.Error as err:
							if err.errno == errorcode.ER_ROW_IS_REFERENCED:
								print(f"Cannot drop table: {table} due to foreign key constraints.")
						continue
					else:
						print("Moving on...")
				else:
					print(f"An error has occured creating table {table}")
					print(err)
				


		