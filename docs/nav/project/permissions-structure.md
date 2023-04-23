# Estrutura de Permissões

Inicialmente para este projeto foi pensado em não usar um banco de dados relacional como `MySQL`, já pensando nos problemas comuns que no futuro pederiam acontecer como a questão do `Deadlock` (Deadlock é o termo utilizado para designar um erro que acontece quando duas sessões entram numa situação de conflito, cada qual aguardando pela liberação de bloqueios que a outra sessão mantém) com as possíveis milhares de solicitações a API por segundo.

Uma das alternativas pensadas ao banco de dados `MySQL` foi o `MongoDB` que é um banco de dados não relacional, para suprir a demanda de armazenamento de informações de `Proxys`, `Clientes` e `Permissões`.

Mas para não deixar muito complexo a parte inicial do projeto foi definido dentro do projeto dois arquivos de configuração, um para os `Proxys` e o outro para o `Cliente`, esse foi um modo de pelo menos padronizar uma estrura de permissões que podem no futuro ser reutilizadas ou integradas com outros tipos de base de dados.

## Configuração: Proxy

**Path**: `api-proxy/proxy/data/proxy.json`

```json
{
    "gorest.co.in": {
        "scheme": "https",
        "host": "gorest.co.in",
        "paths": [
            {
                "path": "/public/v2/users",
                "max_request": 10,
                "time_stamp": 60
            },
            {
                "path": "/public/v2/users/{ID}",
                "max_request": 10,
                "time_stamp": 60
            },
            {
                "path": "/public/v2/posts",
                "max_request": 5,
                "time_stamp": 60
            },
            {
                "path": "/public/v2/comments",
                "max_request": 25,
                "time_stamp": 60
            },
            {
                "path": "/public/v2/todos",
                "max_request": 50,
                "time_stamp": 60
            }
        ]
    }
}
```

Este arquivo de configuração tem como principal função armazenar informações de `APIs` que o `Proxy` irá prover suporte a redirecionamento. É uma estrutura com informações básicas realizar as devidas operações.


## Configuração: Client

**Path**: `api-proxy/proxy/data/users.json`

```json
{
    "172.16.238.1": [
        {
            "host": "gorest.co.in",
            "paths": [
                {
                    "path": "/public/v2/users",
                    "max_request": 10,
                    "time_stamp": 1
                },
                {
                    "path": "/public/v2/users/{ID}",
                    "max_request": 10,
                    "time_stamp": 60
                },
                {
                    "path": "/public/v2/comments",
                    "max_request": 15,
                    "time_stamp": 5
                }    
            ]
        }
    ],
    "127.0.0.1": [
        {
            "host": "gorest.co.in",
            "paths": [
                {
                    "path": "/public/v2/users",
                    "max_request": 5,
                    "time_stamp": 10
                },
                {
                    "path": "/public/v2/users/{ID}",
                    "max_request": 10,
                    "time_stamp": 60
                },
                {
                    "path": "/public/v2/comments",
                    "max_request": 25,
                    "time_stamp": 5
                }    
            ]
        }
    ]
}
```

Este arquivo contém informações relacionadas ao `Cliente`, `Path` e quantidade máxima permitida.