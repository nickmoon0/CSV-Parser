let jwt = require('jsonwebtoken');
const config = require('./config.js');

let checkToken = (req, res, next) => {
	let token = req.headers['x-access-token'] || req.headers['authorization'];
	if (!token) {
		return res.status(403).send({
			success: false,
			message: 'Auth token not supplied'
		});
	}
	if (token.startsWith('Bearer ')) {
		token = token.slice(7, token.length);
	}
	
	if (token) {
		jwt.verify(token, config.secret, (err, decoded) => {
			if (err) {
				return res.status(403).send({
					success: false,
					message: 'Token is not valid'
				});
			} else {
				req.decoded = decoded;
				next()
			}
		});
	} else {
		return res.status(403).send({
			success: false,
			message: 'Auth token not supplied'
		});
	}
};

module.exports = {
	checkToken: checkToken
}