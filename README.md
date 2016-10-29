# flaskbooksuper

# Section 2 - Lecture 2 - Introduction to MongoDB
    - MongoDB structure
        - Databases
            - Collections
                - User
                - Blog
                - Post
                - Each Collection can have one or many indexes
                     * Index on UserName and Email in the User Collection
                - Each record in a Collection is called a Document
                - Each Document can have different schemas/structures
                - Generates a long random string called object_id that is the id


# Section 2 - Lecture 3 - Setting up MongoDB on Cloud9
    - First install MongoDB by typing the following in the terminal
        $ sudo apt-get install -y mongodb-org
    - Then in the terminal, type the following in the /home/ubuntu/workspace directory (where Cloud9 starts you)
        $ mkdir ~/data
        $ mkdir ~/log
        $ mkdir flaskbook
        $ cd flaskbook
    - In the flaskbook folder, create the MongoDB configuration file
        $ touch mongod.conf
    - After opening and adding to mongod.conf, run the following in Cloud9 to start MongoDB
        $ mongod -f mongod.conf
    - If that doesn't work, run:
        $ "mongod" -f mongod.conf
    - To shutdown MongoDB
        $ mongo
        \> use admin
        \> db.shutdownServer()
    - If that doesn't shut it down, find the kill the process
        $ lsof -i:27017  # if on port 27017
        $ kill <PID>  # replace PID the value found using the above command


# Section 2 - Lecture 4 - Playing with MongoDB
    - Access the command line interface (CLI)
        $ mongo
    - Add new document to test Collection
        \> db.test.insert({name: "Michael", last_name: "Skolnik"})
    - Show the new document
        \> db.test.find()

        \> db.test.insert({name: "James", last_name: "Richards"})
    - Show a specific record
        \> db.test.find({last_name: "Skolnik"})
    - Create an index
        \> db.test.createIndex({ last_name: 1 })
        * 1 is ascending order, -1 is descending order
    - Insert a new record with different schema
        \> db.test.insert({name: "Juan", last_name: "Escobar", age: 47})
    - Create document inside of documents
        \> db.test.insert({name: {first_name: "Ricardo", last_name: "Escobar"}, age: 23})
    - Find people less than 40 in age
        \> db.test.find({age: { $lt: 40 } })
    - Find using AND (a commma)
        \> db.test.find( {name: "Michael", last_name: "Skolnik"} )
    - To update a records
        \> db.test.update( {name: "Michael" }, { $set: {last_name: "Skittles" } })


# Section 2 - Lecture 5 - The Basic Factory Structure
    - Install virtualenv
        $ sudo -H pip install virtualenv
    - Create virtual environment
        $ virtualenv -p python3 venv
    - Create requirements.txt and install everything that's in it
        $ sudo -H pip install -r requirements.txt
    - Create settings.py, application.py, and manage.py
    - Create a run configuration so don't have to run manage.py every time
        * Click the + by the terminal window and choose "New Run Configuration"
        * In the Command box, put the following:
            /home/ubuntu/workspace/flaskbook/venv/bin/python3 /home/ubuntu/workspace/flaskbook/manage.py runserver
              * Need to have full path of both python3 and manage.py
        * In the Run Config Name box, put in a name, e.g. Flask Runner
        * Click Run
        * To stop it, click Stop


# Section 2 - Lecture 6 - Introduction to Blueprints
    - Blueprints allow you to modularize your application
    - They also allow for advanced routing
    - Create users directory and in that directory, views.py and __init__.py
        * Don't have to put anything in __init__.py
        * The application will run without it, but it's good practice to add it
        * Add it so what's in the folder is importable


# Section 3 - Lecture 1 - Creating the User Model
    - db_field is the name of that field in the actual document; use a single letter or very few
        * Do that because the full field name will take a lot of data if there are tons of records
        * Saves a lot of characters
    - To add a user at the CLI
        $ python manage.py shell
            \>>> from user.models import User
            \>>> user = User(username="mike", password="test", email="mikeskolnik75@gmail.com", first_name="Mike", last_name="Skolnik")
            \>>> user
            <User: User object>
            \>>> user.username
            'mike'
            \>>> user.save()
            <User: User object>
            \>>> user.id
            ObjectId('580cf18b2684030f4d42dbc9')
            \>>> user = User(username="susan", password="test", email="susan@example.com", first_name="Susan", last_name="Smith")
            \>>> user.id
            \>>> user
            <User: User object>
            \>>> user.save()
            <User: User object>
            \>>> user.id
            ObjectId('580cf1cc2684030f4d42dbca')


