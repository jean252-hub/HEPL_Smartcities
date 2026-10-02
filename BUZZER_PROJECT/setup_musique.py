
notes = {
    'DO': 262,
    'DO#': 277,
    'RE': 294,
    'RE#': 311,
    'MI': 330,
    'FA': 349,      
    'FA#': 370,
    'SOL': 392,
    'SOl#': 415,
    'LA': 440,
    'LA#': 466,
    'SI': 494,
    'DO_AIGU': 523, 
    'DO#_AIGU': 554,
    'RE_AIGU': 587,
    'MI_AIGU': 659,
    'FA_AIGU': 698,
    'PAUSE': 0
}

BPM = 130
NOIRE = 60 / BPM
BLANCHE = NOIRE * 2
RONDE = NOIRE * 4
CROCHE = NOIRE / 2
DOUBLE_CROCHE = NOIRE / 4


partitions = {
    "star_wars_dark": [
        ("LA", NOIRE), ("LA", NOIRE), ("LA", NOIRE), ("FA", CROCHE * 1.5), ("DO_AIGU", DOUBLE_CROCHE),
        ("LA", NOIRE), ("FA", CROCHE * 1.5), ("DO_AIGU", DOUBLE_CROCHE), ("LA", BLANCHE),
        ("MI_AIGU", NOIRE), ("MI_AIGU", NOIRE), ("MI_AIGU", NOIRE), ("FA_AIGU", CROCHE * 1.5), ("DO_AIGU", DOUBLE_CROCHE),
        ("SOl#", NOIRE), ("FA", CROCHE * 1.5), ("DO_AIGU", DOUBLE_CROCHE), ("LA", BLANCHE)
    ],
    "get_lucky": [
        ("SI", CROCHE), ("DO#_AIGU", CROCHE), ("RE_AIGU", CROCHE), ("MI_AIGU", NOIRE),
        ("PAUSE", CROCHE), ("RE_AIGU", CROCHE), ("DO#_AIGU", CROCHE),
        ("LA", CROCHE), ("SI", CROCHE), ("DO#_AIGU", CROCHE), ("RE_AIGU", NOIRE),
        ("PAUSE", CROCHE), ("DO#_AIGU", CROCHE), ("SI", CROCHE),
        ("FA#", NOIRE), ("LA", NOIRE), ("SI", BLANCHE)
    ],
    "blinding_lights": [
        ("FA", CROCHE), ("FA", CROCHE), ("SOL", CROCHE), ("LA", CROCHE), 
        ("DO_AIGU", NOIRE), ("LA", CROCHE), ("SOL", NOIRE),
        ("FA", CROCHE), ("RE", BLANCHE), ("PAUSE", CROCHE),
        ("FA", CROCHE), ("FA", CROCHE), ("SOL", CROCHE), ("LA", CROCHE),
        ("DO_AIGU", NOIRE), ("LA", CROCHE), ("SOL", NOIRE),
        ("DO_AIGU", CROCHE), ("RE_AIGU", BLANCHE)
    ],
    "bad_guy": [
        ("SOL", CROCHE), ("SOL", CROCHE), ("PAUSE", CROCHE), ("SOL", CROCHE),
        ("SOL", CROCHE), ("SI", CROCHE), ("LA", CROCHE), ("SOL", CROCHE),
        ("FA#", CROCHE), ("FA#", CROCHE), ("PAUSE", CROCHE), ("FA#", CROCHE),
        ("FA#", CROCHE), ("LA", CROCHE), ("SOL", CROCHE), ("FA#", CROCHE)
    ]
}
