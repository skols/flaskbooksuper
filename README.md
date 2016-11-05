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


# Section 3 - Lecture 7 - Creating the User Model
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


# Section 3 - Lecture 8 - Adding Indexes
    - To show indexes in MongoDB shell
        \> db.user.getIndexes()
    - After changing model (adding fields, indexes, etc.), need to go in Python shell and create a new user
        \>>> user.to_json()
            * Shows user in JSON format
    - In MongoDB shell
        \> db.user.find({"u":"mike"}).explain()
            * explain() gives more information and lets you see if an index is used


# Section 3 - Lecture 9 - The User Register Form
    - db.user.drop() to delete existing MongoDB data


# Section 3 - Lecture 10 - User Registration
    - Add py-bcrypt to requirements.txt and install


# Section 3 - Lecture 11 - Setting Up Unit Testing
    - Unit Testing Guidelines
        * All tests should be automated; little as possible manual work to run the tests
        * All tests should be independent of each other
        * Tests should be consistent and repeatable
        * Tests should be maintainable; constantly working on and making them better


# Section 3 - Lecture 12 - User Registration Unit Testing
    - Run tests.py that's in the main folder
        $ python tests.py


# Section 3 - Lecture 13 - User Login
    - If you don't properly shutdown Mongo, you have restart
    - The instructor created a "mongo_restart" script
        * Put in the project's root directory, i.e. flaskbook
        * Then type:
            $ chmod 755 mongo_restart
            $ ./mongo_restart


# Section 3 - Lecture 14 - User Login Testing


# Section 3 - Lecture 15 - Navbar and Starting User Profile


# Section 3 - Lecture 16 - User Profile


