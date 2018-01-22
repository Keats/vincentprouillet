+++
title = "Class-based views VS function-based views"
path = "using-class-based-views"
description = "What are the pros/cons of CBV and FBV in Django"
date = 2013-10-02
category = "Programming"
tags = ["python", "django"]
+++

The URL gives me away.  
I do prefer class-based views (CBV) over function-based views (FBV) and will try to explain why in this article.

## Presentation of CBV
First thing, a quick introduction of CBV.  
The 'old' way of doings views in django is something like the following:

```python
def myview(request):
  if request.POST:
    # do my POST action (form, saving)
  else:
    # do my GET action

  return render(...)
```

An identical version using CBV would be:

```python
class MyView(View):
  def get(self, request, *args, **kwargs):  
    # do my get action
  def post(self, request, *args, **kwargs):  
    # do my post action
```

The main advantage of using CBV lies in being able to inherit from mixins and making the code much more compact and readable (
this is obviously from my point of view, some people won't like the fact that they don't see exactly what's happening).  
For example, let's say you want to process a form (very basic one, on GET returns the form, on POST check for errors and show them if 
necessary or do something and redirect to another URL in case of success).  

In a FBV, processing such a form looks like that:

```python
def myview(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            do_something(form)
            return HttpResponseRedirect(reverse('success'))
    else:
        form = MyForm()

    return render(request, 'template.html', {'form': form}) 
```

And in a CBV

```python
class MyView(FormView):
  form_class = MyForm
  success_url = reverse_lazy('success')
  template_name = 'template.html'

  def form_valid(self, form):
    do_something(form)
    return super(MyView, self).form_valid(form)
```

This is so much neater imo.  

## Go CBV !
There are generic classes for every CRUD action and it's easy to create your own mixins on top of it.  
The most common would be a LoginRequired one, working like the login_required decorator.  
A JsonResponse one is also a good example of a useful CBV mixin (for more, look at [django-braces](https://github.com/brack3t/django-braces "django-braces")).  

One pattern that we use all the time in Hizard (and most web app need the same kind of features) is checking that the user is allowed to see/do certains actions.  
In this case, we have mixins like RestrictedDetailView, RestrictedListView, etc that does the check automatically for us, the only thing we have to do is inheriting from them.  
How cool is that ?  
Instead of having huge FBV unorganized (I've seen in the hundreds of line unfortunately), you can divide everything into methods neatly and have much cleaner and easier to read code.  

## FBV is not dead !
FBV is the traditional way to represent requests handling in lots of frameworks/languages, making it *much* easier for a new django dev to understand what's going on.  
On some cases, it even makes more sense to use them rather than FBV (I'm thinking about views with several forms for example).  
You also need to take into account that most current codebase use FBV and lots of developers don't know how/don't want to use CBV.  

## Conclusion
Seeing the number of people not liking CBV, I assume I'm in the minority of people that thinks they are a fantastic tool to make your code cleaner, reusable and easier to maintain (you want to add another check on your LoginRequired ? much more annoying to do with decorators and FBV).  
Even if you're not using generic CBV, just using a CBV inheriting from View will cleanly separate GET and POST.  
The main problem with CBV is the documentation I think but once you get the hang of it, it's awesome.
In the end it's a matter of preference and what the team decides : I use CBV on my own projects and FBV at work.  
