# Quiz-App

#### Video Demo: <URL HERE>

## Description

Quiz-App is a web application implemented using Python's web framework Django. Users can answer the quizzes already created by other users without being logged in. In order to create a quiz however, you need to be a logged in user. Users can create quizzes, edit them and also have the ability to delete them. During quiz creation users are needed to enter a category the quiz falls in, the name of the quiz and a cover photo (optional). The categories are pre-added which this can be done using the admin dashboard. The name of a quiz has to be unique. After this the user can enter the question and two or more choices labeling at least one as correct. Only the quiz creators and the superuser have the ability to edit or delete a quiz.

Incase a user forgets their password, they can reset it by clicking on forgot password in the login page then enter their email in which they would receive an email with a link to reset their password (The project as is at the moment however sends the email to the console but can be configured to send out the email to the users email address).

The homepage contains quizzes listed by category and the recently added quiz. Each subcategory has a page containing all the quizzes it has. The profile page contains the user profile image and name together with a button to edit them and another to log out. It also contains a library section which lists all the quizzes created by that user.

In order to answer a quiz, a user clicks on that quiz, choose one of the choices and proceed to the next. When all question are answered the user will have their result displayed to them.

There are five folders in the project i.e., accounts, core, media, quiz, static and templates. The "accounts" folder is the app containing the user accounts functionality, "core" folder is the django project app, "media" contains files uploaded by the users (cover photos and profile images), "quiz" folder contains the quiz app functionality and "templates" contains the html templates.

## Getting Started with Development

### 1. Clone the project

```bash
git clone https://github.com/gdnkemboi/Quiz-App.git
```

### 2. Navigate to the project directory

```bash
cd CS50-Project-Quiz-App
```

### 3. Create a virtual environment and activate it

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 4. Install project dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup the database (optional)

- ### Postgresql installation

  Install postgres following the instructions of their [website](https://www.postgresql.org/download/).

- Open 'psql' (PostgreSQL's command-line tool to interact with the database server)
- Enter the following SQL commands, to create a database and a user

```
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```

### 6. Create a .env file and add the database url

```
-- If step 5 skipped you can use the default sqlite database
DATABASE_URL=sqlite:///db.sqlite3

-- For PostgreSQL usage
DATABASE_URL=postgres://myuser:mypassword@localhost:5432/mydatabase
```

### 7. Run database migrations

```bash
python manage.py migrate
```

### 8. Create superuser

```bash
python manage.py createsuperuser
```

### 9. Run the development server

```bash
python manage.py runserver
```
