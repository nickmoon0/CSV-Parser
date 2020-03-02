<template>
</template>
<script>
const Cookie = process.client ? require('js-cookie') : undefined
export default {
	created: function() {
		if (Cookie) {
			Cookie.remove('auth')
		}
		this.$store.commit('setAuth', null)
		this.$router.push({name: 'login', params: {'LoggedOut': true}})
	},
	middleware: 'checkAuthenticated'
}
</script>