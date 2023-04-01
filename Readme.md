
# A tutorial to `social-auth-app-django`

[`python-social-auth`](https://github.com/python-social-auth/) is a
powerful set of modules to give developers easy access to many
authentication platforms for their projects.

However, I found the initial contact not so easy - this is why I
started to experiment "from scratch", and wrote this tutorial
alongside.

The purpose is to setup the initial steps of a
from-scratch [Django](https://www.djangoproject.com/) 
project, to allow integration of social-based authentication to your
site. The project will stop at login / logout / hello-world kind of
stage.


# `userdemo` project

It all started with:

``` shell
django-admin startproject userdemo
```

## First step: always start with deriving the User model

It is recommended in the 
[Django doc](https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model),
where you will find instructions to do so. The point is to create a
custom User model *before* to apply the first migration; doing it
later exposes you to painful manual data migration.

So you create an app:

``` shell
python manage.py startapp pf_core
```

In `pf_core/apps.py` you add:

``` python
    verbose_name = "Platform core"
```

then in `userdemo/settings.py`, you add `pf_core.apps.PfCoreConfig,`
to the `INSTALLED_APPS` array.

In `pf_core/models.py`, simply add:

``` python
from django.contrib.auth.models import AbstractUser

class PfUser(AbstractUser):
    pass
```

In `pf_core/admin.py`, add :

``` python
from django.contrib.auth.admin import UserAdmin

from .models import PfUser

admin.site.register(PfUser, UserAdmin)
```

And in `settings.py`, important to declare: 

``` python
AUTH_USER_MODEL = 'pf_core.PfUser'
```

Once this is done, you can finally type:

``` shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```


## Second step - "Hello, World!"

Add in `pf_core/views.py`:

``` python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, World!")
```

Create a `pf_core/urls.py` file with:

``` python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

and in `userdemo/urls.py` put:

``` python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('pf_core.urls')),
    path('admin/', admin.site.urls),
]
```

Once done, `python manage.py runserver 8000` starts a new server,
listening on port 8000.

Then `http://localhost:8000/` shoud give you "Hello, World!".

`http://localhost:8000/admin` pour se connecter au backend, avec le
compte "superuser" créé plus haut.


## At last - authentication!

The purpose is to illustrate in practice the information found in [Configuration](https://python-social-auth.readthedocs.io/en/latest/configuration/settings.html) and
[Django Framework](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html),
in the modules.

In `settings.py`, add:

``` python
INSTALLED_APPS = [
    ...
    ##
    'social_django',
    ...
]

...
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                ##
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        }}]
...

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_MICROSOFT_GRAPH_KEY = "<my key>"
SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET = "<my secret>"
SOCIAL_AUTH_MICROSOFT_GRAPH_LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.microsoft.MicrosoftOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
```

(in the final demo package, I twicked `settings.py` to use
`os.environ` and a pair of environmental variables)

Don't forget to add the default Django backend at the end, so that you
can still use the login/password of your superuser.


And in `userdemo/urls.py`: 

``` python
urlpatterns = [
    ...
    path('', include('social_django.urls', namespace='social')),
    ...
]
```

You need to add to your app declaration in
the [Microsoft portal](https://portal.azure.com/) with a return URL
`http://localhost:8000/complete/microsoft-graph` - reading the code
content in `social_django.urls`, you can understand why:

``` python
"""URLs module"""
from django.conf import settings
from django.urls import path
from social_core.utils import setting_name

from . import views

extra = getattr(settings, setting_name("TRAILING_SLASH"), True) and "/" or ""

app_name = "social"

urlpatterns = [
    # authentication / association
    path(f"login/<str:backend>{extra}", views.auth, name="begin"),
    path(f"complete/<str:backend>{extra}", views.complete, name="complete"),
    # disconnection
    path(f"disconnect/<str:backend>{extra}", views.disconnect, name="disconnect"),
    path(
        f"disconnect/<str:backend>/<int:association_id>{extra}",
        views.disconnect,
        name="disconnect_individual",
    ),
]
```

At this stage, you have and operational test platform: log in with
`http://localhost:8000/login/microsoft-graph`.
 

## Another provider?

Simply add the relevant `SOCIAL_AUTH_...` variables in `settings.py`,
as well as the backend declaration. And that's about it.



## Pipeline

In the
[personalized configuration doc](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html#personalized-configuration),
the 
[pipeline doc](https://python-social-auth.readthedocs.io/en/latest/pipeline.html),
and
in
[pipeline paragraph of introduction doc](https://python-social-auth.readthedocs.io/en/latest/developer_intro.html#understanding-the-pipeline),
you'll find nearly all you need to know about pipelines.

The thing to keep in mind: they play kind of the same role as the
middleware in Django, for authentication process: a chain of functions
to check and enrich gathered data at different steps. 

The [pipeline doc] documents the various steps - the code is also very
readable and informative. Interesting step is the one which actually
creates the user when it does not exists - comment it out if you want
to keep control on who can actually declare a new user.

There even exists a `social_core.pipeline.debug.debug` step that you
can put everywhere, that can dump data about what it is doing.


### One social account can only be linked to one user

This is checked in `social_core.pipeline.social_auth.social_user`.


## Web pages

A few tweaks in `settings.py` to allow templates in
`userdemo/templates` and to define where the static files are located,
and the declaration of a specific middleware in `pf_core.middleware`,
and the matching declaration in `pf_core.context_processors`, and we
are good to go and tune templates to allow login and logout
operations. 

For login, we follow the method described in [understanding PSA URLs](https://python-social-auth.readthedocs.io/en/latest/developer_intro.html#understanding-psa-urls): 

``` html
<a href="{% url 'social:begin' 'provider-name' %}">Login</a>
```

The various urls of the `social` domain name are set in
`social_django.urls`: 

* `begin`: to start the process; calls `/login/<provider>`

* `complete`: the callback point from provider site

* `disconnect`: to *destroy* the social auth credential

* `disconnect_individual`: not tested



For logout, very simple: call the `django.contrib.auth.logout`
function in a view, clean up the `request` object, and redirect to the
home page. See code.
