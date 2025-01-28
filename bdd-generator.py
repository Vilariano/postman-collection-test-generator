"""
Gerador de teste de coleção Postman

Este script converte uma coleção Postman em uma estrutura de teste estruturada com:
- Arquivos de recursos Gherkin (cenários BDD)
- Definições de etapas para os cenários BDD
- Classes de serviço para interações de API

A estrutura gerada segue:
test/
├── features/
│ ├── specs/ # Arquivos de recursos Gherkin
│ ├── steps/ # Definições de etapas
│ └── services/ # Classes de serviço
"""

import json
import os
from typing import Dict, List, Callable, Any

# Configuration constants
FEATURES_DIR = "test/features/specs"
STEPS_DIR = "test/features/steps"
SERVICES_DIR = "test/features/services"

def load_postman_collection(file_path: str) -> Dict:
    """
    Load and parse a Postman collection JSON file.
    
    Args:
        file_path: Path to the Postman collection JSON file
        
    Returns:
        Dict containing the parsed collection data
        
    Raises:
        FileNotFoundError: If collection file doesn't exist
        json.JSONDecodeError: If collection file is invalid JSON
        IsADirectoryError: If path points to a directory instead of a file
    """
    if os.path.isdir(file_path):
        raise IsADirectoryError(f"O caminho fornecido é um diretório: {file_path}\nPor favor, forneça o caminho completo para o arquivo .json da collection.")
    
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Collection file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in collection file: {file_path}")

def ensure_directories() -> None:
    """Create the required directory structure if it doesn't exist."""
    for directory in [FEATURES_DIR, STEPS_DIR, SERVICES_DIR]:
        os.makedirs(directory, exist_ok=True)

def process_items(items: List[Dict], callback: Callable[[Dict], None]) -> None:
    """
    Recursively process items in the Postman collection.
    
    Args:
        items: List of collection items to process
        callback: Function to call for each endpoint found
    """
    for item in items:
        if 'request' in item and 'method' in item['request']:
            callback(item)
        elif 'item' in item:
            process_items(item['item'], callback)

def generate_gherkin_files(collection: Dict) -> None:
    """
    Generate Gherkin feature files for each endpoint.
    
    Args:
        collection: Parsed Postman collection data
    """
    def create_gherkin_file(endpoint: Dict) -> None:
        group_name = endpoint.get('name', 'unknown_group')
        feature_name = f"{endpoint['name'].replace(' ', '_').lower()}.feature"
        feature_path = os.path.join(FEATURES_DIR, feature_name)

        method = endpoint['request']['method']
        url = endpoint['request'].get('url', {}).get('raw', 'URL não especificada')

        gherkin_content = f"""#language:pt
Funcionalidade: {endpoint['name']}
    Como usuário com acesso ao Endpoint: {endpoint['name']}
    Quero interagir com o {group_name}
    Para que eu possa {endpoint['name'].lower()} com sucesso

    @{endpoint['name']}
    Cenário: {endpoint['name']}
        Dado que configurei a solicitação
        Quando envio uma solicitação {method} para "{url}"
        Então recebo uma resposta válida
"""
        with open(feature_path, "w", encoding='utf-8') as f:
            f.write(gherkin_content)

    process_items(collection['item'], create_gherkin_file)

def generate_step_files(collection: Dict) -> None:
    """
    Generate step definition files for each endpoint.
    
    Args:
        collection: Parsed Postman collection data
    """
    def create_step_file(endpoint: Dict) -> None:
        step_name = f"{endpoint['name'].replace(' ', '_').lower()}_steps.py"
        step_path = os.path.join(STEPS_DIR, step_name)

        group_name = endpoint.get('name', 'unknown_group').replace(" ", "_").lower()
        method = endpoint['request']['method']
        url = endpoint['request'].get('url', {}).get('raw', 'URL não especificada')

        step_content = f"""
from behave import *
from services.{group_name}_service import {group_name.capitalize()}Service

service = {group_name.capitalize()}Service()

@given('que configurei a solicitação')
def setup_request(context):
    context.payload = {{}}

@when('envio uma solicitação {method} para "{url}"')
def send_request(context):
    context.response = service.{endpoint['name'].replace(' ', '_').lower()}(context.payload)

@then('recebo uma resposta válida')
def validate_response(context):
    assert context.response.status_code == 200
"""
        with open(step_path, "w", encoding='utf-8') as f:
            f.write(step_content)

    process_items(collection['item'], create_step_file)

