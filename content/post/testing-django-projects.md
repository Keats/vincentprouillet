+++
title = "Testing Django projects"
slug = "testing-django-projects"
url = "testing-django-projects"
description = "Tools and tricks I use to make tests fast and easy to write in Django projects"
date = "2013-09-02"
categories = ["programming"]
tags = ["python", "django"]
+++

## Introduction
This post will introduce what I consider the best practices when testing a Django project.  
As you've probably read 1000 times, testing is very important because without them, deploying 
is pretty much a gamble on whether something is going to break or not.  
There are a few different type of tests:

* unit tests: test a specific function, one path at a time (by path I mean if/else conditions)
* integration tests: test a whole user action, from the template to the model

What I do is unit tests all the functions I write (except the views) and integration tests for the views.  
This ensures you got everything covered.  

Whether you write the tests before the code (if you're doing TDD) or after is up to you.  
I like doing TDD for 'easy' code when I know how I am going to do it but otherwise I first write a quick draft 
that works, then code it again the TDD way.   
I found that it results in better code using that process but again it's up to you.


## Basics
### Structure
I like putting all the tests in a top level package (ie at the same level as the apps) because I find it easier 
to navigate.  
Make sure you have one test file for models, views, forms, etc rather than putting it in a single file like the 
default django does because it quickly becomes impossible to work with.

### Tools
Lots of packages exist to make testing easier.  
Here are the ones I use :

* [factory boy](http://factoryboy.readthedocs.org/en/latest/ "factory boy"): create objects easily (no more fixtures)
* [django-discover-runner](https://github.com/jezdez/django-discover-runner "django-discover-runner"): enhancement of the django test runner (to allow putting tests wherever you want), it will become
the default test runner starting 1.6
* [mock](http://mock.readthedocs.org/en/latest/ "mock"): mocking library, for when you don't really want to call some functions (usually external services), part of python standard library starting 3.3
* [django-webtest](https://pypi.python.org/pypi/django-webtest "django-webtest"): makes integration testing of views easier
* [coverage](http://nedbatchelder.com/code/coverage/ "coverage"): for when you want to know whether you're getting close to 100% coverage or not 

I also like to modify the manage.py to ensure I don't type to type the settings file to use, it looks like this :  

```python
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    if sys.argv[1] == 'test':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings.test")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
```

### Tips for having (and keeping) fast tests
Nothing is worse than having a test suite slow you down when developing (especially if you're doing TDD).  
Here are a few of the settings I use to speed it up

```python
# IN-MEMORY TEST DATABASE
# If you're not using DB specific features
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

# FAST HASHING FOR PASSWORDS
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

# Use syncdb instead of migrate if you're using South
SOUTH_TESTS_MIGRATE = False
```

Also, be careful when testing with saving objects : only do it if it's necessary (if you're using factory_boy, it means using MyFactory.build() instead 
MyFactory()).

## Testing

### A form/model
I group these 2 as they are quite similar : basically if you're writing a method on one of those (be it a custom clean() on a form or a method on a method
to deal with some business logic), it should have a test for each of the different 'paths' it contains.  
By path I mean every branch of code exists, which ideally range from 1 to 3 (more than that and it could mean that the method does too much).   
Those are unit tests, testing one thing at a time so if a test fails, there should only one possible reason.  


### A view
This is where webtest shines.  
Most of the tests I write are actually integration tests, testing thoroughly every path of each view.  
For example, for a FormView you will have 3 paths : first GET, success POST and POST with errors.  
By testing all of the branches you reduce the likelihood of unexpected exceptions (oxymoron I know, exceptions are rarely expected).  
Webtest allow you to easily login (no need for self.client.login(...) anymore), easily grab/submit forms and access the DOM.

Here's an example of testing a landing page with an email field from a model called Interest :  

```python
class PublicViewsTests(WebTest):
    def test_anonymous_can_access_landing_page(self):
        url = reverse('public:landing-page')
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_can_add_email(self):
        url = reverse('public:landing-page')
        form = self.app.get(url).form
        form['email'] = 'easy@abc.com'
        form.submit()
        self.assertEqual(Interest.objects.count(), 1)

    def test_invalid_interest_email_error(self):
        url = reverse('public:landing-page')
        form = self.app.get(url).form
        form['email'] = 'easyabc.com'
        response = form.submit().follow()

        self.assertEqual(Interest.objects.count(), 0)
        # you could look in the dom for your error class or just use assertTemplateUsed instead
        self.assertContains(response, 'invalid')
```

If I wanted to be logged in, I would just need to pass my user object as a parameter to the get, ie self.app.get(url, user=self.user) for example.


### Mocking
Sometimes you want to mock things it out. Things like call to a 3rd party service that can take time and require an internet connection.  
You do not want to mock your own services though unless you have proper integration tests somewhere. 
In the following example, I will mock a method from the Stripe API to prevent it from actually calling Stripe.    

```python
    @patch('stripe.Customer.retrieve')
    @patch.object(stripe.Customer, 'update_subscription')
    def test_subscribe_different_subscription(self, UpdateSubscriptionMock, CustomerRetrieveMock):
        """
        Changing to a different plan (or no previous plan) should call
        Stripe and save it locally
        """
        CustomerRetrieveMock.return_value = StripeTest.get_customer_response()
        UpdateSubscriptionMock.return_value = StripeTest.get_subscription_response()

        self._subscribe_user()
        StripePlanFactory(code='big')
        self.customer.subscribe('big')

        self.assertTrue(CustomerRetrieveMock.called)
        self.assertTrue(UpdateSubscriptionMock.called)
```

Mocking 2 things here : 

- a class method (stripe.Customer.retrieve)
- a method (update_subscription of stripe.Customer)

To accomplish that, you just need to add the right decorators (look into the doc for more info), add the mocks in the test parameters (order matters of course) 
and then define a return_value to these mocks.  
At the end of the tests I'm just making sure both methods were called and that's it.


## Conclusion
That's it for how I test django apps, if you want more details or have better ideas, feel free to ask/share !
