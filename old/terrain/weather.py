from noise import snoise3

def get_weather_at(position, SEED):
    x, z = position

    temperature = snoise3(x / 1600, z / 1600, SEED) * 10
    humidity    = snoise3(x / 1600, z / 1600, SEED + 1) * 10
    wind        = snoise3(x / 1600, z / 1600, SEED + 2) * 10

    return {
        "temperature": temperature,
        "humidity"   : humidity,
        "wind"       : wind
    }

def compute_biome(weather, biomes):
    temperature = weather["temperature"]
    humidity    = weather["humidity"]
    wind        = weather["wind"]
    weather_desc = []

    if temperature > 0.5:
        weather_desc.append("hot")
    elif temperature < -0.5:
        weather_desc.append("cold")
    else:
        weather_desc.append("temperate")

    if humidity > 0.5:
        weather_desc.append("wet")
    elif humidity < -0.5:
        weather_desc.append("dry")
    else:
        weather_desc.append("normal")

    if wind > 0.5:
        weather_desc.append("windy")
    else:
        weather_desc.append("calm")

    for biome in biomes.values():
        for value in weather_desc:
            if value not in biome.weather_desc:
                break
        else:
            return biome
    # fallback to default biome
    return biomes["grasslands"]
