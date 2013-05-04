I made a django thing.  It's pretty closely patterned after the tutorial 
app.  There is a database storing parents and sitters and jobs.  
Parent/Sitter contact relations work.

To play with it:
Go to sitterplan/sitterplan/settings.py.  Change the 'NAME': line
to point to the path to the sitterplan/database.db file on your machine.

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