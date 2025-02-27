# Geração de Testes Automáticos a partir de Coleções Postman

Este script em Python automatiza a geração de testes a partir de coleções Postman. O objetivo é criar arquivos de teste estruturados em formato Gherkin `.feature`, arquivos de steps `_steps.py` e classes de serviço `_service.py`. Ele também trata duplicações e gera arquivos de utilitários para centralizar o código repetido.

## Funcionalidades

### 1. **Solicitação de Caminhos**
   O script solicita ao usuário os caminhos dos arquivos necessários:
   - Caminho da coleção Postman.
   - Caminho do projeto onde os testes serão gerados.

### 2. **Diretórios de Destino**
   - **FEATURES_DIR**: Diretório onde os arquivos `.feature` serão gerados.
   - **STEPS_DIR**: Diretório onde os arquivos `_steps.py` serão gerados.
   - **SERVICES_DIR**: Diretório onde os arquivos de serviço (`_service.py`) serão gerados.
   - **UTILS_FEATURE**: Arquivo centralizado para features duplicadas.
   - **UTILS_STEPS**: Arquivo centralizado para steps duplicados.
   - **UTILS_SERVICE**: Arquivo centralizado para serviços duplicados.

### 3. **Funções principais**

#### `detect_duplicates(directory: str, utils_file: str, check_imports: bool = False) -> None`
   Detecta duplicações nos arquivos de um diretório e as move para um arquivo de utilitários, evitando que múltiplos arquivos com o mesmo conteúdo sejam gerados.

   - **directory**: Diretório onde os arquivos serão verificados.
   - **utils_file**: Arquivo onde os conteúdos duplicados serão centralizados.
   - **check_imports**: Verifica se há imports duplicados, caso o valor seja `True`.

#### `ensure_directories() -> None`
   Cria os diretórios necessários para armazenar os arquivos gerados.

#### `generate_gherkin_files(collection: Dict) -> None`
   Gera arquivos `.feature` para os endpoints presentes na coleção Postman. Cada endpoint gera um arquivo de funcionalidade em Gherkin.

#### `generate_step_files(collection: Dict) -> None`
   Gera arquivos de steps (`_steps.py`) com as definições de cenários e ações a serem realizadas durante os testes. Cada arquivo de step importa a classe de serviço específica para o endpoint.

#### `generate_service_classes(collection: Dict) -> None`
   Gera arquivos de classe de serviço (`_service.py`), que contêm a lógica para fazer as requisições para os endpoints definidos na coleção Postman.

#### `process_items(items: List[Dict], callback: Callable[[Dict], None]) -> None`
   Processa cada item da coleção Postman, chamando a função `callback` para gerar os arquivos correspondentes (Gherkin, steps e serviço) para cada endpoint.

### 4. **Fluxo do Script**
   O script segue a seguinte sequência de passos:
   1. **Criação de Diretórios**: Verifica e cria os diretórios necessários para armazenar os arquivos gerados.
   2. **Leitura da Coleção**: Lê o arquivo JSON da coleção Postman fornecido pelo usuário.
   3. **Geração dos Arquivos de Teste**:
      - **Arquivos `.feature`**: Gerados a partir dos endpoints.
      - **Arquivos `_steps.py`**: Gerados com as ações e validações para cada endpoint.
      - **Arquivos `_service.py`**: Gerados com a lógica para as requisições HTTP.
   4. **Verificação de Duplicações**: Arquivos duplicados são movidos para os arquivos de utilitários correspondentes (`utils_feature.feature`, `utils_steps.py` e `utils_service.py`).

### 5. **Exemplo de Uso**
- Instale o pacote:
   ```python
   pip install postman-collection-test-generator
   ```
- A estrutura esperada para seu projeto de ser:
   ```python
   test/
   ├── features/
   │   ├── specs/ # Arquivos de recursos Gherkin
   │   ├── steps/ # Definições de etapas
   │   └── services/ # Classes de serviço
   ```
- Execute o comando:
   ```python
   bdd-generator
   ```
- Ao executar o comando, será solicitado que forneça o caminho da coleção Postman e o caminho do projeto:
    - Digite o caminho da collection Postman:
        ```bash
        /caminho/para/collection.json
        ```
    - Digite o caminho do projeto onde os testes serão gerados:
        ```bash
        /caminho/do/projeto
        ```

## Conclusão
 - A ideia deste script e facilitar a geração automatizada de testes a partir de coleções Postman, criando arquivos bem estruturados para facilitar a automação de testes de APIs.
 - Ele também evita duplicação de código, centralizando trechos reutilizáveis em arquivos de utilitários.