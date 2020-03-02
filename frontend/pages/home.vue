<template>
	<div class="container-fluid">
		<div>
			<h1 class="title">Home</h1>
			<p>Welcome to 'The Interface'</p>
		</div>
		
		<div class="container">
			<br>
			<h5>Uploading Files</h5>
			<p>
				In order to upload a file please navigate to the 'Upload File' section in the sidebar.
				<br>
				Upon opening this section you will be greeted with two buttons that say "Choose file" and "Upload"
				<br>
				First, click choose file and a drop down menu should appear. You will be able to select the file<br>
				you wish to upload. Once you have selected the file you wish to upload please press upload.<br>
				If successful a green message above the boxes will appear that says 'Successfully uploaded file!'<br>
				If it was not successful a red error message will appear above the boxes. All of the files are processed<br>
				by a backend system.
			</p>
			
			<br>
			
			<h5>Managing Errors</h5>
			<p>
				If there are any errors when parsing or inserting the data from the files into the database they will appear<br>
				in the errors section. In sidebar there will be a section marked errors. Click on that and you will be taken<br>
				to the errors page. Here there will be a table with 6 columns. The first column titled 'Index' is the index<br>
				that is used to reference that error in the database. The second column is the error code. This is the error<br>
				code that MySQL supplies when something goes wrong so that you can determine what the cause of error was. A<br>
				full list of error codes and their meanings can be found at <a href="https://www.fromdual.com/mysql-error-codes-and-messages">this website</a>.<br>
				The next column is titled 'Data Row'. This is the row of data that caused the error when it was attempted to insert it<br>
				into the database. The error message column is the error message supplied when the error occured. The resolved<br>
				column has a double purpose. It is a button that says either true or false. If it says false it means the<br>
				error/issue has not been resolved and if it says true it means it has. When pressed it will change the value<br>
				in the database to true and as such it will not appear again when the page or table is refreshed. The time<br>
				occured column, as the name suggests, is the date and time at which the error occured. In the top right of<br>
				the table there is a button labelled refresh. When pressed that button will empty the table, retreive the <br>
				data from the database again and then populate the table with the new 'fresh' data.
			</p>
			
			<br>
			
			<h5>Creating/Managing Users</h5>
			<p>
				In the sidebar there is a section at the bottom labeled 'Accounts'. If you click on this a table with all the users<br>
				will appear. From here you can see all the users details. At the bottom there is a button labeled 'Create Account'.<br>
				This button will enable you to create user accounts. You can also delete accounts from the main account page. When finished<br>
				with the system please logout using the logout button at the bottom of the sidebar.
			</p>
		</div>
	</div>
</template>

<style scoped>
* {
	text-align: center;
}
li {
	display: inline-block;
}
.subheading {
	text-decoration: underline;
}
</style>

<script>
export default {
	layout: 'sidebarView'
	
}
</script>