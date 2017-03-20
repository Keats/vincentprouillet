+++
title = "Python wheel"
url = "using-the-wheel"
description = "What are wheels and why/how should I use them"
date = "2014-05-24"
category = "Programming"
tags = ["python"]
+++

To quote [PEP 427](http://legacy.python.org/dev/peps/pep-0427/), wheel is:

> A wheel is a ZIP-format archive with a specially formatted file name and the .whl extension. It contains a single distribution nearly as it would be installed according to PEP 376 with a particular installation scheme. Although a specialized installer is recommended, a wheel file may be installed by simply unpacking into site-packages with the standard 'unzip' tool while preserving enough information to spread its contents out onto their final paths at any later time.

To put it simply, wheels are a way to have your own local instant pypi.  

## Why should I care
I actually read a few articles on it some time ago but didn't see the usecase before actually using it myself.    

Here are a few concrete examples on how you could possibly use them:

- **instant installation on localhost**: having a global wheel directory where you can pull your libs from without going to pypi and doing so almost instantly, even for libs requiring compilation (lxml, pyscopg2, pillow, etc)
- **deploying without needing pypi**: obviously the compiled libs won't work if you are using different systems for developing and in production but the rest will work
- **WAY faster installation of requirements**: it takes only a few seconds to install, compared to a possibly long time depending on what you are using. Think of the time your builds on CI are taking just to install the requirements.
- maybe deploy your project as a wheel? I haven't thought about it too much but that *should* be possible and you could change version using pip, the downside being that your project would be in the site-packages directory so it would be a bit annoying for management commands for django fo example

I don't mind waiting a bit for my pip install but the deploy without pypi and the faster builds are killer features in my eyes.  

## How to use them
Let's imagine you have a project you want to convert to using wheels.  
You would have your dependencies in a requirements.txt (or several requirements file for different environments).  
The first thing you need to do is installing wheel.

```bash
$ pip install wheel # with pip version >= 1.4
```
At this point you remember that not even 10 lines above, I said we didn't use to use pypi to deploy.  
Wheels are zip archives that python can execute so that means we can actually use the wheel of wheel to install wheel (yo dawg, I heard you liked wheels).  
You could download the wheel manually and installing using whatever deployment system you are using but let's install from pip locally.  

Now that you got pip and your requirements file ready, time to reinvent the wheels (haha...).  
For example, this is the result of running it in my [Django REST Framework template](https://github.com/Keats/django-drf-template)

``` bash
$ pip wheel --wheel-dir=wheelhouse/ -r requirements/local.txt
```

A ls in wheelhouse gives me the following:
``` bash
bcrypt-1.0.2-cp27-none-linux_x86_64.whl          
docutils-0.11-py2-none-any.whl              
pep8-1.5.6-py2.py3-none-any.whl
cffi-0.8.2-cp27-none-linux_x86_64.whl            
flake8-2.1.0-py2-none-any.whl               
psycopg2-2.5.3-cp27-none-linux_x86_64.whl
Django-1.7b4-py2.py3-none-any.whl                
ipdb-0.8-py2-none-any.whl                   
pycparser-2.10-py2-none-any.whl
django_cors_headers-0.12-py2-none-any.whl        
ipython-2.1.0-py2-none-any.whl              
pyflakes-0.8.1-py2.py3-none-any.whl
django_debug_toolbar-1.2.1-py2.py3-none-any.whl  
Jinja2-2.7.2-py2-none-any.whl               
Pygments-1.6-py2-none-any.whl
django_extensions-1.3.7-py2.py3-none-any.whl     
Markdown-2.4-py2-none-any.whl               
six-1.6.1-py2.py3-none-any.whl
django_model_utils-2.0.3-py2.py3-none-any.whl    
MarkupSafe-0.23-cp27-none-linux_x86_64.whl  
Sphinx-1.2.2-py27-none-any.whl
djangorestframework-2.3.13-py2.py3-none-any.whl  
mccabe-0.2.1-py2-none-any.whl               
sqlparse-0.1.11-py2-none-any.whl
```
This shows pretty well the format of wheel filenames:

> {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl

The platform tag part is important, as a wheel compiled on mac will not work on an Ubuntu machine for example.

To install my requirements from my wheels, I simply need to tell pip where to look for:

```bash
$ pip install --use-wheel --no-index --find-links=wheelhouse/ -r requirements/local.txt
``` 
The `no-index` part flag ensures that pip won't try to look it up in others sources than the directory we specify in find-links.
Delete your virtualenv and see how fast it is to install now (apparently wheel ignores URLs though, you could install the wheel file manually as explained above).  

This is roughly the workflow with using wheels for your project.  

Wheels definitely look like a win for every environment:

- dev: instant installation of most of your pip packages across your projects if you are using a shared wheel directory
- ci: faster build and not reliant on pypi
- prod: not reliant on pypi to deploy 
