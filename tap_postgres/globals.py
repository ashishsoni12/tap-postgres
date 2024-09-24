def get_x():
    try:
        with open("Pos_value.txt", "r") as file:
            x = int(file.read())
    except FileNotFoundError:
        # If the file doesn't exist, start with 0
        x = 0
    return x

def set_x(x):
    with open("Pos_value.txt", "w") as file:
        file.write(str(x))

def addition(timestamp):
    x = get_x()
    x = x + 86400000
    timestamp = x + timestamp
    set_x(x)
    return timestamp

