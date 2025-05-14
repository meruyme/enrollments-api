# Enrollments API

## Descrição

A API tem por objetivo realizar o gerenciamento de inscrições. Além disso, também possui um script autônomo para a aprovação ou rejeição de inscrições.

## Configuração do projeto

### Tecnologias

A API foi desenvolvida usando Python 3.9.6, com o framework FastAPI. O banco de dados escolhido foi o MongoDB. Para o gerenciamento das dependências do projeto, foi escolhido o [pip-tools](https://pypi.org/project/pip-tools/). Para o envio de mensagens, foi utilizado o RabbitMQ.

### Dependências
Esse projeto é dependente da [Age Group API](https://github.com/meruyme/age-group-api). Para o funcionamento correto, clone o repositório e crie um arquivo .env na raiz do projeto para armazenar as variáveis de ambiente necessárias. 

Não é necessária a criação dos containers utilizando o docker-compose.yml do projeto Age group.

### Instruções de execução

Crie, na raiz do projeto, um arquivo .env para armazenar suas variáveis de ambiente. Um arquivo de exemplo pode ser encontrado [aqui](.env_example).

Para a criação dos containers no Docker e execução do sistema, execute:
> make local-up

Após iniciar o projeto, é possível encontrar uma documentação detalhada de todas as rotas da API na seguinte URL:
> http://localhost:8000/api/docs

### Script de atualizacão de status

Para a atualização do status das inscrições criadas, execute:

> make status-processor

O script irá receber as mensagens enviadas após criação das inscrições e atualizar o seu status de acordo.

### Testes

Para a criação dos testes, foi utilizada a biblioteca Pytest. 

Para executá-los, utilize o seguinte comando:
> make local-test
