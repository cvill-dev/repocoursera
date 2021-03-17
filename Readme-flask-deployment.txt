
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

PS C:\Users\CHARLESVILLEPREUX> python --version
Python 3.8.2
PS C:\Users\CHARLESVILLEPREUX> python -c "import os, sys; print(os.path.dirname(sys.executable))"
C:\my-install\install-folder\python382
PS C:\Users\CHARLESVILLEPREUX> cd C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution

PS C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution> pip install -U Flask
PS C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution> pip install -U joblib
PS C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution> pip install -U pandas
PS C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution> python app.py
PS C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution> pip install -U sklearn
C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>pip install -U IPython  
C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>pip install -U matplotlib
C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>pip freeze > requirements.txt

==== Dockerfile  ============

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

=================================

Also make sure you verify the app.py file:
if __name__ == '__main__':
    # host 127.0.0.1 if i run locally on windows without docker
    app.run(host='127.0.0.1', port=7000,debug=True)
    # host 0.0.0.0 if i run in a docker container
    #app.run(host='0.0.0.0', port=7000,debug=True)
	
to

if __name__ == '__main__':
    # host 127.0.0.1 if i run locally on windows without docker
    #app.run(host='127.0.0.1', port=7000,debug=True)
    # host 0.0.0.0 if i run in a docker container
    app.run(host='0.0.0.0', port=7000,debug=True)


C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>docker build -t myapp .

C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>docker run -p 7000:7000 myapp

C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>docker ps
CONTAINER ID   IMAGE     COMMAND           CREATED              STATUS              PORTS                    NAMES
e75a5b3b58a1   myapp     "python app.py"   About a minute ago   Up About a minute   0.0.0.0:7000->7000/tcp   busy_goldberg

localhost/7000 works
and I can get a prediction

C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>docker stop e75a5b3b58a1
e75a5b3b58a1

C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>docker rm e75a5b3b58a1
e75a5b3b58a1

C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>docker images
REPOSITORY                    TAG       IMAGE ID       CREATED              SIZE
myapp                         latest    c1d3c9fcda73   About a minute ago   1.72GB
gcr.io/k8s-minikube/kicbase   v0.0.13   90f1294ff9ac   5 months ago         800MB
hello-world                   latest    bf756fb1ae65   14 months ago        13.3kB

C:\Users\CHARLESVILLEPREUX\my-notebook\ai-ibm-course\ai-workflow-capstone\my-solution>docker rmi myapp
Untagged: myapp:latest
Deleted: sha256:c1d3c9fcda7367d6218db0306b72b388bd39940872a6eb914aa3a099d7baa7fb	
	