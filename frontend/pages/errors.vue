<template>
	<div class="container-fluid">
		<h1 class="title">Errors</h1>
		<div class="container tableContainer">
			<div class="container-fluid">
				<div class="row">
					<div class="col-sm">
						<p>Rows loaded: {{ rowCount }}</p>
					</div>
					<div class="col-sm">
						<p v-if="errorOccured" id="centerMessage" class="errorMsg">{{ errorOccured }}</p>
					</div>
					<div class="col-sm">
						<button @click="getErrorRows()" id="refreshButton" class="btn btn-dark">Refresh</button>
					</div>
				</div>
			</div>
						
			<b-table bordered striped hover class="mt-3" :busy="tableBusy" :items="items" :fields="fields" show-empty>
				<template slot="resolved" slot-scope="row">
					<b-button size="sm" @click="resolvedError(row)">
						{{ row.value }}
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
		</div>
	</div>
</template>

<style scoped>
#refreshButton {
	float: right;
}
#centerMessage {
	text-align: center;
}
table, th, tr {
	border: 1px solid #b3b3b3;
}


th {
	padding-left: 10px;
	padding-right: 10px;
}

</style>

<script>
export default {
	layout: 'sidebarView',
	data() {
		return{
			fields: [
				{
					key: 'index',
					label: 'Index'
				},
				{
					key: 'error_code',
					label: 'Error Code',
				},
				{
					key: 'data_row',
					label: 'Data Row',
				},
				{
					label: 'Error Message',
					key: 'error_message',
				},
				{
					label: 'Resolved',
					key: 'resolved',
				},
				{
					label: 'Time Occured',
					key: 'time',
				}
			],
			items: [],
			rowCount: 0,
			errorOccured: '',
			tableBusy: false,
		}
	},
	created: function() {
		this.getErrorRows()
	},
	methods: {
		getErrorRows() {
			this.errorOccured = ''
			this.tableBusy = true
			this.items = []
			this.$axios.get('http://localhost:4000/errors', {
				params: {
					allResults: false
				}
			}).then((response) => {
				for (var i = 0; i < response.data.length; i++) {
					//{ErrorCode: 1366, IncorrectRow: "["", "William", "Fitzgerald", "9", "2300"]", ErrorMessage: "Incorrect integer value: '' for column 'StudentNumber' at row 1", Resolved: 0, TimeOccured: "2019-04-28T14:49:29.000Z"}
					//console.log(response.data[i])
					
					var errorDateTime = new Date(response.data[i].TimeOccured)
										
					this.items.push({
						index: response.data[i].Index,
						error_code: response.data[i].ErrorCode,
						data_row: response.data[i].IncorrectRow,
						error_message: response.data[i].ErrorMessage,
						resolved: Boolean(response.data[i].Resolved),
						time: errorDateTime
					})
				}
				this.rowCount = this.items.length
				this.tableBusy = false
			}).catch((error) => {
				this.errorOccured = error.response.data.message
				this.tableBusy = false
			})
		},
		resolvedError(row) {
			this.errorOccured = ''
			this.$axios.get('http://localhost:4000/resolveError', {
				params: {
					rowIndex: this.items[row.index].index
				}
			}).then((response) => {
				this.items[row.index].resolved = true
			}).catch((error) => {
				console.log(error)
				this.errorOccured = "An error has occured updating row"
			})
			
		}
	}
}
</script>