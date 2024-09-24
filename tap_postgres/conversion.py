from datetime import datetime
import pytz

# Function to convert custom format like HHmmSS into standard strftime format
def convert_custom_format(custom_format):
    # Mapping custom tokens to Python strftime format tokens
    format_mapping = {
        'YYYY': '%Y',  # Year (4 digits)
        'YY': '%y',    # Year (2 digits)
        'MM': '%m',    # Month (2 digits)
        'DD': '%d',    # Day (2 digits)
        'HH': '%H',    # Hours (24-hour)
        'hh': '%I',    # Hours (12-hour)
        'mm': '%M',    # Minutes
        'SS': '%S',    # Seconds
        'AMPM': '%p',  # AM/PM
    }

    # Replace custom format tokens with strftime tokens
    for token, strf_token in format_mapping.items():
        custom_format = custom_format.replace(token, strf_token)

    return custom_format

# Function to convert epoch to desired format with timezone handling
def convert_epoch_to_format(epoch_time, custom_format, time_zone):
    try:
        # Convert custom format to strftime-compatible format
        desired_format = convert_custom_format(custom_format)

        # Convert epoch to datetime object in UTC
        dt_utc = datetime.utcfromtimestamp(int(epoch_time))

        # Set timezone to the desired one
        tz = pytz.timezone(time_zone)
        dt_localized = pytz.utc.localize(dt_utc).astimezone(tz)

        # Convert datetime object to the formatted string in the given timezone
        formatted_time = dt_localized.strftime(desired_format)
        return formatted_time
    except Exception as e:
        return f"Error: {str(e)}"
