# Automatizando Testes com Python, Selenium e Behave

## Software e Configuração:
```sh
Python 3.9 e pip ou superior
Pip
```
## INSTALAÇÃO E EXECUÇÃO

Instalação de dependências:
```sh
python3 -m venv .env
source .env/bin/activate
pip install -r requirements/requirements.txt
```
### Criação de variáveis de ambiente

## Comandos para execução dos testes:
# Options
#### Executar com tag especifica:
```sh
behave -t@GetRequest -f html -o=reports/results.html -f json -o=reports/results.json -k
```
#### Executar feature especifica:
```sh
behave features/spec/my_store.feature
```
### Utilizando Debug ipdb 
```sh
pip install ipdb
- ipdb é o debugguer do python pois o Behave breescreve ele
- import ipdb; ipdb.sset_trace() - este comando da starta o debug
```