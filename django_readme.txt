I made a django thing.  It's pretty closely patterned after the tutorial 
app.  There is a database storing parents and sitters and jobs.  
Parent/Sitter contact relations work.  Also, one can create jobs, and get a list of the jobs one has created.

-----
To play with it:
Go to sitterplan/sitterplan/local_install_info.py.  Change the function to return
the path to the folder holding all the stuff (all the HTML files and everything).

Start the server by doing 

python sitterplan/manage.py runserver

(if you're not very good at making things be commands like me, drag your python.exe file
into the GitHub folder first)

Then go to 

http://127.0.0.1:8000/parent/contacts/smith

or

http://127.0.0.1:8000/sitter/contacts/jimmy 

to see contact databases working.
(All parent usernames are their last names, all sitter usernames are
their first names.  Jimmy and Smith are in contact with all parents and
all sitters respectively; others only have one contact.  All contact
relationships are mutual of database-enforced necessity.)

All functionality of http://127.0.0.1:8000/parent/ is going through the server at this point.

-----
List of Annoying Things about Django:
As far as I can tell, if you change the models.py file to restructure the database, you must then destroy the database.db file and run 

python sitterplan/manage.py syncdb

to recreate it.  Then you must enter all the contacts again.  Maybe if I have to do this again more than twice I'll write a python file that does it.