#Installation

You must have setuptools installed.

From PyPI:

    pip install django_front_edit

Or download a package from the [PyPI][PyPI Page] or the [BitBucket page][Bit Page]:

    pip install <package>

Or unpack the package and:

    python setup.py install.

[PyPI Page]: https://pypi.python.org/pypi/django_front_edit
[Bit Page]: https://bitbucket.org/dwaiter/django-front-edit/downloads

##Dependencies

Django >= 1.4 and its dependencies.

beautifulsoup4 >= 4.3.2 located at: [http://www.crummy.com/software/BeautifulSoup/][home soup] or
[https://pypi.python.org/pypi/beautifulsoup4/][pypi soup].

django-classy-tags >= 0.5.1 located at: [https://github.com/ojii/django-classy-tags][git classy] or
[https://pypi.python.org/pypi/django-classy-tags][pypi classy].

[home soup]: http://www.crummy.com/software/BeautifulSoup/
[pypi soup]: https://pypi.python.org/pypi/beautifulsoup4/

[git classy]: https://github.com/ojii/django-classy-tags
[pypi classy]: https://pypi.python.org/pypi/django-classy-tags


##Integration
In your Django settings.py file insert the following in an appropriate place:

    ...
    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.contrib.auth.context_processors.auth',
        ...
        'django.core.context_processors.request',
        ...
        'front_edit.context_processors.defer_edit'
    ]
    ...

    INSTALLED_APPS = [
        ...
        "front_edit",
        ...
    ]

    ...

There is nothing to syncdb or migrate.

##Usage

This app uses template tags for all its functionality.

###Template tags

Make sure to load up front\_edit\_tags in your template.

> ####Edit...EndEdit
>> **Arguments:** object.field...[class\_name]

>> **object.field:** This argument consist of multiple arguments of dot separated
object/field variables.

>> **class\_name:** This optional argument is the class name(s) to put on the
form, edit button, and overlay in case you need to adjust them.

>> This tag specifies an editable region.

> ####EditLoader
>> **Arguments:** None

>> This tag includes all the boilerplate to make the front-end editing work.
This tag should always be right before the end `<body>` tag in your base template.

###Example

    {% load front_edit_tags %}
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        {% edit object.text_field object.char_field "class_name" %}
        <div>
            <span>{{ object.text_field }}</span>
            <span>{{ object.char_field }}</span>
        </div>
        {% endedit %}
        {% edit_loader %}
    </body>
    </html>

#Advanced

##Settings

###FRONT\_EDIT\_LOGOUT\_URL\_NAME
> **Default:** "admin:logout"

> Set the name of the logout url.

###FRONT\_EDIT\_CUSTOM\_FIELDS
> **Default:** []

> A list of dot-separated paths to a custom model field such as a rich text field
or file field that has a Media class on its widget.

###FRONT\_EDIT\_INLINE\_EDITING\_ENABLED
> **Default:** True

> Option to disable inline editing.

###FRONT\_EDIT\_LOADER\_TEMPLATE
> **Default:**'front\_edit/loader.html'

> This template is the main boilerplate.

###FRONT\_EDIT\_TOOLBAR\_TEMPLATE
> **Default:** 'front\_edit/includes/toolbar.html'

> This template is the admin toolbar.

###FRONT\_EDIT\_EDITABLE\_TEMPLATE
> **Default:** 'front\_edit/includes/editable.html'

> This template is the editable. Which includes the form, edit button, and overlay.
