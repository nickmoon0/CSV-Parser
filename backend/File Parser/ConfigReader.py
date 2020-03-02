import configparser

class ConfigReader():
	def read_file(filePath, header, parameter):
		config = configparser.ConfigParser()
		config.optionxform = str 
		config.read(filePath)
		returnVal = config[header][parameter]
		return returnVal
	
	def write_file(filePath, header, parameter, value):
		config = configparser.ConfigParser()
		config.optionxform = str 
		config.read(filePath)
		
		config[header][parameter] = value
		
		with open(filePath, 'w') as configfile:
			config.write(configfile)
		