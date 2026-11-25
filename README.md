# Sistema de Controle de Devoluções por Marketplace

**Projeto Integrador — UNISA | Análise e Desenvolvimento de Sistemas**

## Sobre o projeto

Sistema desenvolvido em Python para facilitar o controle e a análise de produtos devolvidos por diferentes marketplaces.

A aplicação utiliza arquivos CSV como fonte de dados e apresenta as informações em um dashboard interativo, permitindo acompanhar devoluções, identificar defeitos e consultar o status dos produtos.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly

## Como funciona o programa

O sistema realiza a leitura dos arquivos CSV e organiza os dados para apresentação em um dashboard.

O usuário pode selecionar o marketplace e aplicar filtros por mês, defeito, status e situação.

O painel apresenta indicadores, gráficos e uma tabela com os produtos devolvidos. Também permite baixar os registros filtrados em formato CSV.

## Como instalar e executar

### 1. Instalar o Python

Caso ainda não tenha Python instalado, acesse:

https://www.python.org/downloads/

Baixe e instale a versão recomendada. No Windows, marque a opção **Add Python to PATH** durante a instalação.

Para verificar se foi instalado corretamente, abra o CMD e execute:

```bash
python --version
```

### 2. Baixar o projeto

- Acesse este repositório no GitHub.
- Clique em **Code**.
- Selecione **Download ZIP**.
- Extraia os arquivos para uma pasta do computador.

### 3. Instalar as bibliotecas

Abra o terminal dentro da pasta do projeto e execute:

```bash
python -m pip install pandas streamlit plotly
```

Aguarde a instalação terminar.

### 4. Executar o programa

No mesmo terminal, execute:

```bash
python -m streamlit run Dashboard_Devolucoes.py
```

### 5. Acessar o dashboard

Após iniciar o programa, abra o navegador e acesse:

http://localhost:8501

Para encerrar o programa, volte ao terminal e pressione `Ctrl + C`.

## Requisitos e observações

- É necessário ter Python instalado.
- A instalação das bibliotecas exige conexão com a internet.
- Os arquivos CSV devem estar disponíveis nos caminhos esperados pelo código.
- Os nomes dos arquivos e das colunas devem corresponder aos esperados pelo programa.
- O dashboard é executado localmente no computador.

## Autor

Mauricio Laurentino Oliveira

Curso: Análise e Desenvolvimento de Sistemas

Universidade Santo Amaro — UNISA | 2026
