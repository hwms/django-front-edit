# Django-Front-Edit

## Description

A front end editing app for Django. This app allows one to edit dynamic data on the front end of a website when logged in as a staff member. The app allows the editing of dynamic content within any element (See Example below).

## Installation

You must have setuptools installed.

From PyPI:

    pip install django_front_edit

Or download a package from the [PyPI][PyPI Page] or the [BitBucket page][Bit Page]:

    pip install <package>

Or unpack the package and:

    python setup.py install.

[PyPI Page]: https://pypi.python.org/pypi/django_front_edit
[Bit Page]: https://bitbucket.org/dwaiter/django-front-edit/downloads

## Dependencies

Django >= 1.4 and its dependencies.

beautifulsoup4 >= 4.3.2 located at: [http://www.crummy.com/software/BeautifulSoup/][home soup] or
[https://pypi.python.org/pypi/beautifulsoup4/][pypi soup].

django-classy-tags >= 0.5.1 located at: [https://github.com/ojii/django-classy-tags][git classy] or
[https://pypi.python.org/pypi/django-classy-tags][pypi classy].

**and either one of the following:** (see `FRONT_EDIT_HTML_PARSER` setting below)

html5lib >= 0.999, != 0.9999, != 1.0b5, != 0.99999, != 1.0b6 located at: [https://github.com/html5lib/html5lib-python][git html] or
[https://pypi.python.org/pypi/html5lib][pypi html].

lxml located at: [https://github.com/lxml/lxml][git lxml] or
[https://pypi.python.org/pypi/lxml][pypi lxml]

[home soup]: http://www.crummy.com/software/BeautifulSoup/
[pypi soup]: https://pypi.python.org/pypi/beautifulsoup4/

[git classy]: https://github.com/ojii/django-classy-tags
[pypi classy]: https://pypi.python.org/pypi/django-classy-tags

[git html]: https://github.com/html5lib/html5lib-python
[pypi html]: https://pypi.python.org/pypi/html5lib

[git lxml]: https://github.com/lxml/lxml
[pypi lxml]: https://pypi.python.org/pypi/lxml

## Integration
In your Django settings.py file insert the following in an appropriate place:

    ...
    # for django >1.4 <1.8
    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.contrib.auth.context_processors.auth',
        ...
        'django.core.context_processors.request',
        ...
        'front_edit.context_processors.defer_edit'
    ]
    # or for django >1.8
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    ...
                    'django.template.context_processors.request',
                    ...
                    'front_edit.context_processors.defer_edit'
                ]
            }
        }
    ]
    ...

    INSTALLED_APPS = [
        ...
        'django.contrib.contenttypes',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.sessions',
        ...
        'front_edit',
        ...
    ]

    ...

In your main urls.py file:

    ...
    url(r'', include('front_edit.urls')),
    ...

There is nothing to syncdb or migrate.

## Usage

This app uses template tags for all its functionality.

### Template tags

Make sure to load up `front_edit_tags` in your template.

#### Edit...EndEdit

> **Arguments:** object.field... [class\_name]

> **object.field:** This argument consist of multiple arguments of dot separated object/field variables. Currently only fields within the same model object can be edited per tag.
> **class\_name:** This optional argument is the class name(s) to put on the form, edit button, and overlay in case you need to adjust them.

This tag specifies an editable region.


#### EditLink...EndEditLink

> **Arguments:** admin_url, [class\_name]

> **admin_url:** A URL string to link to.
> **class\_name:** This optional argument is the class name(s) to put on the form, edit button, and overlay in case you need to adjust them.

This tag specifies an editable region that will link to an admin page instead of editing inline. For example:

```
{% url 'admin:constance_config_changelist' as admin_url %}
{% edit_link admin_url %}
    <div>{{ config.FOO }}</div>
{% endedit_link %}
```


#### EditWithHints...EndEditWithHints

> **Arguments:** None

This tag is used to make editable each object in a collection of pagelets each marked with **EditHint** tags.


#### EditHint

> **Arguments:** object fields [class\_name]

> **object:** A model instance.
> **fields:** A list of fields on this model, i.e. 'field1,field2,...,fieldN'
> **class\_name:** This optional argument is the class name(s) to put on the form, edit button, and overlay in case you need to adjust them.

This tag adds a hint to a small cacheable template used in a pagelet system.


#### EditLoader
> **Arguments:** None

This tag includes all the boilerplate to make the front-end editing work. This tag should always be right before the end `<body>` tag in your base template.


### JavaScript

There is one command that you can call if you need to reposition the edit elements.
You should call this if any JavaScript will change the offset of in-flow elements.

    djangoFrontEdit.refresh();

### Example

    pagelet_text.html
    {% load front_edit_tags %}
    <div class="pagelet pagelet-text" {% edit_hint instance "title,content" "class_name" %}>
        <div class="title">
            {{ instance.title }}
        </div>
        <div class="richtext">
            {{ instance.content|safe }}
        </div>
    </div>

    pagelet_image.html
    {% load front_edit_tags %}
    <div class="pagelet pagelet-image" {% edit_hint instance "image,caption" "class_name" %}>
        <div class="image">
            <img src="{{ instance.image.url }}"/>
            <div class="caption">
                {{ instance.caption }}
            </div>
        </div>
    </div>

    somepage.html
    {% load front_edit_tags pagelet_tags %}
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
        <!-- in a pagelet system -->
        <div>
            {% edit_with_hints %}
            {% render_pagelets object.pagelets %}
            {% endedit_with_hints %}
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

# Advanced

## Settings

> Settings can be set by using the individual settings or by specifying a
dictionary as follows:

                FRONT_EDIT_SETTINGS = {
                    'CUSTOM_FIELDS':['path.to.custom.field'],
                    ...
                    'USE_HINTS':True,
                }

### FRONT\_EDIT\_CUSTOM\_FIELDS
> **Default:** []

> A list of dot-separated paths to a custom model field such as a rich text field
or file field that has a Media class on its widget.

### FRONT\_EDIT\_DEFER\_KEY
> **Default:** '\_\_front\_edit\_defer'

> The context key used to defer display of the collective editable loader
templates.

### FRONT\_EDIT\_EDITABLE\_TEMPLATE
> **Default:** 'front\_edit/includes/editable.html'

> This template is the editable. Which includes the form, edit button, and
overlay.

### FRONT\_EDIT\_HTML\_PARSER
> **Default:** 'html5lib'

> Change the html parser used by beautifulsoup. By default we use 'html5lib',
but we also support 'lxml'. You will have to install either of those libraries.
We do not support the builtin 'html.parser' library due to incompatibilities.

### FRONT\_EDIT\_INLINE\_EDITING\_ENABLED
> **Default:** True

> Option to disable inline editing.

### FRONT\_EDIT\_JQUERY\_BACKUP
> **Default:** 'front_edit/js/jquery.min.js'

> The path to the static jquery backup library if the CDN is down. The value
> is passed through the `static` tag.

### FRONT\_EDIT\_JQUERY\_BUILTIN
> **Default:** True

> Whether or not to use the builtin jquery library or rely on the library
> already being present in the final document.

### FRONT\_EDIT\_JQUERY\_CDN
> **Default:** '//ajax.googleapis.com/ajax/libs/jquery/'

> The url to the CDN to use for jquery. The version and file name are appended.
> i.e. path/1.11.2/jquery.min.js

### FRONT\_EDIT\_JQUERY\_VERSION
> **Default:** '1.11.2'

> The default version of jquery to fetch from the CDN.

### FRONT\_EDIT\_LOADER\_TEMPLATE
> **Default:** 'front\_edit/loader.html'

> This template is the main boilerplate.

### FRONT\_EDIT\_LOGOUT\_URL\_NAME
> **Default:** 'admin:logout'

> Set the name of the logout url.

### FRONT\_EDIT\_TOOLBAR\_TEMPLATE
> **Default:** 'front\_edit/includes/toolbar.html'

> This template is the admin toolbar.

### FRONT\_EDIT\_USE\_HINTS
> **Default:** False

> Whether or not to activate the use of **EditHint** tags. **VIGENERE_KEY** is
required when this is True.

### FRONT\_EDIT\_VIGENERE\_KEY
> **Default:** None

> A vigenere key used to obfuscate edit hints. Optional.

## Custom Media and JS variables

If the FRONT\_EDIT\_CUSTOM\_FIELDS setting doesn't satisfy your needs you will
need to do the following.

1. Change FRONT\_EDIT\_LOADER\_TEMPLATE to your own template, it should
have a different name than 'front_edit/loader.html'.

2. In your template extend 'front_edit/loader.html'.

3. Use the block 'ft\_extra' to set or run javascript code. No script tags
are needed.

4. Use the block 'ft\_extra\_media' to define media such as CSS or JS files.
