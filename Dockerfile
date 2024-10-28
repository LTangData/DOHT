FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8501

COPY . .

CMD ["sh", "-c", "python src/server.py & streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0"]