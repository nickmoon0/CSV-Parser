const middleware = {}

middleware['checkAuthenticated'] = require('@/middleware/checkAuthenticated.js');
middleware['checkAuthenticated'] = middleware['checkAuthenticated'].default || middleware['checkAuthenticated']

middleware['checkNotAuthenticated'] = require('@/middleware/checkNotAuthenticated.js');
middleware['checkNotAuthenticated'] = middleware['checkNotAuthenticated'].default || middleware['checkNotAuthenticated']

export default middleware
