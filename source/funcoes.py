from unidecode import unidecode

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CARACTERES_PERMITIDOS = " .,"


def normalizar_txt(texto):
    texto = unidecode(texto)
    txt_processado = ""
    for char in texto.upper():
        if char in ALFABETO:
            txt_processado += char
        if char in CARACTERES_PERMITIDOS:
            txt_processado += char

    return txt_processado


def extender_chave(chave, tamanho_texto):  # extende e normaliza a chave
    chave_normalizada = ""
    for char in chave.upper():
        if char in ALFABETO:
            chave_normalizada += char
    if not chave_normalizada:
        return "Chave Inválida"
    return (chave_normalizada * (tamanho_texto // len(chave_normalizada) + 1))[
        :tamanho_texto
    ]


def obter_apenas_letras(texto):
    apenas_letras = ""
    for char in texto:
        if char.upper() in ALFABETO:
            apenas_letras += char.upper()
    return apenas_letras


############################## Parte 2 ######################################
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

frequencia_ingles = {
    "A": 0.08167,
    "B": 0.01492,
    "C": 0.02782,
    "D": 0.04253,
    "E": 0.12702,
    "F": 0.02228,
    "G": 0.02015,
    "H": 0.06094,
    "I": 0.06966,
    "J": 0.00153,
    "K": 0.00772,
    "L": 0.04025,
    "M": 0.02406,
    "N": 0.06749,
    "O": 0.07507,
    "P": 0.01929,
    "Q": 0.00095,
    "R": 0.05987,
    "S": 0.06327,
    "T": 0.09056,
    "U": 0.02758,
    "V": 0.00978,
    "W": 0.02360,
    "X": 0.00150,
    "Y": 0.01974,
    "Z": 0.00074,
}


def normalizar_texto_para_analise_frequencia(texto):
    texto_processado_passo1 = unidecode(texto)
    return obter_apenas_letras(texto_processado_passo1)


def calcular_contagens_letras(texto_apenas_letras):
    contagens = {char: 0 for char in ALFABETO}
    comprimento_texto = 0
    for char in texto_apenas_letras:
        if char in contagens:
            contagens[char] += 1
            comprimento_texto += 1
    return contagens, comprimento_texto


def calcular_frequencias_observadas(texto_apenas_letras):
    contagens, comprimento_texto = calcular_contagens_letras(texto_apenas_letras)
    if comprimento_texto == 0:
        return {char: 0.0 for char in ALFABETO}

    frequencias_obs = {char: contagens[char] / comprimento_texto for char in ALFABETO}
    return frequencias_obs


IC_ESPERADO_PORTUGUES = sum(p**2 for p in frequencia_portugues.values())
IC_ALEATORIO = 1 / 26
IC_ESPERADO_INGLES = sum(p**2 for p in frequencia_ingles.values())
