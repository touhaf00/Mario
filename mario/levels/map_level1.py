level_1 = {
    "player_start": (100, 500),
    "platforms": [
        # Sol continu prolongé avec plusieurs segments
        (0, 550, 600, 50),
        (700, 550, 400, 50),
        (1200, 550, 300, 50),
        (1600, 550, 300, 50),
        (2000, 550, 400, 50),
        (2500, 550, 300, 50),
        (2900, 550, 400, 50),
        # Plateformes en hauteur pour plus de challenge
        (800, 400, 150, 20),
        (1700, 400, 150, 20),
        (2600, 400, 200, 20),
        (3100, 400, 150, 20)
    ],
    "enemies": [
        {"pos": (800, 515), "range": 100},
        {"pos": (2000, 515), "range": 50},
        {"pos": (2700, 515), "range": 150},
        {"pos": (3100, 515), "range": 200}
    ],
    "blocks": [
        {"pos": (500, 500), "type": "mystery"},
        {"pos": (750, 500), "type": "normal"},
        {"pos": (850, 500), "type": "mystery"},
        {"pos": (1900, 500), "type": "mystery"},
        {"pos": (2600, 500), "type": "normal"},
        {"pos": (3050, 500), "type": "mystery"}
    ],
    "goal": (3500, 480)
}
