from django.forms import CharField, PasswordInput

from passwords.validators import validate_length, common_sequences, dictionary_words

class PasswordField(CharField):
    default_validators = [validate_length, common_sequences, dictionary_words]

    def __init__(self, *args, **kwargs):
        if not kwargs.has_key("widget"):
            kwargs["widget"] = PasswordInput(render_value=False)
        
        super(PasswordField, self).__init__(*args, **kwargs)