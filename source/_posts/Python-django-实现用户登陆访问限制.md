---
title: Python_django_实现用户登陆访问限制
date: 2017-08-02 19:44:41
categories: Python
tags:
    - Python
    - Django
comments: false
---

## Limiting access to logged-in users
### The raw way
The simple, raw way to limit access to pages is to check [request.user.is_authenticated](https://docs.djangoproject.com/en/1.10/ref/contrib/auth/#django.contrib.auth.models.User.is_authenticated) and either redirect to a login page:
```python
from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
```
…or display an error message:
```python
from django.shortcuts import render

def my_view(request):
    if not request.user.is_authenticated:
        return render(request, 'myapp/login_error.html')
    # ...
```

### The login_required decorator
login_required(redirect_field_name=’next’, login_url=None)[[source]](https://docs.djangoproject.com/en/1.10/_modules/django/contrib/auth/decorators/#login_required)
As a shortcut, you can use the convenient login_required() decorator:
```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...
```
login_required() does the following:
- If the user isn’t logged in, redirect to settings.LOGIN_URL, passing the current absolute path in the query string. Example: **/accounts/login/?next=/polls/3/**.
- If the user is logged in, execute the view normally. The view code is free to assume the user is logged in.
By default, the path that the user should be redirected to upon successful authentication is stored in a query string parameter called **"next"**. If you would prefer to use a different name for this parameter, login_required() takes an optional **redirect_field_name** parameter:
```python
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='my_redirect_field')
def my_view(request):
    ...
```
Note that if you provide a value to redirect_field_name, you will most likely need to customize your login template as well, since the template context variable which stores the redirect path will use the value of redirect_field_name as its key rather than "next" (the default).

login_required() also takes an optional login_url parameter. Example:
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def my_view(request):
    ...
```
Note that if you don’t specify the **login_url parameter**, you’ll need to ensure that the **settings.LOGIN_URL** and your login view are properly associated. For example, using the defaults, add the following lines to your URLconf:
```python
from django.contrib.auth import views as auth_views

url(r'^accounts/login/$', auth_views.login),
```
settings.LOGIN_URL like this:
```python
...
LOGIN_URL = '/accounts/login/'  #这个路径需要根据你网站的实际登陆地址来设置
...
```

The settings.LOGIN_URL also accepts view function names and named URL patterns. This allows you to freely remap your login view within your URLconf without having to update the setting.
> Note
The login_required decorator does NOT check the is_active flag on a user, but the default AUTHENTICATION_BACKENDS reject inactive users.

> See also
If you are writing custom views for Django’s admin (or need the same authorization check that the built-in views use), you may find the django.contrib.admin.views.decorators.staff_member_required() decorator a useful alternative to login_required().

## Limiting permissions to users
**permission_required** similer to login_required
```python
from django.contrib.auth.decorators import permission_required
...
@permission_required('xxx.view_myview')
def my_view(request):
    ...
```

## Source code

### login_required
```python
def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
```

### permission_required
```python
def permission_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(perm, six.string_types):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)
```

ref:
[https://docs.djangoproject.com/en/1.10/topics/auth/default/#the-login-required-decorator](https://docs.djangoproject.com/en/1.10/topics/auth/default/#the-login-required-decorator)
