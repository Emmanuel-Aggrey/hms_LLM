# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Install PostgreSQL client, nano, and vim
RUN apt-get update && apt-get install -y postgresql-client nano vim


# create root directory for our project in the container
RUN mkdir /backend

# Set the working directory to /backend
WORKDIR /backend

# Install any needed packages specified in requirements.txt
ADD ./requirements.txt /backend/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /backend
ADD . /backend/


EXPOSE 7000
