def encode_position(position):
    ret = ""
    for i in range(0, len(position)):
        ret += str(position[i]) + "x"
    return ret[:-1]

def decode_position(position):
    position = position.split("x")
    for i in range(0, len(position)):
        position[i] = int(position[i])
    return position

def jsonify_vbo_data(vertices, texCoords):
    json = "{\"vertices\":["
    for i in range(0, len(vertices)):
        json += f"{i}"
        if i != len(vertices) - 1:
            json += ","
    json += "], \"texCoords\":["
    for i in range(0, len(texCoords)):
        json += f"{i}"
        if i != len(texCoords) - 1:
            json += ","
    json += "]}"
    return json
