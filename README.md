<div align="center">
  <img alt="GROQ Logo" src="src/assets/GROQ Logo.png">
</div>

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](https://github.com/LTangData/GROQ/blob/main/LICENSE.md)
[![Python](https://img.shields.io/badge/python-3.11.9-blue?style=flat&logo=python&logoColor=%233776AB&logoSize=auto)](https://www.python.org/downloads/release/python-3119/)
[![MySQL](https://img.shields.io/badge/mysql-8.0.35-blue?style=flat&logo=mysql&logoColor=%234479A1&logoSize=auto)](https://www.mysql.com/)
[![LangChain](https://img.shields.io/badge/langchain-0.2.16-blue?style=flat&logo=langchain&logoColor=%231C3C3C&logoSize=auto)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-available-blue?style=flat&logo=docker&logoColor=%232496ED&logoSize=auto)](https://www.docker.com/)
[![Conda](https://img.shields.io/badge/conda-supported-blue?style=flat&logo=anaconda&logoColor=%2344A833&logoSize=auto)](https://anaconda.org/anaconda/conda)

## What is GROQ?

GROQ (Get Rid of Queries) is an intelligent RAG application designed to autonomously generate SQL queries from natural language questions, simplifying data retrieval by eliminating the need for technical query-writing skills and providing immediate, accurate access to database information.

## How does it work?

<img alt="GROQ architecture" src="src/assets/Architecture.png" style="">

<div align="right">
  <a href="https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/" style="text-align: right;">Source</a>
</div>

1. **Search for relevant information**: The app (or SQL Agent) searches for data related to the user's question.
2. **Generate SQL query**: AI model (like GPT) uses the data to generate a SQL query.
3. **Execute SQL query**: The app (or SQL Agent) executes the SQL query.
3. **Respond to user question**: AI model responds to user using result from the query.

## What real-world problems does it solve?

GROQ addresses the challenge of accessing and managing database information without technical expertise in SQL, enhancing productivity and reducing reliance on specialized personnel. 

This solution is crucial for businesses seeking to democratize data access and make informed decisions faster, streamlining operations and fostering a data-driven culture.

## Why would you bother?

GROQ might be beneficial for you, who need quick access to database information without the complexities of SQL, if you are a
- Business analyst
- Manager
- Non-technical staff
- Developer
- IT support specialist

Some of the typical use cases include
- Generating reports
- Analyzing inventory levels
- Monitoring sales data
- Enhancing customer service

It's ideal for any organization looking to empower their team members with direct, easy access to data insights, promoting efficiency and informed decision-making across various departments.

## Quickstart

### Reproduce the project

```
git clone https://github.com/HuyTang10/CPSC_2221_Group_Project.git
```

When you clone the GROQ project, you'll need to manually create a `.env` file in the root directory of the project. This file should contain the necessary environment variables for proper configuration. Use the following format for your `.env` file:

```
OPENAI_API_KEY="<Your_OpenAI_API_key>"
DB_USER="root" # Any user that you have locally (we take "root" for demonstration here)
DB_PASSWORD="root" # Password for the user you specified
DB_HOST="localhost" # Host that is allowed to connect to the database through your user. If you use Docker, either use your IPv4 address or a secure host since Docker does not allow connection made from "localhost"
DB_PORT="3306"
DB_NAME="groq_data"
```

Ensure to replace `<Your_OpenAI_API_key>` with your actual OpenAI API key to enable the application's full functionality. If you don't have one, you can obtain it from [OpenAI's API platform](https://platform.openai.com/api-keys).

**IMPORTANT**: Due to financial limitations, the GROQ project's database is managed locally rather than on a cloud platform. Therefore, you need to replicate my data into your MySQL Workbench in order to be able to access to the data through the application.

[GROQ_data.sql](https://www.dropbox.com/scl/fi/n8bdx1rg1oi95j37qw66q/GROQ_data.sql?rlkey=st4yab2fzwfxkakcldz4mjkwi&st=jvmpsz12&dl=0)

### Run with Docker (recommended)

You must have Docker installed on your machine. [Install Docker](https://docs.docker.com/get-docker/)

```
docker compose up
```

Navigate to [`localhost:5801`](http://localhost:8501/) to view the application.

### Run without Docker

#### Package installation

Using `pip`:

```
pip install -r requirements.txt
```

Using `conda`:

```
conda env create -f environment.yml
```

```
conda activate GROQ_ENV
```

#### Start the application

```
invoke app
```

Navigate to [`localhost:5801`](http://localhost:8501/) to view the application.

## Tech Stack

**Client:** Streamlit

**Server:** FastAPI

**Database:** MySQL, Chroma

**AI Solutions:** OpenAI API, LangChain

**DevOps:** Docker, Git

## Acknowledgements

 - [Cookiecutter Data Science template](https://cookiecutter-data-science.drivendata.org/)
 - [README editor](https://readme.so/)
 - [LangChain tutorial on Question/Answering system](https://python.langchain.com/docs/tutorials/sql_qa/)

