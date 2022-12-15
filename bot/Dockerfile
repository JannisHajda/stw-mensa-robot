FROM python:3.7

RUN mkdir /app
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt requirements.txt

# Install the requirements
RUN pip3 install -r requirements.txt

# Copy src to the container
COPY . . 

# Run the app
ENTRYPOINT ["python3", "main.py"]