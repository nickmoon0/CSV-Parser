import time
import csv
import datetime
import hashlib

from os import listdir
from os.path import isfile, join

from databaseManager import dbManager
from tableCreator import tableCreator
from ConfigReader import ConfigReader

class MyHandler():
	def __init__(self):
		self.mod_counter = 0
		self.create_counter = 0
		self.watch_files = []
		self.ignore_files =[]
		
	def insert_data(self, filePath):
		rowList = []
		with open(filePath) as csv_file:
			csv_reader = csv.DictReader(csv_file)
			line_count = 0
			for row in csv_reader:
				rowList.append(row)
		
		db = dbManager()
		db.insert_rows(rowList)
		
		print("Finished inserting rows")

class dir_checker():
	def __init__(self):
		self.sleep_interval = 1 # Time that program waits before checking again
		self.minimum_same_hash = 5 # Amount of times a file should be iterated over before being processed
		# (The time taken for a file to be processed in seconds = sleep_interval * minimum_same_hash)
		
		self.watch_files = [] # Files that the program should watch and check
		self.ignore_files = [] # Files that the program should ignore
		
		self.monitor_dir = join('..', 'API Server', 'uploads') # Directory that the program should monitor
		self.file_extensions = ['.csv'] # File extensions that program should allow
		
		self.handler = MyHandler()
	
	def run(self):
		try:
			while True:
				time.sleep(self.sleep_interval)
				self.check_for_updates()
		except KeyboardInterrupt:
			print("\nExiting now...")
	
	# Calculating a files hash (used to see if its changed)
	def calculate_file_hash(self, file):
		hash_md5 = hashlib.md5()
		with open(file, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return hash_md5.hexdigest()
		
	def check_if_contains(self, file, toCheck):
		if len(toCheck) <= 0:
			return False
		try: # Try to check if file is in the path of a toCheck element
			for i in range(len(toCheck)):
				if toCheck[i]['path'] == file:
					return True
		except: # If toCheck does not contain dicts it checks if the string is in toCheck
			if file in toCheck:
				return True
		return False
		
	def check_for_updates(self):
		# Getting a list of all the files in the chosen dir
		files = [f for f in listdir(self.monitor_dir) if isfile(join(self.monitor_dir, f))]
		
		if (len(files) <= 0) :
			return
		
		# Ignoring all the files that are not .csv files
		for i in range(len(files)):
			# Check to see if the file has already been checked
			files[i] = self.monitor_dir + '/' + files[i]
			if self.check_if_contains(files[i], self.watch_files) or self.check_if_contains(files[i], self.ignore_files):
				continue # If it has skip over it
			print(f"Checking file type of: {files[i]}")
			if files[i][-4:] not in self.file_extensions:
				if (files[i] in self.ignore_files):
					continue
				else:
					self.ignore_files.append(files[i])
					print(f"Ignored file: {files[i]}")

		# Deleting ignored files from array
		for i in range(len(self.ignore_files)):
			if self.check_if_contains(self.ignore_files[i], self.watch_files):
				self.watch_files = [x for x in self.watch_files if x != self.ignore_files[i]]
						
		# Checking if self.watch_files contains a file
		for file in files:
			if self.check_if_contains(file, self.watch_files): 
				continue # Continue if it does contain it
			elif self.check_if_contains(file, self.ignore_files):
				continue # Continues if file is in the ignore_files array
			else:
				print(f"New file found: {file}") # Add it if it doesnt
				self.watch_files.append({
					'path': file,
					'hash': self.calculate_file_hash(file),
					'same_hash_count': 0
				})
				print(f"New file added: {self.watch_files[len(self.watch_files) - 1]}")
		
		# Checking if the file has changed by calculating the hash and comparing it to the last recorded hash
		for i in range(len(self.watch_files)): 
			file_hash = self.calculate_file_hash(self.watch_files[i]['path']) # Calculate file hash now so that big files dont calculate it multiple times
			
			if self.watch_files[i]['hash'] == file_hash: # Calculate hash of file and compare it to previously recorded hash	
				self.watch_files[i]['same_hash_count'] += 1 # If it is the same increase the same hash count by 1
				print(f"File: {self.watch_files[i]['path']} has the same hash as last recorded ({self.watch_files[i]['hash']})")
				
				if self.watch_files[i]['same_hash_count'] >= self.minimum_same_hash: # If its reached the minimum same hash count start to process it
					print(f"{self.watch_files[i]['path']} has not changed in {(self.minimum_same_hash * self.sleep_interval) / 60} minute(s).")
					print("Processing file now...")
					
					self.handler.insert_data(self.watch_files[i]['path']) # Process File and yeet it into the database (Delete file afterwards)
					self.ignore_files.append(self.watch_files[i]['path']) # Add file to ignore list after its been processed
					
					print(f"Added: {self.watch_files[i]} to ignore files")
					continue
			else:
				self.watch_files[i]['same_hash_count'] = 0
				self.watch_files[i]['hash'] = self.calculate_file_hash(self.watch_files[i]['path'])
				print(f"File: {self.watch_files[i]['path']} does not have the same hash")
				
		new_watch_files = [] # Create list to hold all the unprocessed watch_files
		for file in self.watch_files:
			if self.check_if_contains(file['path'], self.ignore_files): # Check if each file is in self.ignored_files)
				continue # Skip over it if it is
			else:
				new_watch_files.append(file) # Add it to new list if its not
		
		if self.watch_files != new_watch_files:
			print("Updated watch_files")
			self.watch_files = new_watch_files
						
		
if __name__ == "__main__":
	checker = dir_checker() # Object that polls directory for new files and checks that theyve downloaded
	
	db = dbManager() # Object that will be used to create the tables if they dont exist
	
	filePath = "../../config/ProjectConfig.ini" # File path to the configuration file
	firstTimeOpened = ConfigReader.read_file(filePath, 'ProjectSettings', 'FirstTimeOpened') # Opening and loading values into configuration file
	if firstTimeOpened == 'true': # Checking if it is the programs first time being run
		tc = tableCreator() # If it is then start creating the databases and tables
		tc.create_all()
		ConfigReader.write_file(filePath, 'ProjectSettings', 'FirstTimeOpened', 'false') # Change the value in the config file to false so that it knows its been run before
	
	print("Starting file watcher...")
	checker.run() # Checking directory
