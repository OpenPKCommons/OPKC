# OPKC web interface 

This directory contains the tools needed to launch the OPKC web interface. This front-end content is implemented in Django. 

Django should be installed as part of the virtual environment. If it's not, you can download it using 

```
pip install Django
```

To launch the development server, navigate to this directory in the terminal and run 

```
python manage.py runserver
```

Then, open your web browser and navigate to `http://127.0.0.1:8000/`. You should see a page saying "The install worked successfully! Congratulations!"