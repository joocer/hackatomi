# Hans

On a 1 second loop:

- choose a username from a set of 2000 (500 + 1500 randoms)
- send a random authentication request - if successful, drain account, if unsuccessful continue

On an interval to be determined, send SQL injection disguised in a ANSI sequence

e.g.  `password\r' OR 1 = 1 --`

If we get the database, increase the accuracy of the sign-ins.


----

keep track of user names and their status
- valid, invalid, locked
