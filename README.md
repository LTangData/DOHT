
## GROQ

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/python-3.11.9-blue?style=flat&logo=python&logoColor=%233776AB&logoSize=auto&link=https%3A%2F%2Fwww.python.org%2Fdownloads%2Frelease%2Fpython-3119%2F)](https://www.python.org/downloads/release/python-3119/)
[![LangChain](https://img.shields.io/badge/langchain-0.2.16-blue?style=flat&logo=langchain&logoColor=%231C3C3C&logoSize=auto)](https://api.python.langchain.com/en/latest/langchain_api_reference.html)
[![Dev Containers](https://img.shields.io/badge/Dev_Containers-Open-blue?style=flat&logo=docker&logoColor=%232496ED&logoSize=auto)]()
[![Conda](https://img.shields.io/badge/conda-supported-blue?style=flat&logo=anaconda&logoColor=%2344A833&logoSize=auto)](https://anaconda.org/anaconda/conda)

## What is GROQ?

GROQ (Get Rid Of Queries) is an intelligent RAG application designed to autonomously generate SQL queries from natural language questions, simplifying data retrieval by eliminating the need for technical query-writing skills and providing immediate, accurate access to database information.

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

```
git clone https://github.com/HuyTang10/CPSC_2221_Group_Project.git
```

When you clone the GROQ project, you'll need to manually create a `.env` file in the root directory of the project. This file should contain the necessary environment variables for proper configuration. Use the following format for your `.env` file:

```
OPENAI_API_KEY=<Your_OpenAI_API_key>
DB_USER="groq"
DB_PASSWORD="groq2024"
DB_HOST="100.96.1.2"
DB_PORT="3306"
DB_NAME="groq_data"
```

Ensure to replace `<Your_OpenAI_API_key>` with your actual OpenAI API key to enable the application's full functionality. If you don't have one, you can obtain it from [OpenAI's API platform](https://platform.openai.com/api-keys).

### With Docker (recommended)

You must have Docker installed on your machine. [Install Docker](https://docs.docker.com/get-docker/)

```
docker compose up
```

Navigate to [`localhost:5801`](http://localhost:8501/) to view the application.

### Without Docker

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

#### Starting the application

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

