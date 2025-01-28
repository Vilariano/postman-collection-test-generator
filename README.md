# Postman Collection Test Generator

Este projeto é um gerador automatizado de estrutura de testes que converte uma coleção do Postman em um framework de testes estruturado usando BDD (Behavior Driven Development).

## Estrutura Gerada

```
test/
├── features/
│   ├── specs/      # Arquivos Gherkin (.feature)
│   ├── steps/      # Definições dos steps do BDD
│   └── services/   # Classes de serviço para interação com API
```

## Pré-requisitos

- Python 3.7+
- Postman Collection (formato JSON)
- Bibliotecas Python:
  - requests
  - behave

## Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
```

2. Instale as dependências:
```bash
pip install requests behave
```

## Configuração

1. Coloque seu arquivo de coleção do Postman no diretório `collections/` com o nome `Swagger-Petstore.postman_collection.json`

2. Certifique-se que a estrutura do arquivo JSON da coleção está correta e contém:
   - Nome dos endpoints
   - Métodos HTTP
   - URLs
   - Parâmetros (se houver)

## Uso

Execute o script principal:

```bash
python postman_test_generator.py
```

O script irá:
1. Carregar a coleção do Postman
2. Criar a estrutura de diretórios necessária
3. Gerar arquivos Gherkin (.feature) para cada endpoint
4. Gerar arquivos de steps para cada cenário
5. Gerar classes de serviço para interação com a API

## Estrutura dos Arquivos Gerados

### Arquivos Gherkin (.feature)

```gherkin
#language:pt
Funcionalidade: [Nome do Endpoint]
    Como usuário com acesso ao Endpoint
    Quero interagir com o [Grupo]
    Para que eu possa [Ação] com sucesso

    @[Tag]
    Cenário: [Nome do Cenário]
        Dado que configurei a solicitação
        Quando envio uma solicitação [MÉTODO] para "[URL]"
        Então recebo uma resposta válida
```

### Arquivos de Steps

```python
from behave import given, when, then
from test.features.services.[service] import [Service]Class

@given('que configurei a solicitação')
def setup_request(context):
    context.payload = {}

@when('envio uma solicitação')
def send_request(context):
    context.response = service.method(context.payload)

@then('recebo uma resposta válida')
def validate_response(context):
    assert context.response.status_code == 200
```

### Classes de Serviço

```python
import requests
from support.logger import *
from support.ambientes import *
from support.loads import *

class ServiceClass:
    def method(self, payload=None):
        try:
            response = requests.method(f'{BASE_URL_QA}/2020', json=payload)
            return response
        except Exception as error:
            logging.error(error)
            raise
```

## Personalização

Para personalizar a geração dos testes, você pode modificar:

1. Templates dos arquivos gerados nas funções:
   - `generate_gherkin_files()`
   - `generate_step_files()`
   - `generate_service_classes()`

2. Constantes de diretório no início do arquivo:
   - `FEATURES_DIR`
   - `STEPS_DIR`
   - `SERVICES_DIR`

## Tratamento de Erros

O script inclui tratamento de erros para:
- Arquivo de coleção não encontrado
- JSON inválido
- Erros durante a geração dos arquivos
- Erros de execução das requisições

## Contribuição

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.