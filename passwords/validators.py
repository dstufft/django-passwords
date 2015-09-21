# coding=utf-8
from __future__ import division, unicode_literals

import string
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
try:
    from django.utils.encoding import smart_text
except ImportError:  # django < 1.4.2
    from django.utils.encoding import smart_unicode as smart_text


COMMON_SEQUENCES = [
    "0123456789",
    "`1234567890-=",
    "~!@#$%^&*()_+",
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./",
    'qwertyuiop{}|asdfghjkl;"zxcvbnm<>?',
    "qwertyuiopasdfghjklzxcvbnm",
    "1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik,9ol.0p;/-['=]\\",
    "qazwsxedcrfvtgbyhnujmikolp",
    "qwertzuiopü+asdfghjklöä#<yxcvbnm,.-",
    "qwertzuiopü*asdfghjklöä'>yxcvbnm;:_",
    "qaywsxedcrfvtgbzhnujmikolp",
]

# Settings
PASSWORD_MIN_LENGTH = getattr(
    settings, "PASSWORD_MIN_LENGTH", 6)
PASSWORD_MAX_LENGTH = getattr(
    settings, "PASSWORD_MAX_LENGTH", None)
PASSWORD_DICTIONARY = getattr(
    settings, "PASSWORD_DICTIONARY", None)
PASSWORD_MATCH_THRESHOLD = getattr(
    settings, "PASSWORD_MATCH_THRESHOLD", 0.9)
PASSWORD_COMMON_SEQUENCES = getattr(
    settings, "PASSWORD_COMMON_SEQUENCES", COMMON_SEQUENCES)
PASSWORD_COMPLEXITY = getattr(
    settings, "PASSWORD_COMPLEXITY", None)


class LengthValidator(object):
    message = _("Invalid Length (%s)")
    code = "length"

    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value):
        err = None
        if self.min_length is not None and len(value) < self.min_length:
            err = _("Must be %s characters or more") % self.min_length
        elif self.max_length is not None and len(value) > self.max_length:
            err = _("Must be %s characters or less") % self.max_length

        if err is not None:
            raise ValidationError(self.message % err, code=self.code)


class ComplexityValidator(object):
    message = _("Must be more complex (%s)")
    code = "complexity"

    def __init__(self, complexities):
        self.complexities = complexities

    def __call__(self, value):
        if self.complexities is None:
            return

        uppercase, lowercase, letters = set(), set(), set()
        digits, special, punctuation = set(), set(), set()

        for character in value:
            if character.isupper():
                uppercase.add(character)
                letters.add(character)
            elif character.islower():
                lowercase.add(character)
                letters.add(character)
            elif character.isdigit():
                digits.add(character)
            elif character in string.punctuation:
                punctuation.add(character)
            elif not character.isspace():
                special.add(character)

        words = set(re.findall(r'\b\w+', value, re.UNICODE))

        errors = []
        if len(uppercase) < self.complexities.get("UPPER", 0):
            errors.append(
                _("must contain %(UPPER)s or more unique uppercase characters") %
                self.complexities)
        if len(lowercase) < self.complexities.get("LOWER", 0):
            errors.append(
                _("must contain %(LOWER)s or more unique lowercase characters") %
                self.complexities)
        if len(letters) < self.complexities.get("LETTERS", 0):
            errors.append(
                _("must contain %(LETTERS)s or more unique letters") %
                self.complexities)
        if len(digits) < self.complexities.get("DIGITS", 0):
            errors.append(
                _("must contain %(DIGITS)s or more unique digits") %
                self.complexities)
        if len(punctuation) < self.complexities.get("PUNCTUATION", 0):
            errors.append(
                (_("must contain %(PUNCTUATION)s or more unique punctuation characters: %%s"
                  ) % self.complexities) % string.punctuation)
        if len(special) < self.complexities.get("SPECIAL", 0):
            errors.append(
                _("must contain %(SPECIAL)s or more non unique special characters") %
                self.complexities)
        if len(words) < self.complexities.get("WORDS", 0):
            errors.append(
                _("must contain %(WORDS)s or more unique words") %
                self.complexities)

        if errors:
            raise ValidationError(self.message % (u', '.join(errors),),
                                  code=self.code)



class BaseSimilarityValidator(object):
    message = _("Too Similar to [%(haystacks)s]")
    code = "similarity"

    def __init__(self, haystacks=None, threshold=None):
        self.haystacks = haystacks if haystacks else []
        if threshold is None:
            self.threshold = PASSWORD_MATCH_THRESHOLD
        else:
            self.threshold = threshold

    def fuzzy_substring(self, needle, haystack):
        needle, haystack = needle.lower(), haystack.lower()
        m, n = len(needle), len(haystack)

        if m == 1:
            if needle not in haystack:
                return -1
        if n == 0:
            return m

        row1 = [0] * (n + 1)
        for i in range(0, m):
            row2 = [i + 1]
            for j in range(0, n):
                cost = 1 if needle[i] != haystack[j] else 0
                row2.append(min(
                    row1[j + 1] + 1,
                    row2[j] + 1,
                    row1[j] + cost))
            row1 = row2
        return min(row1)

    def __call__(self, value):
        for haystack in self.haystacks:
            distance = self.fuzzy_substring(value, haystack)
            longest = max(len(value), len(haystack))
            similarity = (longest - distance) / longest
            if similarity >= self.threshold:
                raise ValidationError(
                    self.message % {"haystacks": ", ".join(self.haystacks)},
                    code=self.code)


class DictionaryValidator(BaseSimilarityValidator):
    message = _("Based on a dictionary word")
    code = "dictionary_word"

    def __init__(self, words=None, dictionary=None, threshold=None):
        haystacks = []
        if dictionary:
            words = self.get_dictionary_words(dictionary)
        if words:
            haystacks.extend(words)
        super(DictionaryValidator, self).__init__(
            haystacks=haystacks,
            threshold=threshold)

    def get_dictionary_words(self, dictionary):
        with open(dictionary) as dictionary:
            return [smart_text(x.strip()) for x in dictionary.readlines()]


class CommonSequenceValidator(BaseSimilarityValidator):
    message = _("Based on a common sequence of characters")
    code = "common_sequence"


validate_length = LengthValidator(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
complexity = ComplexityValidator(PASSWORD_COMPLEXITY)
dictionary_words = DictionaryValidator(dictionary=PASSWORD_DICTIONARY)
common_sequences = CommonSequenceValidator(PASSWORD_COMMON_SEQUENCES)
