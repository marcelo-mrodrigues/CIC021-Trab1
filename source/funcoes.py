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
        if char in ALFABETO:
            apenas_letras += char
    return apenas_letras