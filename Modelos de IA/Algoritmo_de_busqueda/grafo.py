# Título: Grafo de Rutas en Sevilla
# Contiene el grafo de distancias (ruta_euclidea) y las coordenadas para visualización.

ruta_euclidea = {
        "IES Punta del Verde":{
            "Estadio Benito Villamarín": 685,
            "Pabellón de México": 1600
            },
        "Estadio Benito Villamarín": {
            "IES Punta del Verde": 685,
            "Hospital Virgen del Rocío": 546
            },
        "Pabellón de México": {
            "IES Punta del Verde": 1600,
            "Hospital Virgen del Rocío": 1110,
            "Plaza de España": 891,
            "Palacio de San Telmo": 1240
            },
        "Palacio de San Telmo": {
            "Pabellón de México": 1240,
            "Plaza de Cuba": 379,
            "Puente de Triana": 1000,
            "Plaza de España": 697
            },
        "Plaza de Cuba": {
            "Parque de los Príncipes": 732,
            "Palacio de San Telmo": 379
            },
        "Estadio La Cartuja": {
            "Torre Sevilla": 2940,
            "Puente de la Barqueta": 1540,
            "Glorieta Olímpica": 1460
            },
        "Puente de la Barqueta": {
            "Estadio La Cartuja": 1540,
            "Malandar": 699,
            "Parlamento de Andalucía": 790
            },
        "Puente de Triana":{
            "Palacio de San Telmo": 1000,
            "Plaza de Armas": 580,
            "Torre Sevilla": 890
            },
        "Parque de los Príncipes": {
            "Plaza de Cuba": 732,
            "Torre Sevilla": 1720
            },
        "Torre Sevilla": {
            "Parque de los Príncipes": 1720,
            "Puente de Triana": 890,
            "Estadio La Cartuja": 2940
            },
        "Plaza de Armas": {
            "Malandar": 799,
            "Puente de Triana": 580
            },
        "Hospital Virgen del Rocío": {
            "Avenida de la paz": 1290,
            "Pabellón de México": 1110,
            "Estadio Benito Villamarín": 546
            },
        "Plaza de España": {
            "Sta. Justa": 1930,
            "Pabellón de México": 891,
            "Palacio de San Telmo": 697
            },
        "Nervión Plaza": {
            "Sta. Justa": 871,
            "Avenida de la paz": 1660
            },
        "Sta. Justa": {
            "Nervión Plaza": 871,
            "Plaza de España": 1930,
            "Pandora": 1810,
            "Parlamento de Andalucía": 790
            },
        "Parlamento de Andalucía": {
            "Sta. Justa": 790,
            "Pandora": 2320,
            "Puente de la Barqueta": 790
            },
        "Glorieta Olímpica": {
            "Pandora": 2480,
            "Estadio La Cartuja": 1460
            },
        "Avenida de la paz": {
            "Hospital Virgen del Rocío": 1290,
            "Nervión Plaza": 1660
            },
        "Pandora": {
            "Sta. Justa": 1810,
            "Parlamento de Andalucía": 2320,
            "Glorieta Olímpica": 2480
            },
        "Malandar": {
            "Plaza de Armas": 799,
            "Puente de la Barqueta": 699
            }
        }

# Coordenadas X/Y para la visualización del grafo (ejemplo abstracto)
coordenadas = {
    "IES Punta del Verde": (3, 10),
    "Estadio Benito Villamarín": (3, 8),
    "Pabellón de México": (5, 9),
    "Hospital Virgen del Rocío": (3, 6),
    "Plaza de España": (7, 8),
    "Palacio de San Telmo": (7, 9),
    "Plaza de Cuba": (8, 7),
    "Estadio La Cartuja": (10, 1),
    "Puente de la Barqueta": (9, 3),
    "Puente de Triana": (9, 7),
    "Parque de los Príncipes": (8, 6),
    "Torre Sevilla": (10, 5),
    "Plaza de Armas": (9, 5),
    "Nervión Plaza": (5, 4),
    "Sta. Justa": (6, 5),
    "Parlamento de Andalucía": (7, 3),
    "Glorieta Olímpica": (4, 1),
    "Avenida de la paz": (4, 5),
    "Pandora": (5, 3),
    "Malandar": (8, 3)
}
