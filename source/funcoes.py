ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

frequencia_portugues = {
    "A": 0.1463,
    "B": 0.0104,
    "C": 0.0388,
    "D": 0.0499,
    "E": 0.1257,
    "F": 0.0102,
    "G": 0.0130,
    "H": 0.0078,
    "I": 0.0618,
    "J": 0.0040,
    "K": 0.0002,
    "L": 0.0278,
    "M": 0.0474,
    "N": 0.0505,
    "O": 0.1073,
    "P": 0.0252,
    "Q": 0.0120,
    "R": 0.0653,
    "S": 0.0680,
    "T": 0.0434,
    "U": 0.0368,
    "V": 0.0158,
    "W": 0.0004,
    "X": 0.0021,
    "Y": 0.0001,
    "Z": 0.0047,
}
# normaliza de acordo com alfabeto

def normalizar_txt(texto):
    txt_processado = ""
    for char in texto.upper():
        if char in ALFABETO:
            txt_processado += char
    return txt_processado


def extender_chave(chave, tamanho_texto): #extende e normaliza a chave
    chave_normalizada = ""
    for char in chave.upper():
        if char in ALFABETO:
            chave_normalizada += char
    if not chave_normalizada:
        return "Chave Inválida"    
    return (chave_normalizada * (tamanho_texto // len(chave_normalizada) + 1))[:tamanho_texto]
