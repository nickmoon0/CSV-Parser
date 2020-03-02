<template>
	<div class="container-fluid">
		<h1 class="title">Accounts</h1>
		<div class="tableContainer">
			<p v-if="successMessage" class="successMsg">{{ successMessage }}</p>
			<b-table bordered striped hover class="mt-3" :busy="tableBusy" :items="items" :fields="fields" showempty>
				<template slot="delete" slot-scope="row">
					<b-button size="sm" @click="deleteAccount(row)" class="bg-danger">
						Delete
					</b-button>
				</template>
				
				<template slot="empty" slot-scope="items" class="text-center my-2">
					<h1>Nothing to show :)</h1>
				</template>
				
				<div slot="table-busy" class="text-center my-2">
					<b-spinner class="align-middle"></b-spinner>
					<strong>Loading</strong>
				</div>
			</b-table>
			<b-button style="float: right;" @click="toCreateAccount">
				Create Account
			</b-button>
		</div>
	</div>
</template>

<style scoped>
.deleteButton {
	color: 
}
</style>

<script>
export default {
	layout: 'sidebarView',
	data() {
		return {
			fields: [
				{
					key: 'username',
					label: 'Username'
				},
				{
					key: 'password',
					label: 'Password'
				},
				{
					key: 'firstname',
					label: 'First Name'
				},
				{
					key: 'surname',
					label: 'Surname'
				},
				{
					key: 'email',
					label: 'Email'
				},
				{
					key: 'isAdmin',
					label: 'Is Admin'
				},
				{
					key: 'delete',
					label: 'Delete'
				}
			],
			items: [],
			errorMessage: '',
			successMessage: '',
			tableBusy: false
		}
	},
	created: function() {
		this.getAccounts()
	},
	methods: {
		toCreateAccount() {
			this.$router.push('createAccount')
		},
		deleteAccount(row) {
			this.$axios.delete(
				'http://localhost:4000/deleteAccount', 
				{ data: { username: row.item.username } }
			).then((response) => {
				this.successMessage = response.data.message
			}).catch((error) => {
				this.errorMessage = error.response.data.message
			})
		},
		getAccounts() {
			this.tableBusy = true
			this.items = []
			this.$axios.get(
				'http://localhost:4000/accounts'
			).then((response) => {
				for (var i = 0; i < response.data.length; i++) {
					this.items.push({
						username: response.data[i].username,
						password: response.data[i].password,
						firstname: response.data[i].firstname,
						surname: response.data[i].surname,
						email: response.data[i].email,
						isAdmin: response.data[i].isAdmin
					});
					this.tableBusy = false
				}
			}).catch((error) => {
				this.errorMessage = error.response.data.message
				this.tableBusy = false
			})
		}
	}
}
</script>