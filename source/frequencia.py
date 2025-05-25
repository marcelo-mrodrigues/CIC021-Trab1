import math
import funcoes


def obter_subtexto_coluna(
    texto_apenas_letras: str, tamanho_chave: int, indice_coluna: int
):
    """Extrai o subtexto (coluna) de um texto que contém apenas letras."""
    subtexto = ""
    for i in range(indice_coluna, len(texto_apenas_letras), tamanho_chave):
        subtexto += texto_apenas_letras[i]
    return subtexto


def calcular_ic_texto(texto_apenas_letras: str) -> float:

    if not texto_apenas_letras:
        return 0.0

    contagens, comprimento_texto = funcoes.calcular_contagens_letras(
        texto_apenas_letras
    )

    if comprimento_texto < 2:
        return 0.0

    soma_numerador_ic = 0.0
    for letra_idx in funcoes.ALFABETO:
        ni = contagens.get(letra_idx, 0)
        soma_numerador_ic += ni * (ni - 1)

    denominador_ic = comprimento_texto * (comprimento_texto - 1)
    if denominador_ic == 0:
        return 0.0

    ic = soma_numerador_ic / denominador_ic
    return ic


def encontrar_tamanho_chave(
    texto_cifrado_apenas_letras: str,
    tamanho_min_chave: int = 1,
    tamanho_max_chave: int = 20,
    idioma_alvo: str = "pt",
) -> int:

    ic_alvo_lingua = funcoes.IC_ESPERADO_PORTUGUES
    nome_idioma_print = "Português"

    if idioma_alvo.lower() == "en":
        if hasattr(funcoes, "IC_ESPERADO_INGLES"):
            ic_alvo_lingua = funcoes.IC_ESPERADO_INGLES
            nome_idioma_print = "Inglês"
        else:
            print(
                f"Aviso: Constante IC_ESPERADO_INGLES não encontrada em funcoes.py. Usando Português como fallback para IC."
            )
    elif idioma_alvo.lower() != "pt":
        print(
            f"Aviso: Idioma alvo '{idioma_alvo}' não reconhecido para IC. Usando Português como fallback para IC."
        )

    melhor_tamanho_chave = 0
    menor_diferenca_abs_ic = float("inf")

    print(
        f"\nProcurando tamanho da chave (IC alvo para {nome_idioma_print}: {ic_alvo_lingua:.4f}):"
    )

    for tamanho_candidato in range(tamanho_min_chave, tamanho_max_chave + 1):
        if tamanho_candidato <= 0:
            continue

        ics_das_colunas = []
        for i in range(tamanho_candidato):
            coluna_texto = obter_subtexto_coluna(
                texto_cifrado_apenas_letras, tamanho_candidato, i
            )
            if coluna_texto:
                ics_das_colunas.append(calcular_ic_texto(coluna_texto))

        if not ics_das_colunas:
            ic_medio_colunas = 0.0
        else:
            ic_medio_colunas = sum(ics_das_colunas) / len(ics_das_colunas)

        diferenca_atual = abs(ic_medio_colunas - ic_alvo_lingua)

        print(
            f"  Tamanho candidato {tamanho_candidato:2d}: IC Médio das Colunas = {ic_medio_colunas:.4f}, (Diferença para IC alvo: {diferenca_atual:.4f})"
        )

        if diferenca_atual < menor_diferenca_abs_ic:
            menor_diferenca_abs_ic = diferenca_atual
            melhor_tamanho_chave = tamanho_candidato

    if melhor_tamanho_chave == 0 and tamanho_min_chave > 0:
        print(
            f"Aviso: Não foi possível determinar um tamanho de chave ótimo. Usando tamanho mínimo: {tamanho_min_chave}"
        )
        melhor_tamanho_chave = tamanho_min_chave

    print(f"Melhor estimativa para tamanho da chave: {melhor_tamanho_chave}")
    return melhor_tamanho_chave


def encontrar_char_chave_para_coluna(
    coluna_apenas_letras: str, idioma_alvo: str = "pt"
) -> str:
    """Encontra o caractere da chave para uma coluna, usando as frequências do idioma_alvo."""
    if not coluna_apenas_letras:
        return "?"

    frequencias_lingua_alvo = funcoes.frequencia_portugues

    if idioma_alvo.lower() == "en":
        if hasattr(funcoes, "frequencia_ingles"):
            frequencias_lingua_alvo = funcoes.frequencia_ingles
        else:
            print(
                f"Aviso: frequencia_ingles não encontrada em funcoes.py. Usando Português para encontrar char da chave."
            )
    elif idioma_alvo.lower() != "pt":
        print(
            f"Aviso: Idioma '{idioma_alvo}' não reconhecido para frequências. Usando Português para encontrar char da chave."
        )

    frequencias_esperadas_vetor = [
        frequencias_lingua_alvo.get(char, 0.0) for char in funcoes.ALFABETO
    ]
    melhor_char_chave = "A"
    maior_correlacao = -1.0

    for i_chave_candidata in range(len(funcoes.ALFABETO)):
        char_chave_candidato = funcoes.ALFABETO[i_chave_candidata]
        coluna_decifrada_tentativa_lista = []

        for char_cifrado_coluna in coluna_apenas_letras:
            valor_char_cifrado = funcoes.ALFABETO.find(char_cifrado_coluna)
            valor_char_chave_cand = i_chave_candidata

            valor_char_decifrado = (
                valor_char_cifrado - valor_char_chave_cand + len(funcoes.ALFABETO)
            ) % len(funcoes.ALFABETO)
            coluna_decifrada_tentativa_lista.append(
                funcoes.ALFABETO[valor_char_decifrado]
            )

        coluna_decifrada_str = "".join(coluna_decifrada_tentativa_lista)
        frequencias_observadas_tentativa = funcoes.calcular_frequencias_observadas(
            coluna_decifrada_str
        )
        frequencias_observadas_vetor = [
            frequencias_observadas_tentativa.get(char, 0.0) for char in funcoes.ALFABETO
        ]

        correlacao_atual = sum(
            p_esp * q_obs
            for p_esp, q_obs in zip(
                frequencias_esperadas_vetor, frequencias_observadas_vetor
            )
        )

        if correlacao_atual > maior_correlacao:
            maior_correlacao = correlacao_atual
            melhor_char_chave = char_chave_candidato

    return melhor_char_chave


def recuperar_senha(
    texto_cifrado_apenas_letras: str, tamanho_chave: int, idioma_alvo: str = "pt"
) -> str:
    """Recupera a senha completa, usando as estatísticas do idioma_alvo."""
    if tamanho_chave <= 0 or not texto_cifrado_apenas_letras:
        return ""

    senha_recuperada_lista = []
    print(
        f"\nRecuperando caracteres da chave (tamanho {tamanho_chave}, idioma {idioma_alvo.upper()}):"
    )

    for i in range(tamanho_chave):
        coluna_atual = obter_subtexto_coluna(
            texto_cifrado_apenas_letras, tamanho_chave, i
        )
        if not coluna_atual:
            print(f"  Coluna {i+1} está vazia. Adicionando '?' à chave.")
            senha_recuperada_lista.append("?")
            continue

        char_chave_encontrado = encontrar_char_chave_para_coluna(
            coluna_atual, idioma_alvo
        )
        senha_recuperada_lista.append(char_chave_encontrado)
        print(f"  Coluna {i+1}: Caractere da chave = {char_chave_encontrado}")

    return "".join(senha_recuperada_lista)
