from django.forms import CharField, PasswordInput
from django.utils.translation import ugettext_lazy as _

from passwords.validators import (validate_length, common_sequences,
                                  dictionary_words, complexity,
                                  PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)


class PasswordField(CharField):

    default_validators = [
        validate_length,
        common_sequences,
        dictionary_words,
        complexity]

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            attrs = {}

            # 'minlength' is poorly supported, so use 'pattern' instead.
            # See http://stackoverflow.com/a/10294291/25507,
            # http://caniuse.com/#feat=input-minlength.
            if PASSWORD_MIN_LENGTH and PASSWORD_MAX_LENGTH:
                attrs['pattern'] = ('.{%i,%i}' %
                                    (PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH))
                attrs['title'] = (_('%i to %i characters') %
                                  (PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH))
            elif PASSWORD_MIN_LENGTH:
                attrs['pattern'] = '.{%i,}' % PASSWORD_MIN_LENGTH
                attrs['title'] = _('%i characters minimum') % PASSWORD_MIN_LENGTH

            if PASSWORD_MAX_LENGTH:
                attrs['maxlength'] = PASSWORD_MAX_LENGTH

            kwargs["widget"] = PasswordInput(render_value=False, attrs=attrs)

        super(PasswordField, self).__init__(*args, **kwargs)
