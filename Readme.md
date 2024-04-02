# API Luke Books

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Full Stack Avançado**

## Objetivo

A missão primordial desta API é gerenciar os processos de login na plataforma Luke Books, fornecendo rotas dedicadas para registro de usuários, login e logout. Com uma abordagem estruturada e segura, esta API visa facilitar a gestão de usuários na plataforma, garantindo uma experiência fluida e segura.

- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/)
- [JWT](https://jwt.io/)
- [Flasgger](https://pypi.org/project/flasgger/)

---

### Instalação

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---

### Executando o servidor

Para executar a API basta executar:

```
(env)$ python app.py
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ python app.py --reload
```

---

### Acesso no browser

Abra o [http://localhost:6050/apidocs/](http://localhost:6050/apidocs/) no navegador para verificar o status da API em execução, e a sua documentação!

---

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t rest-api-login .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 6050:6050 rest-api-login
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:6050/apidocs/](http://localhost:6050/apidocs/) no navegador.

### Alguns comandos úteis do Docker

> **Para verificar se a imagem foi criada** você pode executar o seguinte comando:
>
> ```
> $ docker images
> ```
>
> Caso queira **remover uma imagem**, basta executar o comando:
>
> ```
> $ docker rmi <IMAGE ID>
> ```
>
> Subistituindo o `IMAGE ID` pelo código da imagem
>
> **Para verificar se o container está em exceução** você pode executar o seguinte comando:
>
> ```
> $ docker container ls --all
> ```
>
> Caso queira **parar um container**, basta executar o comando:
>
> ```
> $ docker stop <CONTAINER ID>
> ```
>
> Subistituindo o `CONTAINER ID` pelo ID do conatiner
>
> Caso queira **destruir um conatiner**, basta executar o comando:
>
> ```
> $ docker rm <CONTAINER ID>
> ```
>
> Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).
