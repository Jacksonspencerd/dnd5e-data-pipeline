# python image
FROM python:3.11-slim

# set environment variables
WORKDIR /app

#copy project files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the application
CMD ["python", "-m", "etl.pipeline", "--db", "spells.db", "--sleep", "0.1"]

