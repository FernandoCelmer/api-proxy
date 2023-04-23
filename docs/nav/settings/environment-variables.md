# Variaveis de Ambiente

## Resumo

Como o próprio nome já diz uma variável de ambiente é uma variável que existe no contexto do seu projeto,
ou seja, se eu criar uma variável de ambiente no meu computador ele não vai aparecer no seu computador.

OBS: E principalmente não pode enviado para o repositório do projeto, deve ser adicionado no projeto
o mesmo ser executado em desenvolvimento, homologação ou produção.

### Criação Variável

Para criar as variáveis de ambiente em seu projeto basta seguir o modelo de arquivo,
disponibilizado na raiz do projeto chamado `.env-exemple`.

Instruções:

- Copie o arquivo `.env-exemple`
- Renomeia a cópia de `.env-exemple-copy` para `.env`
- Edite o arquivo `.env` com as informações necessárias

## Variáveis -> proxy

### Lista de Variáveis

| NOME                      | Tipo    | Valor Exemplo                                         |
| ------------------------  | ------- | ------------------------------------------------------|
| DEBUG                     | Integer | 0 - 1                                                 |
| ENVIRONMENT               | String  | development - sandbox - production                    |
| PROXY                     | String  | ./proxy/data/proxy.json                               |
| USERS                     | String  | ./proxy/data/users.json                               |
| URL_PROYX                 | String  | http://127.0.0.1:8000                             |
| URL_PROMETHEUS            | String  | http://127.0.0.1:9090                             |

## Variáveis -> prometheus

### Lista de Variáveis

| NOME                      | Tipo    | Valor Exemplo                                         |
| ------------------------  | ------- | ------------------------------------------------------|