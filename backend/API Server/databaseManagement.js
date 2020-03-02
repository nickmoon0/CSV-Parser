let mysql = require('mysql');
var bcrypt = require('bcrypt');

let jwt = require('jsonwebtoken');
let config = require('./config.js');

let configParser = require('./configParser.js')
var configFilePath = "../../config/ProjectConfig.ini"

var createAccount = (req, res) => {
	var accounts_db = configParser.getValue(configFilePath, 'DatabaseNames', 'accounts')
	connection = create_connection(accounts_db)
	connection.connect()
	var user = {
		username: req.body.username,
		password: bcrypt.hashSync(req.body.password, 10),
		firstName: req.body.firstname,
		lastName: req.body.surname,
		email: req.body.email,
		isAdmin: 1
	}
	
	try {
		connection.query('INSERT INTO UserDetails SET ?', user, (error, results, fields) => {
			if (error) {
				res.status(500).send({
					success: false,
					message: "Failed to insert into database"
				});
				return
			}
			res.status(200).send({
				success: true,
				message: "Successfully inserted row into database"
			});
		})
	} catch (error) {
		res.status(500).send({
			success: false,
			message: "Failed to insert into database"
		});
	}
}

var deleteAccount = (req, res) => {
	var user = req.body.username
	var accounts_db = configParser.getValue(configFilePath, 'DatabaseNames', 'accounts')
	connection = create_connection(accounts_db)
	connection.connect()
	try {
		connection.query(`DELETE FROM UserDetails WHERE username = \'${user}\'`, (error, results, fields) => {
			if (error) {
				console.log(error)
				res.status(500).send({
					success: false,
					message: `Failed to delete user: ${user} from database`
				});
				return
			}
			res.status(500).send({
				success: true,
				message: `Successfully deleted user: ${user}`
			});
		})
	} catch (error) {
		console.log(error)
		res.status(500).send({
			success: false,
			message: `Failed to delete user: ${user} from database`
		});
	}
}

var create_connection = (dbName) => {
	var connection = mysql.createConnection({
		host: configParser.getValue(configFilePath, 'DatabaseCredentials', 'host'),
		user: configParser.getValue(configFilePath, 'DatabaseCredentials', 'user'),
		password: configParser.getValue(configFilePath, 'DatabaseCredentials', 'password'),
		database: dbName
	});
	
	return connection
}

var getAccounts = (res) => {
	var accounts_db = configParser.getValue(configFilePath, 'DatabaseNames', 'accounts')
	connection = create_connection(accounts_db)
	connection.connect()
	try {
		connection.query(`SELECT * FROM UserDetails`, (error, results, fields) => {
			if (error) throw error
			newResults = []
			for (var i = 0; i < results.length; i++) {
				newResults.push({
					'username': results[i].username,
					'password': results[i].password,
					'firstname': results[i].firstName,
					'surname': results[i].lastName,
					'email': results[i].email,
					'isAdmin': results[i].isAdmin
				})
			}
			
			res.status(200).send(newResults)
		});
	} catch (err) {
		res.status(500).send({
			success: false,
			message: "Failed to retreive data from database"
		});
	}
}

var validateUser = (req, res) => {
	let username = req.body.username;
	var password = req.body.password;
	var connection = create_connection(configParser.getValue(configFilePath, 'DatabaseNames', 'accounts'))
	connection.connect();
	connection.query(`SELECT * FROM UserDetails WHERE username = \'${username}\' or email = \'${username}\'`, (error, results, fields) => {
		if (error) throw error
		
		if (results.length <= 0) {
			res.status(403).send({
				success: false,
				message: 'Incorrect username or password'
			});
			return
		}
		
		var retrievedUsername = ''
		var retrievedPassword = results[0].password
		
		if (username === results[0].username) {
			retrievedUsername = results[0].username
		} else {
			retrievedUsername = results[0].email
		}
		if (username && password) {
			if (username === retrievedUsername && bcrypt.compareSync(password, retrievedPassword)) {
				let token = jwt.sign(
					{username: username}, 
					config.secret,
					{expiresIn: '24h'}
				);
				
				res.status(200).send({
					success: true,
					message: 'Authentication successful',
					token: token
				});
			} else {
				res.status(403).send({
					success: false,
					message: 'Incorrect username or password'
				});
			}
		} else {
			res.status(400).send({
				success: false,
				message: 'Authentication Failed! Please check request'
			});
		}
	}); 
}

let resolveError = (req, res) => {
	var index = req.query.rowIndex
	var connection = create_connection(configParser.getValue(configFilePath, 'DatabaseNames', 'errorList'))
	connection.connect()
	
	var query = `UPDATE ErrorTable SET resolved = 1 WHERE ErrorReference = ${index}`
	
	connection.query(query, (error, results, fields) => {
		if (error) {
			res.status(500).send({
				success: false,
				message: 'Failed to update data'
			})
			return
		}
		
		res.status(200).send({
			success: true,
			message: 'Successfully updated row'
		})
	})
}

let getErrors = (allResults, res) => {
	var connection = create_connection(configParser.getValue(configFilePath, 'DatabaseNames', 'errorList'))
	connection.connect()
	
	var query = ''
	if (allResults) {
		query = 'SELECT * FROM ErrorTable'
	} else {
		query = 'SELECT * FROM ErrorTable WHERE resolved = 0'
	}
	
	connection.query(query, (error, results, fields) => {
		if (error) {
			res.status(500).send({
				success: false,
				message: "Failed to retrieve results from database"
			})
			return
		}
		var newResults = []
		for (var i = 0; i < results.length; i++) {
			newResults.push({
				Index: results[i].ErrorReference,
				ErrorCode: results[i].ErrorCodeFk,
				IncorrectRow: results[i].incorrectRow,
				ErrorMessage: results[i].errorMessage,
				Resolved: results[i].resolved,
				TimeOccured: results[i].TimeOccured 
			})
		}
		res.status(200).send(newResults)
	})
}

module.exports = {
	getErrors: getErrors,
	resolveError: resolveError,
	validateUser: validateUser,
	getAccounts: getAccounts,
	deleteAccount: deleteAccount,
	createAccount: createAccount
}