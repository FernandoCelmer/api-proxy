# Execução do Projeto

Para execução e teste deste projeto foi configurado um ambiente pronto para utilização a partir de `containers`, onde são executados as duas aplicações, `API Proxy` e `Prometheus` com informações pré-carregadas.

## Dependências

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


| OS         | Package Manager  | Command                                |
|:---------- |:---------------- | :------------------------------------: | 
| linux      | Pacman           |  `pacman -S docker docker-compose git` |

## Etapas

### Download

Clonar o repositório [api-proxy](https://github.com/FernandoCelmer/api-proxy), disponível no Github.

```bash
git clone https://github.com/FernandoCelmer/api-proxy.git
```

### Construção

Comando para construir ou reconstruir serviços. Mais informações na documentação oficial -> [docker compose build](https://docs.docker.com/engine/reference/commandline/compose_build/)

```bash
docker-compose build
```

### Execução
Comando que constrói, (re)cria, inicia e anexa a contêineres para um serviço. Mais informações na documentação oficial -> [docker compose up](https://docs.docker.com/engine/reference/commandline/compose_up/)

```bash
docker-compose up
```
