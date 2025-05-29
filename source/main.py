from funcoes import *
import frequencia
import os


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


print(criptografar(input("  chave: "), input("  texto: ")))  # cifra
print(decifrar(input("  chave: "), input("  texto: ")))  # decifra

input('Continuar para a parte II?')

def atacar_arquivo(
    caminho_arquivo_cifrado: str,
    idioma_alvo: str,
    chave_original_para_teste: str = None,
):

    print(
        f"\n--- ATACANDO ARQUIVO: {caminho_arquivo_cifrado} (Idioma Alvo: {idioma_alvo.upper()}) ---"
    )

    texto_para_atacar = ""
    texto_original_conhecido_normalizado = ""

    if chave_original_para_teste:
        print(
            f"Usando chave original para teste: '{chave_original_para_teste}' para gerar texto cifrado."
        )
        try:
            with open(
                caminho_arquivo_cifrado.replace("_cifrado", ""), "r", encoding="utf-8"
            ) as f_orig:
                texto_original_bruto = f_orig.read()
            print(
                f"Texto original lido (início): '{texto_original_bruto[:100].replace(os.linesep, ' ')}...'"
            )
            texto_original_conhecido_normalizado = normalizar_txt(texto_original_bruto)
            texto_para_atacar = criptografar(
                chave_original_para_teste, texto_original_bruto
            )
            print(
                f"Texto gerado para ataque (cifrado, início): '{texto_para_atacar[:100].replace(os.linesep, ' ')}...'"
            )
        except FileNotFoundError:
            print(
                f"ERRO: Arquivo original para gerar cifrado não encontrado: {caminho_arquivo_cifrado.replace('_cifrado', '')}"
            )
            return
        except Exception as e:
            print(f"ERRO ao ler ou cifrar arquivo original: {e}")
            return
    else:
        try:
            with open(caminho_arquivo_cifrado, "r", encoding="utf-8") as f_cif:
                texto_para_atacar = f_cif.read()
            print(
                f"Texto cifrado lido do arquivo (início): '{texto_para_atacar[:100].replace(os.linesep, ' ')}...'"
            )
        except FileNotFoundError:
            print(f"ERRO: Arquivo cifrado '{caminho_arquivo_cifrado}' não encontrado.")
            return
        except Exception as e:
            print(f"ERRO ao ler arquivo cifrado: {e}")
            return

    if not texto_para_atacar:
        print("Texto para atacar está vazio.")
        return
    texto_cifrado_para_analise = normalizar_texto_para_analise_frequencia(
        texto_para_atacar
    )

    if not texto_cifrado_para_analise:
        print("Erro: Após normalização para análise, o texto cifrado ficou vazio.")
        return

    print(
        f"Texto cifrado normalizado para análise (total de {len(texto_cifrado_para_analise)} letras): {texto_cifrado_para_analise[:80]}..."
    )

    tamanho_chave_estimado = frequencia.encontrar_tamanho_chave(
        texto_cifrado_para_analise,
        tamanho_min_chave = 1,
        tamanho_max_chave = 50,  # mudar com a suspeita da chave
        idioma_alvo=idioma_alvo,
    )

    if tamanho_chave_estimado == 0:
        print("Não foi possível estimar um tamanho de chave provável.")
        return

    chave_recuperada = frequencia.recuperar_senha(
        texto_cifrado_para_analise, tamanho_chave_estimado, idioma_alvo=idioma_alvo
    )
    print(f"CHAVE RECUPERADA (estimada): '{chave_recuperada}'")

    if chave_original_para_teste:
        if chave_recuperada.upper() == chave_original_para_teste.upper():
            print(
                f"SUCESSO NA CHAVE! Chave recuperada corresponde à chave original de teste ('{chave_original_para_teste}')."
            )
        else:
            print(
                f"FALHA NA CHAVE. Chave recuperada '{chave_recuperada}' != Chave original de teste '{chave_original_para_teste}'."
            )

    if "?" in chave_recuperada or not chave_recuperada:
        print(
            "Aviso: A chave pode não ter sido completamente recuperada ou é inválida. Tentando decifrar mesmo assim..."
        )

    if chave_recuperada:
        print("Tentando decifrar o texto com a chave recuperada...")
        texto_decifrado_final = decifrar(chave_recuperada, texto_para_atacar)

        print(f"\nTEXTO DECIFRADO COM A CHAVE RECUPERADA (início):")
        resultado_preview = texto_decifrado_final[:300].replace(os.linesep, " ")
        print(resultado_preview + ("..." if len(texto_decifrado_final) > 300 else ""))

        if (
            texto_original_conhecido_normalizado
            and texto_original_conhecido_normalizado
            == normalizar_txt(texto_decifrado_final)
        ):
            print(
                "VERIFICAÇÃO DE TEXTO: SUCESSO! Texto decifrado corresponde ao original normalizado."
            )
        elif texto_original_conhecido_normalizado:
            print(
                "VERIFICAÇÃO DE TEXTO: FALHA! Texto decifrado NÃO corresponde ao original normalizado."
            )

    else:
        print("Não foi possível decifrar o texto")
    print("--- fim ---")


# testes, mexer aqui

PASTA_BASE_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_TEXTOS = os.path.join(PASTA_BASE_PROJETO, "textos")


CHAVE_PT_TESTE = "segredo"  # Escolha uma chave
ARQUIVO_PT_ORIGINAL = os.path.join(PASTA_TEXTOS, "pt.txt")

atacar_arquivo(
    ARQUIVO_PT_ORIGINAL, idioma_alvo="pt", chave_original_para_teste=CHAVE_PT_TESTE
)


#  en.txt
CHAVE_EN_TESTE = "HGFBSMNBKDJVBSJKDHFSDJDA"  # Escolha uma chave
ARQUIVO_EN_ORIGINAL = os.path.join(PASTA_TEXTOS, "en.txt")


atacar_arquivo(
    ARQUIVO_EN_ORIGINAL, idioma_alvo="en", chave_original_para_teste=CHAVE_EN_TESTE
)


print("\n--- ataque fim ---")


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
