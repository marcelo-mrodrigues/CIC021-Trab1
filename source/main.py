from funcoes import *
import argparse


def criptografar( chave , texto ): #  chave e plaintext para o Vigenere

    chave_normalizada = extender_chave( chave , len(texto))
    plaintext_normalizado = normalizar_txt( texto )
    texto_cifrado = []

    for i in range(len(plaintext_normalizado)):
        
        itexto = plaintext_normalizado[i]
        ichave = chave_normalizada[i]

        valor_char_texto = ALFABETO.find(itexto)
        valor_char_chave = ALFABETO.find(ichave)

        valor_cifrado = (valor_char_texto + valor_char_chave) % 26
        texto_cifrado.append(ALFABETO[valor_cifrado])
    return ''.join(texto_cifrado)

def decifrar( chave , texto_cifrado ):
    texto_original = []
    chave_normalizada = extender_chave( chave , len(texto_cifrado))

    for i in range(len(texto_cifrado)):

        icifrado = texto_cifrado[i]
        ichave = chave_normalizada[i]

        valor_char_cifrado = ALFABETO.find(icifrado)
        valor_char_chave = ALFABETO.find(ichave)

        valor_char_original = (valor_char_cifrado - valor_char_chave + 26) % 26
        texto_original.append(ALFABETO[valor_char_original])
    return ''.join(texto_original)

print(criptografar("marcelo", "teste 1 do trabalho, simples para verificar o algoritmo"))
print(decifrar("marcelo" , criptografar("marcelo", "teste 1 do trabalho, simples para verificar o algoritmo") ))