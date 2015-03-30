from django.forms import CharField, PasswordInput

from passwords.validators import (validate_length, common_sequences,
                                  dictionary_words, complexity)


class PasswordField(CharField):

    default_validators = [
        validate_length,
        common_sequences,
        dictionary_words,
        complexity]

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs["widget"] = PasswordInput(render_value=False)

        super(PasswordField, self).__init__(*args, **kwargs)