# Section 3 - Lecture 17 - Check Username Format with Regular Expressions
    - ^ is beginning of string, $ is end of string
    - re.match("^[a-zA-Z0-9_-]{4,25}$"
        * lowercase, uppercase, numbers, underscore, dash, min length of 4, max of 25


# Section 3 - Lecture 18 - Edit Profile Form and Model
    - import signals from mongoengine
    - Add pre_save function
        * pre_save always has the same arguments: cls, sender, document, kwargs
    - Add blinker to requirements.txt


# Section 3 - Lecture 19 - Edit Profile Views and Templates


# Section 3 - Lecture 20 - Edit Profile Tests


# Section 3 - Lecture 21 - Introduction to AWS SES
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


# Section 3 - Lecture 22 - Implementing Email Templates
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


# Section 3 - Lecture 23 - Increasing Sending Limits in AWS SES
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


# Section 3 - Lecture 24 - User Registration Email Confirmation Code
    - Add settings.py to .gitignore file always


# Section 3 - Lecture 25 - Confirmation Code Functionality


# Section 3 - Lecture 26 - Confirmation Code Testing


# Section 3 - Lecture 27 - Forgot and Reset Password
    - To add multiple options to render_field, have to treat as kwargs with ** and then a dictionary or list
    - Don't include the backslash. Using it here as an escape character
        * {{ render_field(form.password, \**("class":'form-control', "aria-described-by": "passwordHelpBlock")) }}


# Section 3 - Lecture 28 - Forgot and Reset Password Form Work


# Section 3 - Lecture 29 - Forgot and Reset Password Views
    - Create a function for hashing password because the same code is being repeated
        * Good place for a function


# Section 3 - Lecture 30 - Reset Password Tests


# Section 3 - Lecture 31 - Change Password
    - Homework - Create the email that gets sent when the password
        * Body: Per your request your password has been changed. If you didn't request your password to be changed, please contact support immediately


# Section 3 - Lecture 32 - Change Password Tests


# Section 3 - Lecture 33 - Image Uploading Setup
    - imagemagic - Server package so have to install use "sudo apt-get ..." on Cloud9
        * sudo apt-get update
        * sudo apt-get install imagemagick libmagickcore-dev
    - Add Wand==0.4.2 to requirements.txt
    - Test both are properly installed
        $ python manage.py shell
        \>>> from wand.image import Image
        \>>> with Image(filename="static/assets/flaskbook-logo-sm.png") as img:
        ...    print(img.size)
        ...
        (82, 20)
        * If get the above when in the shell, properly installed
    - Add two lines to settings.py
        * UPLOAD_FOLDER = "/home/ubuntu/workspace/flaskbook/static/images"
        * STATIC_IMAGE_URL = "images"
            - The folder name and url name have to be equal, i.e. images here


# Section 3 - Lecture 34 - The Imaging Library


# Section 3 - Lecture 35 - The Edit Form and Template for Image


# Section 3 - Lecture 36 - The Edit View for Imaging


# Section 3 - Lecture 37 - Setting up Amazon S3
    - Amazon will host all the images
    - Go to AWS, then Services, then S3
    - Click Create Bucket
        * Bucket Name: flaskbookms (names have to be unique as they shared by all users in the system)
        * Region: Oregon (same as everything else so far; could be different email or other things are)
    - Create folder
        * user
    - Add two lines to settings.py
        * AWS_BUCKET = "flaskbookms" (or whatever the bucket name is)
        * AWS_CONTENT_URL = "https://s3-us-west-2.amazonaws.com"
    - Attach another policy to the mailer user so can use S3
        * Services then IAM
        * Click users
        * Click mailer (or whatever the user was)
        * Click Attach Policy
        * Filter for S3 and select AmazonS3FullAccess, then click Attach Policy
    - Make settings.py look like this for when working in development environment
        * # Production Environment
        * # AWS_BUCKET = "flaskbookms"
        * # AWS_CONTENT_URL = "https://s3-us-west-2.amazonaws.com"

        * # Development Environment
        * AWS_BUCKET = ""
        * AWS_CONTENT_URL = ""
    - If in Production, comment out the development section. If in Development, comment out production.


# Section 4 - Lecture 38 - Starting the Relationship App


# Section 4 - Lecture 39 - Playing with the Relationship Model
    - Create some users and then enter the python shell
        $ python manage.py shell
        \>>> from user.models import *
        \>>> from relationship.models import *
        \>>> user1 = User.objects.get(username="michael")
        \>>> user2 = User.objects.get(username="javier")
        \>>> friends = Relationship(from_user=user1, to_user=user2, rel_type=Relationship.FRIENDS, status=Relationship.PENDING).save()
        \>>> rel = Relationship.objects.first()
        \>>> rel.to_json()


# Section 4 - Lecture 40 - Get Relationship Helper
    - Add a static method to models.py; get_relationship
    - Go into the python shell
        \>>> from user.models import *
        \>>> from relationship.models import *
        \>>> Relationship.objects.delete()
        \>>> user1 = User.objects.get(username="michael")
        \>>> user2 = User.objects.get(username="javier")
        \>>> friends = Relationship(from_user=user1, to_user=user2, rel_type=Relationship.FRIENDS, status=Relationship.APPROVED).save()
        \>>> Relationship.get_relationship(user1, user2)
            "FRIENDS_APPROVED"
        \>>> friends.status=Relationship.PENDING
        \>>> friends.save()
        \>>> Relationship.get_relationship(user1, user2)
            "FRIENDS_PENDING"
        \>>> friends.rel_type=Relationship.BLOCKED
        \>>> friends.save()
        \>>> Relationship.get_relationship(user1, user2)
            "BLOCKED"
    - After reading about it, try refactoring the staticmethod as a classmethod


# Section 4 - Lecture 41 - The Relationship Frontend
    - jQuery used, mainly for hovering
        * See if can be refactored using CSS or something else


# Section 4 - Lecture 42 - Relationship Views
    - Adding decorators.py to user and creating login_required function


# Section 4 - Lecture 43 - More Work on Relationship Views
    - Edited add_friend
    - Added remove_friend, block, unblock


# Section 4 - Lecture 44 - Complete Relationship Frontend


# Section 4 - Lecture 45 - Relationship Tests Part 1


# Section 4 - Lecture 46 - Relationship Tests Part 2


# Section 4 - Lecture 47 - Adding a Profile Image
    - Add to user.models to allow for default pictures if user hasn't uplaoded


# Section 4 - Lecture 48 - The Friends Sidebar


# Section 4 - Lecture 49 - The Friends Page
    - Refactor profile.html so friends part in different html file?


# Section 4 - Lecture 50 - Reusable Follow Button
