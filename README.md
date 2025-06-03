# Implementação da Cifra de Vigenère e Ataque por Análise de Frequência

Este projeto foi desenvolvido como parte da disciplina de Segurança Computacional (CIC0201) na Universidade de Brasília e consiste na implementação da Cifra de Vigenère, um método clássico de criptografia polialfabética, e um ataque por análise de frequência para tentar decifrar mensagens sem o conhecimento prévio da chave.

## Visão Geral do Projeto

O projeto está dividido em duas partes principais:

1.  **Cifrador/Decifrador Vigenère:**
    * Permite cifrar um texto plano utilizando uma chave fornecida.
    * Permite decifrar um texto cifrado utilizando a chave correta.
    * A implementação lida com a normalização de texto (remoção de acentos, conversão para maiúsculas) e preserva caracteres como espaços, pontos e vírgulas, cifrando apenas as letras do alfabeto.

2.  **Ataque por Análise de Frequência:**
    * Tenta determinar o comprimento da chave de um texto cifrado através do método do Índice de Coincidência (IC).
    * Após estimar o comprimento da chave, tenta determinar cada caractere da chave comparando as frequências de letras das colunas do texto cifrado com as frequências conhecidas dos idiomas português e inglês.
    * Por fim, tenta decifrar a mensagem original utilizando a chave recuperada.

## Estrutura de Arquivos do Projeto

CIC021-TRAB1/
|-- source/
|   |-- main.py             # Script principal, orquestra a cifragem, decifragem e o ataque
|   |-- funcoes.py          # Funções auxiliares: normalização de texto, extensão de chave,
|   |                       # constantes (alfabeto, frequências de letras, ICs esperados),
|   |                       # e funções de cálculo para análise de frequência.
|   |-- frequencia.py       # Lógica específica do ataque: encontrar tamanho da chave,
|   |                       # encontrar caracteres da chave, recuperar senha.
|-- textos/
|   |-- pt.txt              # Exemplo de texto em português para testes
|   |-- en.txt              # Exemplo de texto em inglês para testes
|-- README.md  

## Configuração e Requisitos

1.  **Python:** É necessário ter o Python 3.x instalado.

2.  **Dependência:** A única dependência externa é a biblioteca `unidecode`, utilizada para remover acentos de caracteres. Instale-a com:
    ```bash
    pip install unidecode
    ```

## Como Usar

O script principal é `source/main.py`. Conforme a última configuração, ele contém exemplos estáticos para demonstrar o ataque por análise de frequência.

**Execução dos Testes de Ataque Estáticos:**

Para executar os exemplos de ataque predefinidos nos arquivos `textos/pt.txt` e `textos/en.txt`:

1.  Navegue até a pasta raiz do projeto (`CIC021-TRAB1/`).
2.  Execute o comando:
    ```bash
    python source/main.py
    ```
    O script irá:
    * Permite a entrada de usuário para a chave selecionada e o texto a ser cifrado.
    * Permite decifrar utilizando uma chave e um texto cifrado.
    * Imprimir no console os resultados:
        * Texto cifrado.
        * Texto recuperado.
    * Ler os arquivos de texto originais (`pt.txt` e `en.txt`).
    * Cifrá-los com chaves de teste predefinidas no próprio `main.py`.
    * Aplicar o ataque de análise de frequência aos textos cifrados gerados.
    * Imprimir no console os resultados:
        * Estimativa do comprimento da chave.
        * A chave recuperada.
        * Um trecho do texto decifrado com a chave recuperada.
        * Uma comparação entre a chave original de teste e a chave recuperada.
