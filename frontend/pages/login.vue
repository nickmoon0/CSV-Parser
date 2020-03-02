<template>
	<div class="h-100 row align-items-center">
		<div class="col-md-4">
		</div>
		<div class="col-md-4">
			<div class="container centerPiece">
				<div class="container titleDiv">
					<h1 class="loginTitle">Login</h1>
				</div>
				<div class="container-fluid textBoxContainer">
					<p class="errorMsg">{{ incorrect }}</p>
					<p class="successMsg">{{ success }}</p>
					<form name="login">
						<input class="textBox" v-on:keyup.enter="submit()" v-model="username" name="username" placeholder="Username or Email"/>
						<br/>
						<input class="textBox" v-on:keyup.enter="submit()" v-model="password" name="password" type="password" placeholder="Password"/>
						<br/>
						<button @click.stop.prevent="submit()" form="login" type="submit" class="sendButton">Login</button>
					</form>
				</div>
			</div>
		</div>
		<div class="col-md-4">
		</div>
	</div>
</template>
<script>
import { mapActions } from 'vuex';
const Cookie = process.client ? require('js-cookie') : undefined;
//import axios from 'axios';
export default {
	name: 'login',
	middleware: 'checkNotAuthenticated',
	created: function() {
		this.success = "";
		this.incorrect = "";
		if (this.$route.params.LoggedOut === true) {
			this.success = "Logged out successfully"
		}
	},
	data: function() {
		return {
			username: '',
			password: '',
			incorrect: '',
			success: '',
			authToken: ''
		}
	},
	methods: {
		submit() {
			this.success = "";
			this.incorrect = "";
			if (!this.username.length || this.username === "") {
				this.incorrect = "Please enter username"
				return;
			} else if (!this.password.length || this.password === "") {
				this.incorrect = "Please enter password"
				return;
			}
			this.$axios.post('http://localhost:4000/login', { 
				username: this.username,
				password: this.password,
			}).then((res) => {
				if (res.data.success === false) {
					this.incorrect = "Username or password incorrect"
				} else {
					this.incorrect = ""
					this.success = res.data.message
					this.authToken = res.data.token
					this.postLogin()
				}
			}).catch(error => {
				console.log()
				this.success = ""
				this.incorrect = error.response.data.message + ` (${error.response.status})`
			})
		},
		postLogin() {
			setTimeout(() => {
				const auth = {
					accessToken: this.authToken
				}
				this.$store.commit('setAuth', auth)
				Cookie.set('auth', auth)
				this.$router.push('/home')
			}, 1000)
		}
	}
}
</script>
<style>
.sendButton {
	border-radius: 5px;
	margin-top: 5px;
}
.textBoxContainer {
	text-align: center;
	margin-bottom: 5px;
}

.centerPiece {
	border: 1px solid;
	border-color: #808080;
	border-radius: 10px;
}
.titleDiv {
	width: 175px;
}
.loginTitle {
	text-align: center;
	letter-spacing: 5px;

	border-bottom: 1px solid; 
	padding: 1.5px;
}
</style>