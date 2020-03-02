export default function({ $axios, store }) {
	$axios.onRequest((config) => {
		try {
			config.headers.common['x-access-token'] = store.state.auth.accessToken
		} catch (error) {
			return
		}
	})
}