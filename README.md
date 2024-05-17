# Gerenciamento de Vendedores e Comissão de Vendas

Este projeto é uma API para gerenciar vendedores. Ele permite criar, atualizar, deletar e consultar vendedores, bem como calcular comissões e volumes de vendas a partir de uma planilha Excel.

### Requisitos

- Python 3.8
- virtualenv 

### Passos para Configuração

1. **Clone o repositório:**

```bash
   git clone https://github.com/JosePBNeto/Desafio-Tecnico-Gerenciador-Vendedores.git
```
2. **Crie um ambiente virtual:**
  ```bash
python -m venv .venv
```
3. **Ativa o ambiente virtual:**
```bash
.venv\Scripts\activate
```
3. **Instale as dependencias:**
```bash
pip install flask pandas openpyxl 
```
### API Gerenciar vendedores endpoints
Collection do Postman na pasta resources com payloads e endpoints para facilitar

Criar vendedor: <br />
`POST` http://localhost:5000/vendedores

Exemplo do payload:
```JSON
  {
    "nome": "Jose Patricio",
    "cpf": "391.321.321-11",
    "data_nascimento": "1980-02-07",
    "email": "joosee@gmail.com",
    "estado": "SC"
  }
```
Retorna a lista de todos os vendedores: <br />
`GET` http://localhost:5000/vendedores

Retorna vendedor pelo cpf: <br />
`GET` http://localhost:5000/vendedores/{cpf}

Alltera dados do vendedore pelo cpf: <br />
`PUT` http://localhost:5000/vendedores/{cpf}

Deleta dados do vendedore pelo cpf: <br />
`DELETE` http://localhost:5000/vendedores/{cpf}


### Endpoints para atualizar ou adicionar vendedores a partir de planilha Excel:

`POST` Atualiza ou adiciona vendedores na base de dados com base em uma planilha excel: <br />
http://localhost:5000/vendedores/planilha

`POST` Calcula comissões dos vendedores e cria uma nova sheet no arquivo Excel com o resultado <br />
http://localhost:5000/vendedores/calcularComissao

`POST` Apresenta o volume de vendas e média por profissional por canal e cria uma nova sheet no arquivo Excek com o resultado<br />
http://localhost:5000/vendedores/calcularComissao

### Observações:
Certifique-se de que os arquivos Vendas.xlsx e Vendedores.xlsx estejam presentes na pasta resources para que as operações de leitura e escrita funcionem corretamente.

### Execução do projeto:
Para iniciar a aplicação, execute o arquivo run.py:

```bash
python run.py
```
















