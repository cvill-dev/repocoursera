
# Use an official Python runtime as a parent image
FROM python:3.8.2

RUN apt-get update && apt-get install -y \
python3-dev \
build-essential    
  
# Set the working directory to /app-docker
WORKDIR /app-docker
  
# Copy the current directory contents into the container at /app-docker
COPY . /app-docker

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000

# Run app.py when the container launches
CMD ["python", "app.py"]
