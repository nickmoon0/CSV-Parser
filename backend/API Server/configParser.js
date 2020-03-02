var fs = require('fs')
var ini = require('ini')

var getValue = (filePath, header, parameter) => {
	var config = ini.parse(fs.readFileSync(filePath, 'utf-8'))
	
	try {
		returnVal = config[header][parameter]
		return returnVal
	} catch {
		return null
	}
}

module.exports = {
	getValue: getValue
}