# CSV Parser
This is a project I created for an assessment in year 12. The aim was to make an interface where the user could upload '.csv'
files to be parsed. The program would then have to handle any errors in the file, store the contents in the database and later
retrieve the contents of the database if requested. I chose a web interface for this task and used VueJS for the frontend and
NodeJS for the backend. Python is also used to check for new files that have been uploaded in the backend.

## To run:
1. Please install python 3.6.5 from: https://www.python.org/downloads/release/python-365/
2. Please install the latest version of node.js from: https://nodejs.org/en/
(npm should have been installed with node.js however if it wasn't please install npm from: https://www.npmjs.com/products)
3. Please make sure that MySQL or XAMPP is installed (The installer for XAMPP can be downloaded here: https://www.apachefriends.org/download.html)
4. Open the file ProjectConfig.ini (in the config folder) and input all your database credentials (You shouldn't have to touch anything else
	host = The database servers address
	user = The username used to login to the database
	password = The password used to login to the database
5. Make sure the MySQL server is running 

6. Open a new terminal window and change your directory to "[...]/CompSci_proj/backend/File\ Parser"
7. Upon doing this type "source venv/bin/activate", press enter and then type ```python main.py```

8. Open a new terminal window and change your directory to "[...]/CompSci_proj/backend/API\ Server"
9. Type ```npm install``` to ensure that all dependencies are installed
10. Then type ```npm run dev```

11. Open a new terminal window and change your directory to "[...]/CompSci_proj/frontend"
12. Type ```npm install``` to ensure that all dependencies are installed
13. Type ```npm run dev```
  
After these steps have been completed you should be able to navigate to "http://localhost:3000" in your browser
and see a login screen. 
The default credentials to login are:
	username: admin
	password: Password
	
Upon logging in you will be greeted by a home screen with instructions on how to use the software.
