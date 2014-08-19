#Django-Front-Edit

##Description

A front end editing app for Django. This app allows one to edit dynamic data on
the front end of a website when logged in as a staff member. The app allows
the editing of dynamic content within any element (See Example below).

##Installation

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

In your main urls.py file:

    ...
    url(r'', include('front_edit.urls')),
    ...

There is nothing to syncdb or migrate.

##Usage

This app uses template tags for all its functionality.

###Template tags

Make sure to load up front\_edit\_tags in your template.

> **Edit...EndEdit**
>> **Arguments:** object.field...[class\_name]

>> **object.field:** This argument consist of multiple arguments of dot separated
object/field variables. Currently only fields within the same model object can
be edited per tag.

>> **class\_name:** This optional argument is the class name(s) to put on the
form, edit button, and overlay in case you need to adjust them.

>> This tag specifies an editable region.

> **EditLoader**
>> **Arguments:** None

>> This tag includes all the boilerplate to make the front-end editing work.
This tag should always be right before the end `<body>` tag in your base template.

###JavaScript

There is one command that you can call if you need to reposition the edit elements.
You should call this if any JavaScript will change the offset of in-flow elements.

    $.front_edit('refresh');

###Example

    {% load front_edit_tags %}
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <div>
            <!-- In a list -->
            <ul>
                {% for object in objects %}
                {% edit object.text_field object.char_field "class_name" %}
                <li>
                    <span>{{ object.text_field }}</span>
                    <span>{{ object.char_field }}</span>
                </li>
                {% endedit %}
                {% endfor %}
            </ul>
            <!-- In a table -->
            <table>
                <tbody>
                    <tr>
                        {% for object in objects %}
                        {% edit object.text_field object.char_field "class_name" %}
                        <td>
                            <span>{{ object.text_field }}</span>
                            <span>{{ object.char_field }}</span>
                        </td>
                        {% endedit %}
                        {% endfor %}
                    </tr>
                </tbody>
            </table>
        </div>
        <div>
            <!-- On a span -->
            {% edit object.text_field "class_name" %}
            <span>{{ object.text_field }}</span>
            {% endedit %{
        </div>
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

##Custom Media and JS variables

If the FRONT\_EDIT\_CUSTOM\_FIELDS setting doesn't satisfy your needs you will
need to do the following.

1. Change FRONT\_EDIT\_LOADER\_TEMPLATE to your own template, it should
have a different name than 'front_edit/loader.html'.

2. In your template extend 'front_edit/loader.html'.

3. Use the block 'ft\_extra' to set or run javascript code. No script tags
are needed.

4. Use the block 'ft\_extra\_media' to define media such as CSS or JS files.
