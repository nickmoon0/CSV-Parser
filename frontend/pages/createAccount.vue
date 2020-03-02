<template>
	<div class="container-fluid">
		<h1 class="title">Create Account</h1>
		<div class="container-fluid centerContent">
			<div class="middleContainer">
				<p v-if="successMessage" class="successMsg">{{ successMessage }}</p>
				<p v-if="errorMessage" class="errorMsg">{{ errorMessage }}</p>
				<form name="createAccountForm">
					<label name="username" for="username">Username: </label>
					<input class="textBox" v-on:keyup.enter="submit()" v-model="username" name="username" placeholder="Username"/>
					<br>
					<label name="username" for="username">Password: </label>
					<input class="textBox" v-on:keyup.enter="submit()" v-model="password" name="password" type="password" placeholder="Password"/>
					<br>
					<label name="username" for="username">First Name: </label>
					<input class="textBox" v-on:keyup.enter="submit()" v-model="firstname" name="firstname" placeholder="First Name"/>
					<br>
					<label name="username" for="username">Surname: </label>
					<input class="textBox" v-on:keyup.enter="submit()" v-model="surname" name="surname" placeholder="Surname"/>
					<br>
					<label name="username" for="username">Email: </label>
					<input class="textBox" v-on:keyup.enter="submit()" v-model="email" name="email" placeholder="Email"/>
					<br>
					<b-button @click.stop.prevent="submit()" form="username" type="submit">Submit</b-button>
				</form>
			</div>
		</div>
		
	</div>
</template>

<style scoped>
.middleContainer {
	display: inline-block;
	text-align: right;
}
.centerContent {
	text-align: center;
}
</style>

<script>
export default {
	layout: 'sidebarView',
	data: function() {
		return {
			username: '',
			password: '',
			firstname: '',
			surname: '',
			email: '',
			successMessage: '',
			errorMessage: ''
		}
	},
	methods: {
		submit() {
			this.errorMessage = ''
			this.$axios.post('http://localhost:4000/createAccount', {
				username: this.username,
				password: this.password,
				firstname: this.firstname,
				surname: this.surname,
				email: this.email
			}).then((response) => {
				console.log("Here")
				this.successMessage = response.data.message
				this.$router.push('/accounts')
			}).catch((error) => {
				this.successMessage = ''
				this.errorMessage = error.response.data.message
			})
		}
	}
}
</script>