const express = require('express');
let middleware = require('./middleware.js');
let dbManagement = require('./databaseManagement.js')
//Handling Token Stuff

class HandlerGenerator {
	createAccount(req, res) {
		dbManagement.createAccount(req, res)
	}
	
	deleteAccount(req, res, next) {
		dbManagement.deleteAccount(req, res)
	}
	
	getAccounts(req, res, next) {
		dbManagement.getAccounts(res)
	}
	
	errors(req, res, next) {
		var allResults = true
		if (req.query.allResults === "false") {
			allResults = false
		}
		dbManagement.getErrors(allResults, res)
	}
	
	resolvedError(req, res, next) {
		dbManagement.resolveError(req, res)
	}
	
	login(req, res, next) {
		dbManagement.validateUser(req, res)		
	}
	
	//File Upload route
	fileUpload (req, res) {
		if(req.file === undefined) {
			res.status(406).send({
				success: false,
				message: "Please upload a file"
			});
		} else {
			res.status(200).send({
				success: true,
				message: "File recieved successfully"
			});
		}
	}
}
// Entry point
function main() {
	const app = express();
	const cors = require('cors');
	const multer = require('multer');
	
	const PORT = 4000;
	
	/*
	 * Enabling Pre-Flight requests so that its not gay
	 */
	 
	const allowedOrigins = [
		'http://localhost:3000'
	];
	
	const corsOptions = {
		origin: (origin, callback) => {
			if (allowedOrigins.includes(origin) || !origin) {
				callback(null, true);
			} else {
				callback(new Error('Origin not allowed by cors'))
			}
		}
	}
	
	app.options('*', cors(corsOptions));
	
	/*
	 * Setting up multer to handle file uploads/downloads
	 */
	 
	var storage = multer.diskStorage({
		destination: (req, file, cb) => {
			cb(null, 'uploads/')
		},
		filename: (req, file, cb) => {
			newFilename = ''
			if (file.originalname[file.originalname.length - 4] === '.') {
				newFilename = file.originalname.substring(0, file.originalname.length - 4) + '-' + Date.now() + file.originalname.substring(file.originalname.length - 4, file.originalname.length)
			} else {
				newFilename = file.originalname + '-' + Date.now()
			}
			//newFilename = file.originalname.split(".")[0] + '-' + Date.now() + '.' + file.originalname.split(".")[1]
			cb(null, newFilename)
		}
	}) 
	
	var upload = multer({ storage: storage });
	var type = upload.single('file')
	
	var handlers = new HandlerGenerator();

	app.use(express.json());

	app.post(`/login`, cors(corsOptions), handlers.login);
	app.post('/uploadFile', cors(corsOptions), middleware.checkToken, type, handlers.fileUpload);
	
	app.get('/resolveError', cors(corsOptions), middleware.checkToken, handlers.resolvedError)
	app.get('/errors', cors(corsOptions), middleware.checkToken, handlers.errors);
	
	app.get('/accounts', cors(corsOptions), middleware.checkToken, handlers.getAccounts)
	app.delete('/deleteAccount', cors(corsOptions), middleware.checkToken, handlers.deleteAccount)
	app.post('/createAccount', cors(corsOptions), middleware.checkToken, handlers.createAccount)
	
	app.listen(PORT, () => {
		console.log(`Server is running on port: ${PORT}`);
	});
}
main();