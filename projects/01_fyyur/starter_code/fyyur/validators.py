from us import states
import phonenumbers
from phonenumbers.geodata import data0, data1, data2, data3
from phonenumbers.prefix import _prefix_description_for_number
from wtforms.validators import ValidationError

from .enums import State

# Compile all US prefix mappings
# Only compile the geodata we require for US regions (1XXX) to avoid excessive memory required for metadata
US_PHONE_GEODATA = {}
for data in [data0, data1, data2, data3]:
    US_PHONE_GEODATA.update(data.data)


class GeoValidateUsPhone(object):
    ERROR_MSG = 'Invalid phone number format.'

    def __call__(self, form, field):
        # Get the selected state
        form_state = State(int(form.state.data))

        # Parse the phone number into constituent parts
        try:
            phone = phonenumbers.parse(field.data, 'US')
        except phonenumbers.NumberParseException:
            raise ValidationError(self.ERROR_MSG)

        # Check if parsed number is a valid pattern foregin (US)
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError(self.ERROR_MSG)

        # Check area prefix is valid for US states, and matches the selected state
        longest_prefix = 4  # Only return results for state name description (1XXX) (excl. city names)
        _state = _prefix_description_for_number(US_PHONE_GEODATA, longest_prefix, phone, 'en')
        try:
            assert _state
            lookup_state = states.lookup(_state)
            assert lookup_state
            state = State[lookup_state.abbr]  # Raise Key error if state abbreviation not in local states
            assert state == form_state  # Check that specified state same as parsed state
        except (AssertionError, KeyError):
            raise ValidationError('Invalid area code prefix')
