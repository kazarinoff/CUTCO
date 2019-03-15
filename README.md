# CUTCO
Project for Oregon College Transfer Coursebook

This site is a central hub for course transfer information for students, faculty, and administrators. It includes multi-tiered models to establish permissions for teachers on different campuses with differing roles, CRUD operations depending on those roles, and an administrative dashboard to manage user access. Most importantly it serves as a quick and useful reference for students.

zachkaz.com/cutco

1. Create new virtual environment
2. Git pull
3. pip install requirements.txt
4. manage.py migrate
5. manage.py loaddata db.json (seeds the database so that the entire thing doesn't have to be refractored w/ "try/except" for all database logic)
6. manage.py runserver
