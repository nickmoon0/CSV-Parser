import mysql.connector
import time
import datetime
import json
from ConfigReader import ConfigReader

filePath = "../../config/ProjectConfig.ini"

config = {
	'user': ConfigReader.read_file(filePath, 'DatabaseCredentials', 'user'),
	'password': ConfigReader.read_file(filePath, 'DatabaseCredentials', 'password'),
	'host': ConfigReader.read_file(filePath, 'DatabaseCredentials', 'host'),
	'database': ConfigReader.read_file(filePath, 'DatabaseNames', 'hsi')
}

class errorDbManager():
	def __init__(self):
		self.dbName = 'errors'
		
	def create_connection(self):
		errorConfig = config
		errorConfig['database'] = 'errorList'
		cnx = None
		try:
			cnx = mysql.connector.connect(**errorConfig)
		except mysql.connector.Error as err:
			raise err
			return None
		return cnx
		
		
	def newError(self, err, row):
		self.insertErrorCode(err)
		self.insertError(err, row)	
	
	def insertErrorCode(self, err):
		query = "INSERT INTO ErrorCode (errorNum) VALUES (%s)"
		data = err.errno,
		self.insert(query, data)
		
	def insertError(self, err, row):
		query = "INSERT INTO ErrorTable (ErrorCodeFk, incorrectRow, errorMessage, resolved, TimeOccured) VALUES (%s, %s, %s, %s, %s)"
		data = (err.errno, row, err.msg, False, datetime.datetime.now())
		self.insert(query, data)
		
	def insert(self, query, data):
		cnx = self.create_connection()
		cursor = cnx.cursor()
		try:
			cursor.execute(query, data)
			cnx.commit()
			cursor.close()
			cnx.close()
			print(f"New error logged :(")
		except mysql.connector.IntegrityError as err:
			return
		except mysql.connector.Error as err:
			return
		
class dbManager():
	def __init__(self):
		self.cnx = ''
		self.cursor = ''
		self.dbName = 'hsi'

	def connect_to_database(self):
		try:
			config['database'] = 'hsi'
			cnx = mysql.connector.connect(**config)
		except mysql.connector.Error as err:
			raise err
			return None
		return cnx

	def parse_data(self, row):
		try:
			titleData = row['TeacherTitle'],
			teacherData = (row['TeacherCode'], row['TeacherTitle'], row['TeacherSurname']) # Make sure to change teacher title to titleId
			subjectData = (row['SubjectCode'], row['SubjectName'])
			classData = (row['SubjectCode'], row['TeacherCode'])
			
			parentData = (row['ParentNumber'], row['ParentFirstName'], row['ParentSurname'], row['ParentEmail'])
			studentData = (row['StudentNumber'], row['StudentFirstName'], row['StudentSurname'], row['StudentYear'], row['ParentNumber'])
			
			classEnrolementData = (row['StudentNumber'], row['SubjectCode'], row['TeacherCode'])
		except KeyError as err:
			print("Error in file formatting.")
			errorConfig = config
			errorConfig['database'] = 'errorList'
			cnx = None
			try:
				cnx = mysql.connector.connect(**errorConfig)
			except mysql.connector.Error as err:
				raise err
				return None
			cursor = cnx.cursor()
			data = (json.dumps(dict(row)), "Key error occured", datetime.datetime.now())
			query = "INSERT INTO ErrorTable (incorrectRow, errorMessage, TimeOccured) VALUES (%s, %s, %s)"
			cursor.execute(query, data)
			cnx.commit()
			cursor.close()
			cnx.close()
			return
			
		self.insertTitle(titleData)
		self.insertTeacher(teacherData)
		self.insertSubject(subjectData)
		self.insertClass(classData)
		
		self.insertParent(parentData)
		self.insertStudent(studentData)
		
		self.insertClassEnrolement(classEnrolementData)		

	def insert(self, query, data, tableName):
		try:
			self.cursor.execute(query, data)
			self.cnx.commit()
			print(f"Inserted {data} into {tableName}")
		except mysql.connector.Error as err:
			if err.errno != 1062:
				errDbManager = errorDbManager()
				errDbManager.newError(err, json.dumps(data))
				self.cnx = self.connect_to_database() # Create a connection to the database (This will be used the whole time)
				self.cursor = self.cnx.cursor() # Create a cursor to execute queries

	def insertTitle(self, data):
		query = "INSERT INTO Title (TitleName) VALUES (%s)"
		self.insert(query, data, "Title")

	def insertTeacher(self, data):
		titleQueryData = data[1],
		titleQuery = "SELECT TitleId FROM Title WHERE TitleName = %s"
		self.cursor.execute(titleQuery, (titleQueryData))
		
		dataList = list(data)
		
		for TitleId in self.cursor:
			dataList[1] = TitleId[0]
		
		data = tuple(dataList)
		
		query = "INSERT INTO Teacher (TeacherCode, TitleFk, Surname) VALUES (%s, %s, %s)"
		self.insert(query, data, "Teacher")
		
	def insertSubject(self, data):
		query = "INSERT INTO Subject (SubjectCode, SubjectName) VALUES (%s, %s)"
		self.insert(query, data, "Subject")
		
	def insertClass(self, data):
		query = "INSERT INTO Class (SubjectFk, TeacherFk) VALUES (%s, %s)"
		self.insert(query, data, "Class")

	def insertParent(self, data):
		query = "INSERT INTO Parent (ParentNumber, FirstName, Surname, Email) VALUES (%s, %s, %s, %s)"
		self.insert(query, data, "Parent")
		
	def insertStudent(self, data):
		query = "INSERT INTO Student (StudentNumber, FirstName, Surname, YearGroup, ParentFk) VALUES (%s, %s, %s, %s, %s)"
		self.insert(query, data, "Student")

	def insertClassEnrolement(self, data):
		query = "INSERT INTO ClassEnrolement (StudentFk, enrolementSubjectFk, enrolementTeacherFk) VALUES (%s, %s, %s)"
		self.insert(query, data, "ClassEnrolement")

	def insert_rows(self, rowList):
		self.cnx = self.connect_to_database() # Create a connection to the database (This will be used the whole time)
		self.cursor = self.cnx.cursor() # Create a cursor to execute queries
		for row in rowList:
			self.parse_data(row) # Parses and inserts the data from each row
		self.cursor.close() # Closes the cursor
		self.cnx.close() # Closes the connection
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		