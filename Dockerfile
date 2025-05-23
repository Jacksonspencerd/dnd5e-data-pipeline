# python image
FROM python:3.11-slim-bullseye

# set environment variables
WORKDIR /app

#copy project files
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501"]