# Section 3 - Lecture 2 - Adding Indexes
    - To show indexes in MongoDB shell
        \> db.user.getIndexes()
    - After changing model (adding fields, indexes, etc.), need to go in Python shell and create a new user
        \>>> user.to_json()
            * Shows user in JSON format
    - In MongoDB shell
        \> db.user.find({"u":"mike"}).explain()
            * explain() gives more information and lets you see if an index is used


# Section 3 - Lecture 3 - The User Register Form
    - db.user.drop() to delete existing MongoDB data


# Section 3 - Lecture 4 - User Registration
    - Add py-bcrypt to requirements.txt and install


# Section 3 - Lecture 5 - Setting Up Unit Testing
    - Unit Testing Guidelines
        * All tests should be automated; little as possible manual work to run the tests
        * All tests should be independent of each other
        * Tests should be consistent and repeatable
        * Tests should be maintainable; constantly working on and making them better


# Section 3 - Lecture 6 - User Registration Unit Testing
    - Run tests.py that's in the main folder
        $ python tests.py


# Section 3 - Lecture 7 - User Login
    - If you don't properly shutdown Mongo, you have restart
    - The instructor created a "mongo_restart" script
        * Put in the project's root directory, i.e. flaskbook
        * Then type:
            $ chmod 755 mongo_restart
            $ ./mongo_restart


# Section 3 - Lecture 8 - User Login Testing


# Section 3 - Lecture 9 - Navbar and Starting User Profile


# Section 3 - Lecture 10 - User Profile


# Section 3 - Lecture 11 - Check Username Format with Regular Expressions
    - ^ is beginning of string, $ is end of string
    - re.match("^[a-zA-Z0-9_-]{4,25}$"
        * lowercase, uppercase, numbers, underscore, dash, min length of 4, max of 25


# Section 3 - Lecture 12 - Edit Profile Form and Model
    - import signals from mongoengine
    - Add pre_save function
        * pre_save always has the same arguments: cls, sender, document, kwargs
    - Add blinker to requirements.txt


# Section 3 - Lecture 13 - Edit Profile Views and Templates


# Section 3 - Lecture 14 - Edit Profile Tests


# Section 3 - Lecture 15 - Introduction to AWS SES
    - SES = Simple Email Service
    - Go to Services and select IAM
        * Allows you to create users
    - Create the user and save the security credentials somewhere
    - Click Policies
    - Filter for SES
    - Check "AmazonSESFullAcces", click Attach, and attach to the user
    - Go to Services and select SES
    - Click Email Addresses
    - Click Verify New Email Address to add a new one
        * Must be valid because have to click a link; I used mailinator
    - Once you receive the email, click the link to Verify
    - Refresh the Email Addresses page and click verified under status
    - Copy the "MAIL FROM Doman" part
        * us-west-2.amazonses.com
        * It's the region you have to put in the application


# Section 3 - Lecture 16 - Implementing Email Templates
    - Add boto3 to requirements.txt
    - Create a new directory from project's root, ~/.aws
    - Create a new file in there called credentials, e.g. touch ~/.aws/credentials
    - Add the AWS access key and secret access key
    - Create another file in there called config, e.g. touch ~/.aws/configuration
    - Add the region, us-west-2 in this case
    - Create a mail directory in templates
    - Create a user directory in templates/mail
    - Add .html and .txt
        * Email clients that can't read html will get the text one instead
    - Add email function to common.py
    - Send a test
       $ python manage.py shell
       \>>> from flask import render_template
       \>>> from user.models import User
       \>>> user = User.objects.first()
       \>>> body_html = render_template("mail/user/register.html", user=user)       
       \>>> body_text = render_template("mail/user/register.txt", user=user)       
       \>>> from utilities.common import email
       \>>> email("cluepyre@mailinator.com", "Welcomd to Flaskbook", body_html, body_text)


# Section 3 - Lecture 17 - Increasing Sending Limits in AWS SES
    - Go to AWS management console
    - Click SES
    - Click Sending Statistics under "Email Sending"
    - Click "Request a Sending Limit Increase"
        * Region - US West (if that's what you have)
        * Limit - Daily Desired Sending Quota
        * New limit value - 100
        * Mail type - Transactional
        * Use Case Description - Testing a new application
        * Contact method - Web
        * Does your email-sending comply with the AWS Service Terms and AWS Acceptable Use Policy (AUP) - Yes
        * Do you only send to recipients who have specifically requested your mail - Yes
        * Do you have a process to handle bounces and complaints - Yes
    - Submit and wait


# Section 3 - Lecture 18 - User Registration Email Confirmation Code
    - 
