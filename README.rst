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
    
Settings
--------

django-passwords adds 6 optional settings

Optional:
    Specifies minimum length for passwords::

        PASSWORD_MIN_LENGTH = 6 # Defaults to 6

    Specifies maximum length for passwords::

        PASSWORD_MAX_LENGTH = 120 # Defaults to None

    Specifies the location of a dictionary (file with one word per line)::

        PASSWORD_DICTIONARY = "/usr/share/dict/words" # Defaults to None

    Specifies how close a fuzzy match has to be to be considered a match::

        PASSWORD_MATCH_THRESHOLD = 0.9 # Defaults to 0.9, should be 0.0 - 1.0 where 1.0 means exactly the same.

    Specifies a list of common sequences to attempt to match a password against::

        PASSWORD_COMMON_SEQUENCES = [] # Should be a list of strings, see passwords/validators.py for default

    Specifies number of characters within various sets that a password must contain::

        PASSWORD_COMPLEXITY = { # You can ommit any or all of these for no limit for that particular set
            "UPPER": 1,       # Uppercase
            "LOWER": 1,       # Lowercase
            "DIGITS": 1,      # Digits
            "PUNCTUATION": 1, # Punctuation (string.punctuation)
            "NON ASCII": 1,   # Non Ascii (ord() >= 128)
            "WORDS": 1        # Words (substrings seperates by a whitespace)
        }

Usage
-----

    To use the formfield simply import it and use it::

        from django import forms
        from passwords.fields import PasswordField

        class ExampleForm(forms.Form):
            password = PasswordField(label="Password")