def generate_service_classes(collection: Dict) -> None:
    """
    Generate service classes for each endpoint group.
    
    Args:
        collection: Parsed Postman collection data
    """
    def create_service_class(endpoint: Dict) -> None:
        group_name = endpoint.get('name', 'unknown_group').replace(" ", "_").lower()
        service_file = f"{group_name}_service.py"
        service_path = os.path.join(SERVICES_DIR, service_file)

        method = endpoint['request']['method'].lower()
        endpoint_name = endpoint['name'].replace(' ', '_').lower()

        service_content = f"""import requests
from typing import Dict, Any
from support.logger import *
from support.ambientes import *
from support.loads import *

class {group_name.capitalize()}Service:
    def {endpoint_name}(self, payload: Dict[str, Any] = None) -> requests.Response:
        '''
        Executa requisição {method.upper()} para o endpoint {endpoint_name}
        
        Args:
            payload: Dados da requisição (opcional)
            
        Returns:
            Response object from the API call
            
        Raises:
            Exception: Se houver erro na requisição
        '''
        try:
            response = requests.{method}(f'{{BASE_URL_QA}}/2020', json=payload)
            print(response.text)
            return response
        except Exception as error:
            logging.error(error)
            raise
"""
        # Append to file to allow multiple endpoints in same service
        with open(service_path, "a", encoding='utf-8') as f:
            f.write(service_content)

    process_items(collection['item'], create_service_class)

def get_collection_path() -> str:
    """
    Get the Postman collection path from user input.
    
    Returns:
        str: Path to the Postman collection file
        
    Raises:
        FileNotFoundError: If the provided file path doesn't exist
    """
    while True:
        file_path = input("\nInsira o caminho completo para sua collection do Postman (incluindo o nome do arquivo .json)\n" +
                         "Ou pressione Enter para usar o padrão 'collections/Swagger-Petstore.postman_collection.json': ").strip()
        
        if not file_path:
            file_path = "collections/Swagger-Petstore.postman_collection.json"
        
        if not file_path.endswith('.json'):
            print("\nErro: O arquivo deve ter extensão .json")
            print("Por favor, forneça o caminho completo para o arquivo .json da collection.")
            continue
            
        if os.path.isdir(file_path):
            print(f"\nErro: O caminho fornecido é um diretório: {file_path}")
            print("Por favor, forneça o caminho completo para o arquivo .json da collection.")
            continue
            
        if os.path.exists(file_path):
            return file_path
            
        print(f"\nErro: Arquivo não encontrado: {file_path}")
        print("Por favor, verifique o caminho e tente novamente.")

def main() -> None:
    """Main execution function that orchestrates the test generation process."""
    try:
        print("\n=== Postman Collection Test Generator ===")
        collection_path = get_collection_path()
        print(f"\nCarregando collection de: {collection_path}")
        
        collection = load_postman_collection(collection_path)
        print("Collection carregada com sucesso")

        ensure_directories()
        print("Estrutura de diretórios criada")

        generate_gherkin_files(collection)
        print("Arquivos Gherkin (.feature) gerados")

        generate_step_files(collection)
        print("Arquivos de steps gerados")

        generate_service_classes(collection)
        print("Classes de serviço geradas")

        print("\nGeração de testes concluída com sucesso!")

    except Exception as e:
        print(f"\nErro durante a geração dos testes: {str(e)}")
        raise

if __name__ == "__main__":
    main()