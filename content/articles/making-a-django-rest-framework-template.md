Title: A template for Django REST Framework projects
Date: 2014-05-15
Modified: 2014-05-24
summary: Showing off a django template to kickstart a DRF project
URL: making-a-django-rest-framework-template/
save_as: making-a-django-rest-framework-template/index.html


I made a project template for Django 1.7 + Django REST framework + PostgreSQL containing things I use and find useful.  
Part of it is based on [Two Scoops of Django template](https://github.com/twoscoops/django-twoscoops-project).  
You can see the repo on [Github](https://github.com/Keats/django-drf-template).  

## Features

It contains the following things: 

- [Django REST framework](http://www.django-rest-framework.org/): for writing your API
- [django-model-utils](https://django-model-utils.readthedocs.org/en/latest/): for things like TimestampedModel and other nice things for models
- [django-cors-headers](https://github.com/ottoyiu/django-cors-headers): automatically allows CORS on local dev and allows for a whitelist in production
- bcrypt: hash password with bcrypt instead of PBKDF2

There are also goodies on dev and test environments:

- [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar): lots of information on request/response and queries
- [ipdb](https://pypi.python.org/pypi/ipdb): pdb in ipython. Awesome
- [django-extensions](https://github.com/django-extensions/django-extensions): adds some useful management commands
- [coverage](http://nedbatchelder.com/code/coverage/): measures code coverage
- [factory-boy](https://factoryboy.readthedocs.org/en/latest/): my library of choice to create objects in tests, I go more into details in my article [Python testing: Factory Boy or Model Mommy](http://vincent.is/using-factory-boy-or-model-mommy/)
- [flake8](https://flake8.readthedocs.org): ensures code quality, respect of pep8 and other nice things, it can easily be installed as a git/mercurial hook

## Install
You will need Postgres installed and the following libs (for ubuntu/debian, for others systems look in your package managers).

```bash
$ sudo apt-get install libpq-dev python-dev
```

Create your virtualenv (and virtualenvwrapper in the example case), I will use the name myproject but use your own name.

```bash
$ mkdir myproject && cd myproject
$ mkvrirtualenv myproject
$ pip install django
$ django-admin.py startproject myproject --template=https://github.com/Keats/django-drf-template/archive/master.zip
$ cd myproject
$ pip install -r requirements/local.txt
$ python myproject/manage.py migrate
```

If you want, you can also add a pre-commit flake8 hook to ensure that commit respects it.  

```bash
$ flake8 --install-hook
```

By default it will not stop commits because of warning, a quick look at .git/hooks/pre-commit shows that putting an environment variable of FLAKE8_STRICT will stop them.  

And you should be almost good to go. 
There are a few hardcoded temporary settings that you will want to replace, look for the string 'Ann Onymous' and you should find them.  
They are in the Sphinx folder and in the base settings file if you're lazy.  

Once again, PRs are welcome if there's a bug or want to share something you use all the time that I don't necessarily know about !
