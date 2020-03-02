<template>
	<div class="container-fluid">
		<h1>Upload File</h1>
		<div class="container-fluid h-100">
			<div class="centerItems">
				<div class="middleContainer">
					<p class="successMsg">{{ successMessage }}</p>
					<p class="errorMsg">{{ failureMsg }}</p>
					<input type="file" id="file" ref="file" @change="onFileSelected"/>
					<br/>
					<button @click="submitFile" style="margin-top: 10px;">Upload</button>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.middleContainer {
	display: inline-block;
	text-align: left;
}
.centerItems {
	text-align: center;
}
</style>

<script>
export default {
	layout: 'sidebarView',
	data: function() {
		return {
			selectedFile: null,
			successMessage: '',
			failureMsg: ''
		}
	},
	methods: {
		onFileSelected(event) {
			this.selectedFile = event.target.files[0]
		},
		submitFile() {
			let formData = new FormData();
			formData.append('file', this.selectedFile);
			this.$axios.post('http://localhost:4000/uploadFile', formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			}).then((res) => {
				this.failureMsg = ""
				this.successMessage = "Successfully uploaded file!"
			}).catch((error) => {
				this.successMessage = ""
				this.failureMsg = error.response.data.message + ` (${error.response.status})`
			})
		}
	}
}
</script>