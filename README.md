
DOHT

[//]: # (Core dependencies)
[![Python](https://img.shields.io/badge/python-3.12.8-ffde57?style=flat&logo=python&logoColor=4584b6&logoSize=auto)](https://www.python.org/downloads/release/python-3128/)
[![LLM](https://img.shields.io/badge/LLM-GPT--4o-412991?style=flat)](https://platform.openai.com/docs/models)

[//]: # (DBMS available)
[![MySQL](https://img.shields.io/badge/MySQL-available-darkgreen?style=flat&logo=mysql&logoColor=F29111&logoSize=auto)](https://www.mysql.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-developing-blue?style=flat&logo=postgresql&logoColor=008bb9&logoSize=auto)](https://www.postgresql.org/)
[![Microsoft SQL Server](https://img.shields.io/badge/SQL%20Server-developing-blue?style=flat)](https://www.microsoft.com/en-ca/sql-server/sql-server-downloads)
[![SQLite](https://img.shields.io/badge/SQLite-developing-blue?style=flat&logo=sqlite&logoColor=5db1e4&logoSize=auto)](https://www.sqlite.org/)
[![Oracle Database](https://img.shields.io/badge/Oracle%20Database-unavailable-red?style=flat)]()
[![MongoDB](https://img.shields.io/badge/MongoDB-developing-blue?style=flat&logo=mongodb&logoColor=3FA037&logoSize=auto)](https://www.mongodb.com/)

[//]: # (Deployment)
[![Docker](https://img.shields.io/badge/Docker-deployed-darkgreen?style=flat&logo=docker&logoColor=0db7ed&logoSize=auto)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-deployed-darkgreen?style=flat&logo=render&logoColor=white&logoSize=auto)](https://render.com/)
[![Streamlit Community Cloud](https://img.shields.io/badge/Streamlit%20Community%20Cloud-deployed-darkgreen?style=flat&logo=streamlit&logoColor=FF4B4B&logoSize=auto)](https://streamlit.io/cloud)

[//]: # (Licenses)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](https://github.com/LTangData/GROQ/blob/main/LICENSE.md)

**dohT** is an advanced [Retrieval-Augmented Generation (RAG)](https://www.databricks.com/glossary/retrieval-augmented-generation-rag) application designed to simplify database interaction by eliminating the need for SQL queries. With dohT, users can retrieve precise and relevant information from databases simply by asking natural-language questions. The app leverages the power of [Large Language Model (LLM)](https://aws.amazon.com/what-is/large-language-model/) to interpret user questions, translate them into SQL queries, execute the queries, and return accurate, concise answers in a natural response.

Tailored specifically for business use, **dohT** is highly beneficial for non-technical users:

- **Ease of Use**: Eliminating the need to learn SQL, users can interact with database using everyday language.
- **Enhanced efficiency and Time saving**: Accurate information is provided promptly. More effective decision-making is facilitated while conserving technical resources.
- **Accurate and Contextualized results**: Integrated with powerful LLM, a RAG app delivers precise and context-aware responses. Actionable insights are extracted instead of raw or incomplete data.

# Quickstart

This application has been deployed for public access, allowing you to quickly test its functionality.

👉 [Try the Demo Here](https://ltang-doht.streamlit.app/)

⚠️ **HIGHLY IMPORTANT**

To ensure the application works seamlessly with your databases:

- Databases must be hosted on a cloud platform (e.g., AWS RDS, Google Cloud SQL, Azure SQL) or a dedicated server with a public IP address or domain name.
- Local databases (hosted on your personal machine) are not accessible by deployed services.

# Run Locally

With this approach, users will be able to establish connection to their local databases.

To run this project on your local machine, follow these steps:

1. **Clone the Repository**

    ```terminal
    git clone https://github.com/LTangData/dohT.git
    ```

2. **Set Up Environement Variables**

    When you clone the project, you'll need to manually create a `.env` file in the root directory of the project. As mentioned earlier, since this project utilizes GPT-4o model to perform core functionalities, you need to have your **OpenAI API key** available. Use the following format for your `.env` file:

    ```.env
    OPENAI_API_KEY="<Your_OpenAI_API_key>"
    ```

    Ensure to replace `<Your_OpenAI_API_key>` with your actual OpenAI API key to enable the application's full functionality. If you don't have one, you can obtain it from [OpenAI's API platform](https://platform.openai.com/api-keys).

## With Docker (recommended)

You must have Docker installed on your machine.

⬇️ [Install Docker Desktop](https://docs.docker.com/get-docker/)

After installation, in the root directory of the project, run the following command in your terminal:

```terminal
docker compose up
```

Navigate to [localhost:5801](http://localhost:8501/) to view the application.

## Without Docker

### Create a Virtual Environment (Optional)

It is recommended to use a virtual environment (`venv`) to isolate the project's dependencies and ensure compatibility across different environments.

1. **Initiliaze the virtual environment**

    ```terminal
    python -m venv venv
    ```

2. **Activate the virtual environment**

    On Windows:

    ```terminal
    venv\Scripts\activate
    ```

    On macOS/Linux:

    ```terminal
    source venv/bin/activate
    ```

### Package Installation

Using `pip`:

    ```terminal
    pip install -r requirements.txt
    ```

### Start the Application

To run the whole application:

    ```terminal
    start-app
    ```

To run backend and frontend separately:

- Backend:

    ```terminal
    start-server
    ```

- Frontend:

    ```terminal
    start-client
    ```

Navigate to [localhost:5801](http://localhost:8501/) to view the application.
# Tech Stack

**Client:** Streamlit

**Server:** FastAPI

**Database:** MySQL, Chroma

**AI Solutions:** OpenAI API, LangChain

**DevOps:** Docker, Git, Render, Streamlit Community Cloud

# Acknowledgements

 - [Cookiecutter Data Science template](https://cookiecutter-data-science.drivendata.org/)
 - [README editor](https://readme.so/)
 - [LangChain tutorial on Question/Answering system](https://python.langchain.com/docs/tutorials/sql_qa/)

