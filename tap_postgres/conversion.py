from datetime import datetime
import pytz

# Function to convert custom format like YYYYMMDDTHHMMSSZ into standard strftime format
def convert_custom_format(custom_format):
    # Mapping custom tokens to Python strftime format tokens
    format_mapping = {
        'YYYY': '%Y',  # Year (4 digits)
        'YY': '%y',    # Year (2 digits)
        'MM': '%m',    # Month (2 digits)
        'DD': '%d',    # Day (2 digits)
        'HH': '%H',    # Hours (24-hour)
        'mm': '%M',    # Minutes
        'SS': '%S',    # Seconds
        'Z': 'Z',      # Literal 'Z'
        'T': 'T',      # Literal 'T'
        # We will handle 's', 'ss', 'sss' manually
    }

    # Replace custom format tokens with strftime tokens
    for token, strf_token in format_mapping.items():
        custom_format = custom_format.replace(token, strf_token)

    return custom_format

# Function to extract milliseconds in required format
def format_milliseconds(epoch_time_ms, precision):
    milliseconds = int(epoch_time_ms % 1000)  # Get the milliseconds part
    if precision == 1:  # 's'
        return f'{milliseconds // 100}'  # Get first digit of milliseconds
    elif precision == 2:  # 'ss'
        return f'{milliseconds // 10:02}'  # Get first two digits of milliseconds
    elif precision == 3:  # 'sss'
        return f'{milliseconds:03}'  # Full milliseconds (3 digits)
    return ''

# Function to convert epoch (in milliseconds) to desired format with timezone handling
def convert_epoch_to_format(epoch_time_ms, custom_format, time_zone):
    try:
        # Extract milliseconds from the epoch time
        epoch_time = epoch_time_ms / 1000.0  # Convert milliseconds to seconds
        
        # Convert custom format to strftime-compatible format
        desired_format = convert_custom_format(custom_format)

        # Convert epoch to datetime object in UTC
        dt_utc = datetime.utcfromtimestamp(epoch_time)

        # Set timezone to the desired one
        tz = pytz.timezone(time_zone)
        dt_localized = pytz.utc.localize(dt_utc).astimezone(tz)

        # Handle 's', 'ss', 'sss' manually since strftime doesn't support milliseconds
        if 'sss' in custom_format:
            formatted_time = dt_localized.strftime(desired_format)
            formatted_time = formatted_time.replace('sss', format_milliseconds(epoch_time_ms, 3))
        elif 'ss' in custom_format:
            formatted_time = dt_localized.strftime(desired_format)
            formatted_time = formatted_time.replace('ss', format_milliseconds(epoch_time_ms, 2))
        elif 's' in custom_format:
            formatted_time = dt_localized.strftime(desired_format)
            formatted_time = formatted_time.replace('s', format_milliseconds(epoch_time_ms, 1))
        else:
            # No milliseconds to handle, format normally
            formatted_time = dt_localized.strftime(desired_format)

        return formatted_time
    except Exception as e:
        return f"Error: {str(e)}"
