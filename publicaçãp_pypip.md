## Publicação no PyPI

Para publicar o projeto no PyPI, siga os passos abaixo:

1. **Configurar o `setup.py`**:
   Certifique-se de que o arquivo `setup.py` está configurado corretamente com as informações do pacote.

2. **Gerar a distribuição**:
   ```bash
   python setup.py sdist bdist_wheel
   ```
   Isso irá criar os arquivos de distribuição na pasta `dist/`.

3. **Configurar a autenticação no PyPI**:
   Crie ou edite o arquivo `~/.pypirc` com as credenciais:

   ```ini
   [distutils]
   index-servers =
       pypi

   [pypi]
   username = __token__
   password = <seu-token-aqui>
   ```

4. **Fazer o upload para o PyPI**:
   ```bash
   twine upload dist/*
   ```

5. **Verificar o pacote**:
   Acesse [PyPI](https://pypi.org/) e verifique se o pacote foi publicado com sucesso.

## Exemplo de Uso

1. Execute o programa:
   ```bash
   python -m gerenciador_projetos
   ```

2. Escolha o tipo de projeto e a linguagem na interface.

3. Especifique o diretório de destino para extração.

4. O gerenciador irá copiar, extrair e limpar os arquivos automaticamente.

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção de bug:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m "Adiciona minha nova feature"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

