# -*- coding: utf8 -*-

from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.forms import PasswordInput, TimeInput, CharField
from passwords import fields, validators
from unittest import TestCase


class TestFields(TestCase):

    def test_default_widget(self):
        p = fields.PasswordField()
        assert isinstance(p.widget, PasswordInput)

        p = fields.PasswordField(widget=TimeInput())
        assert isinstance(p.widget, TimeInput)

    def test_widget_attributes(self):
        p = fields.PasswordField()
        # Verify that our default minimum length creates some sort of HTML5
        # validation.
        self.assertTrue(
            'minlength' in p.widget.attrs or 'pattern' in p.widget.attrs)

    def test_default_validation(self):
        # because our tests/__init__ has not provided any configuration to
        # Django, we get default behaviour here.
        p = fields.PasswordField()
        p.clean('password')  # robust defaults it seems

    def test_using_validators_on_other_fields(self):
        dict_validator = validators.DictionaryValidator(
            words=['nostromo'],
            threshold=0.8)
        length_validator = validators.LengthValidator(
            min_length=2)

        p = CharField(validators=[dict_validator, length_validator])

        p.clean('aa')
        with self.assertRaises(ValidationError):
            p.clean('a')  # too short
        with self.assertRaises(ValidationError):
            p.clean('nostrilomo')  # too much like nostromo
