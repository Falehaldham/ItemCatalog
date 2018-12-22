## My Favorite Manga Item Catalog Project
This application lists manga catalog that I favorite myself. It lists my favorites based on their category (action, sport, comedy...) and a click on each one will display breif information about the manga. 

the application was designed so that users can add, edit and/or delete manga as desired. However, only registered users can do so.

## Dependinces and Installations:
The application uses few dependincies that needs to be installed for it to be functional:
1- Flask:
Installation commend: `pip install flask`

2- sqlalchemy:
Installation commend: `pip install sqlalchemy`

3- random, string, json
Included within Python library

4- oauth2client:


5- httplib2:
Installation commend: `pip install httplib2`

6- requests:
Included within Python library

## Deployment Environment
The Deployment Environment on which the application was designed is as follows:
- Operating System: the script connects to a Virtual Machine - Ubuntu 16.04.5 LTS installed using Vagrant. 

- Database: the database engine used is SQLite (used as a light database for the sake of development. it is recomended to upgrade the database to a more mature one such as PosgreSQL or MySQL as desired)

- The actual database used to store data is named: mangacatelog.db.sql database which is provided in my GitHub account as a way to demonstrate the working version of the application. You have the choice to use it or populate your own favorites from the data creator script called "lotsofmanga.py (you need to edit its content to reflect your own data). If you choose to have your own data, make sure to first create the database using the 

- Clone the project into your GitHub account or into your local git directory from this URL (make sure this lives in your VM):
`URL goes here`

## Running the application
1- Running the Backend server:
- Access your VM on which you've cloned the project (hints: `Vagrant up` then `Vagrant ssh`)
- navigate to the directory in which you've cloned the project
- provided that you've installed all the dependincies (see Dependinces and Installation section), run the app.py script using Python 2.7:
`python app.py`
- navigate to the following URL:
`http://localhost:8000/`
- you should be presented with the home page of the application

2- Navigating the Frontend:
- the left hand side is where the manga category listed, clicking on each one should return the corresponding manga falls under it. clicking on each manga should return a description about the manga.
- the right hand side of the home page lists the top 5 recently added manga, clicking on any of them should takes you to a description about the manga.
- on the top left corner, a login link is provided for users to either register or sign in using their Google Accounts.
- Once a user is logged in, the user will be presented with bottons to allow for add, edit, or delete manga as desired.

## Future Improvements
The development of this project was done to demonstrate several concepts learnd through the Full-Stack Nano Degree course provided by Udacity. In its development, I was concentrating on delivering the project requirenments but there is plenty room for improvments. To improve upon this project, you can try to implement the following:
- allow users to register/login to the application directly
- allow users to register/login using FaceBook and/or Twiter
- allow users to create, edit and/or delete manga categories (currently, users can only do that for an actual manga item)
- implement user previliges (not all users have the capibality to add, edit and/or delete manga or categories)
- display the name of user who created each manga
