How to setup Sailracing app

run run.py to initialize the app and set up the db.

once initialized register a user to later set as admin and then shut down the server.

to set the users admin privileges, do the following:

type in terminal

flask shell
user = User.query.filter_by(username="your_admin_username").first()
user.admin = True
db.session.commit()
exit()


Now you can start the app again and use the created admin with its features.