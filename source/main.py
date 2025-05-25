from funcoes import *
import argparse


def criptografar(chave, texto):  #  chave e plaintext para o Vigenere

    chave_normalizada = extender_chave(chave, len(texto))
    plaintext_normalizado = normalizar_txt(texto)
    texto_cifrado = []
    indice = 0

    for char_do_texto in plaintext_normalizado:
        if char_do_texto in ALFABETO:

            valor_char_texto = ALFABETO.find(char_do_texto)
            valor_char_chave = ALFABETO.find(chave_normalizada[indice])

            valor_char_cifra = (valor_char_texto + valor_char_chave) % 26
            texto_cifrado.append(ALFABETO[valor_char_cifra])
            indice += 1
        else:
            texto_cifrado.append(char_do_texto)
            
            
            
    return "".join(texto_cifrado)


def decifrar(chave, texto_cifrado):
    texto_original = []
    indice = 0
    
    chave_normalizada = extender_chave(chave, len(texto_cifrado))
    texto_cifrado = normalizar_txt(texto_cifrado)

    for char_da_cifra in texto_cifrado:
        if char_da_cifra in ALFABETO:
            valor_char_cifra = ALFABETO.find(char_da_cifra)
            valor_char_chave = ALFABETO.find(chave_normalizada[indice])

            valor_char_texto = (valor_char_cifra - valor_char_chave + 26) % 26
            texto_original.append(ALFABETO[valor_char_texto])
            indice += 1
        else:
            texto_original.append(char_da_cifra)
    return "".join(texto_original)
            
print(criptografar(input("  chave: "), input("  texto: ")))

print(decifrar(input("  chave: "), input("  texto: ")))

    
"""
print(
    criptografar("marcelo", "teste 1 do trabalho, simples para verificar o algoritmo")
)
print(
    decifrar(
        "marcelo",
        criptografar(
            "marcelo", "teste 1 do trabalho, simples para verificar o algoritmo"
        ),
    )
)
"""