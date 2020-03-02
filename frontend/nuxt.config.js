module.exports = {
	plugins: [
		'~/plugins/axios',
	],
	modules: [
		'bootstrap-vue/nuxt',
		'@nuxtjs/axios'
	],
	css: [
		'@/assets/globalStyle.css',
		'@/assets/sidebarStyle.css'
	],
	axios: {
		proxyHeaders: false,
		credentials: false,
		requestInterceptor: (config, { store }) => {
			config.headers.common['x-access-token'] = store.state.auth
			return config
		}
	}
}