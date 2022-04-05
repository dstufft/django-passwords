.. image:: https://travis-ci.org/dstufft/django-passwords.svg?branch=master
    :target: https://travis-ci.org/dstufft/django-passwords
.. image:: https://img.shields.io/pypi/v/django-passwords.svg
    :target: https://pypi.python.org/pypi/django-passwords/
.. image:: https://img.shields.io/pypi/dm/django-passwords.svg
    :target: https://pypi.python.org/pypi/django-passwords/
.. image:: https://img.shields.io/pypi/l/django-passwords.svg
    :target: https://pypi.python.org/pypi/django-passwords/


Django Passwords
================

django-passwords is a reusable app that provides a form field and
validators that check the strength of a password.

Installation
------------

You can install django-passwords with pip by typing::

    pip install django-passwords

Or with easy_install by typing::

    easy_install django-passwords

Or manually by downloading a tarball and typing::

    python setup.py install

Compatibility
-------------

django-passwords is compatible with Django 2.2, 3.2, and 4.0. Pythons 3.7
through 3.10 are supported.

Settings
--------

django-passwords adds 6 optional settings

Optional:
    Specifies minimum length for passwords:

    .. code-block:: python

        PASSWORD_MIN_LENGTH = 6 # Defaults to 6

    Specifies maximum length for passwords:

    .. code-block:: python

        PASSWORD_MAX_LENGTH = 120 # Defaults to None

    Specifies the location of a dictionary (file with one word per line):

    .. code-block:: python

        PASSWORD_DICTIONARY = "/usr/share/dict/words" # Defaults to None

    Specifies how close a fuzzy match has to be to be considered a match:

    .. code-block:: python

        PASSWORD_MATCH_THRESHOLD = 0.9 # Defaults to 0.9, should be 0.0 - 1.0 where 1.0 means exactly the same.

    Specifies a list of common sequences to attempt to match a password against:

    .. code-block:: python

        PASSWORD_COMMON_SEQUENCES = [] # Should be a list of strings, see passwords/validators.py for default

    Specifies number of characters within various sets that a password must contain:

    .. code-block:: python

        PASSWORD_COMPLEXITY = { # You can omit any or all of these for no limit for that particular set
            "UPPER": 1,        # Uppercase
            "LOWER": 1,        # Lowercase
            "LETTERS": 1,       # Either uppercase or lowercase letters
            "DIGITS": 1,       # Digits
            "SPECIAL": 1,      # Not alphanumeric, space or punctuation character
            "WORDS": 1         # Words (alphanumeric sequences separated by a whitespace or punctuation character)
        }

Usage
-----

To use the formfield simply import it and use it:

.. code-block:: python

    from django import forms
    from passwords.fields import PasswordField

    class ExampleForm(forms.Form):
        password = PasswordField(label="Password")

You can make use of the validators on your own fields:

.. code-block:: python

    from django import forms
    from passwords.validators import dictionary_words

    field = forms.CharField(validators=[dictionary_words])

You can also create custom validator instances to specify your own
field-specific configurations, rather than using the global
configurations:

.. code-block:: python

    from django import forms
    from passwords.validators import (
        DictionaryValidator, LengthValidator, ComplexityValidator)

    field = forms.CharField(validators=[
        DictionaryValidator(words=['banned_word'], threshold=0.9),
        LengthValidator(min_length=8),
        ComplexityValidator(complexities=dict(
            UPPER=1,
            LOWER=1,
            DIGITS=1
        )),
    ])


Django's `password validation API`_ is slightly different than the form
validation API and has wrappers in the `auth_password_validators` module:

.. code-block:: python

    AUTH_PASSWORD_VALIDATORS = [
        …,
        {"NAME": "passwords.auth_password_validators.ComplexityValidator"}
    ]


.. _`password validation API`: https://docs.djangoproject.com/en/2.1/topics/auth/passwords/#password-validation
