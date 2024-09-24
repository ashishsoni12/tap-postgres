from datetime import datetime

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

# Function to convert epoch to desired format
def convert_epoch_to_format(epoch_time, custom_format):
    try:
        # Convert custom format to strftime-compatible format
        desired_format = convert_custom_format(custom_format)
        
        # Convert epoch to formatted time
        formatted_time = datetime.utcfromtimestamp(int(epoch_time)).strftime(desired_format)
        return f"Formatted Time: {formatted_time}"
    except Exception as e:
        return f"Error: {str(e)}"

# Get user input for epoch time and custom format
epoch_time = input("Enter epoch time: ")
custom_format = input("Enter custom date format (e.g., HHmmSS, YYYYMMDD): ")

# Convert and display the result
result = convert_epoch_to_format(epoch_time, custom_format)
print(result)

