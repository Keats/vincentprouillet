+++
title = "Python testing: Factory Boy or Model Mommy"
path = " using-factory-boy-or-model-mommy"
description = "Pros/cons of each"
date = 2014-04-05
category = "Programming"
tags = ["python"]

[extra]
updated = "2014-07-25"
+++


Writing tests is necessary.  
Whether you write them before the code itself (TDD, BDD) or after, it allows you to refactor and change your code with confidence (nobody wants to refactor a critical feature with no coverage).  
One thing you need very frequently in tests is objects.  
There's several choices when it comes to how you can create objects for your tests:

- Fixtures: objects are stored as json or another filetype and loaded for tests. This is a bad idea as you need to update your fixtures everytime you modify your models
- ORM: you could for example use MyModel.objects.create in Django to create your object in the database. Much cleaner than fixtures but you will repeat yourself quite a bit.
- Factories: that's what the article is about, define a template once (or not at all with Model Mommy) and you can use the factory in all your tests.

You could create your own factory system based on the ORM but there are libraries that already do that, and do it well so there's no point reinventing the wheel.  
All the examples below will be for Django tests and we are going to make factories for the following models:

```python
# This is pseudocode, in reality that would be your django or SQLAlchemy models
class Teashop(object):
    name = string
    address = string
    owner = Owner

class Owner(object):
    first_name = string
    last_name = string
    email = string
    age = int
```

## Factory Boy
 is based on factory_girl for those of you that used it in Ruby.  
Using it is very simple, define your factory by creating a class that inherits from the class you want to use (it supports several ORM, mainly Django and SQLAlchemy).  
It brings lots of cool features like lazy attributes, fuzzy attributes,  sequences and more.  

Let's see how the factories would work for our models:

```python
class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Owner

    first_name = 'bobby'
    last_name = 'D'
    # age will be somewhere between 25 and 42
    age = FuzzyInteger(25, 42)
    # email will use first_name and last_name (the default or the one you provide)
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())

class TeashopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Teashop

    name = 'Tea-Bone'
    # the first teashop will be 0 Downing street, the second 1 Downing Street etc
    address = factory.Sequence(lambda n: '{0} Downing Street'.format(n))
    owner = factory.SubFactory(OwnerFactory)
```

Now, to use it in your tests, it's very simple:

```python
>>> OwnerFactory() # will save into database and return an instance of the model
>>> OwnerFactory.create() # same as above
>>> OwnerFactory.build() # will create the object but not save it in database, very cool for unit tests
>>> OwnerFactory(first_name='Malcom') # override the default first name we defined in the factory
>>> TeashopFactory() # will create both a teashop and an associated owner model and return the teashop
>>> TeashopFactory(owner=my_owner_object) # will use the Owner object provided instead of creating one
```

Factory boy also provides hooks if you need to modify the object or save some properties in another database.

## Model Mommy
[Model Mommy](https://github.com/vandersonmota/model_mommy) is an extremely simple way to create objects for tests in Django (and Django only).  
Look at that:

```python
>>> mommy.make(Owner) # identical to .create() in factory boy
>>> mommy.make(Teashop) # will create and save the teashop and the owner
>>> mommy.prepare(Owner) # create but not save in the database
```

And yes, there's nothing else to define. Model mommy will automatically fill the objects attributes with random data corresponding to the type of column in the ORM.  
You can obviously define the attributes manually if you want, even for related objects:  

```python
>>> mommy.make(Owner, first_name='Malcolm')
>>> mommy.make(Teashop, owner__first_name='Malcom') # AWESOME
>>> mommy.make(Teashop, _quantity=7) # creates and return 7 teashop objects, everyone gets a teashop!
```

You might be thinking that having random data in your tests can be a bad idea (I tend to agree) and annoying to track down bugs (it's hard to see that sdawrewaev is a first name).  
Thankfully, Model Mommy provides a way to set predefined data called recipes, with several examples in the [doc](https://github.com/vandersonmota/model_mommy#recipes).  
It doesn't have lazy attributes though.  

## Which one should I use?
If you are using something other than Django, the choice is easy and you should use Factory Boy if possible.  
If you are using Django, things are pretty much down to your personal preference as both do a good job providing models for your tests.  
I really like how simple it is to use Model Mommy and the ORM syntax to edit relationship attributes but since I don't want random data, I would always use recipes and I might as well use Factory Boy.  
In the end I use Factory Boy, the explicit declaration and the possibility of using the same tool on a Flask or Pyramid project makes it very attractive.  
