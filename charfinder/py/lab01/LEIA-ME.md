# LEIA-ME

Registro do ambiente utilizado nesta sessão.

## Ambiente

| Item | Valor |
| --- | --- |
| Versão do OpenCode | v2.2.5 |
| Provedor do modelo | opencode |
| Modelo selecionado | DeepSeek V4.1 Flash Free (`opencode/deepseek-v4.1-flash-free`) |

## Observações

- Versão obtida com `opencode --version`.
- Modelo identificado pelo provedor e ID ativos na sessão atual.
- Data do registro: 01/11/2026.


## Prompts

### #1

Escreva um arquivo LEIA-ME.md registrando a versao do OpenCode e do modelo selecionado neste momento.

### #2

Quero criar um utilitário de linha de comando que recebe uma ou mais palavras e exibe uma lista de caracteres Unicode que contém todas as palavras fornecidas em seus nomes. A lista deve conter 3 campos separados por tab: 1) código unicode no formato U+XXXX; 2) o caractere; 3) o nome do caractere.

### #3

Em vez de reclamar, ignore palavras vazias fornecidas pelo usuário.

### #4

Estou buscando "cat" e o resultado traz "indicator". Quero resultados somente quando coincidem palavras inteiras.

### #5

Ficou muito complicado. Nos nomes unicode, as palavras são separadas por espaços ou hífens. Use apenas split para separar o nome em palavras. Não use expressões regulares.

### #6

Em vez de tratar ValueError em unicodedata.name, existe uma solução mais eficiente?

