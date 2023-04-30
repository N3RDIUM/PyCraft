def position_to_string(position):
    return str(position[0]) + ',' + str(position[1]) + ',' + str(position[2])
def string_to_position(string):
    return tuple([float(i) for i in string.split(',')])