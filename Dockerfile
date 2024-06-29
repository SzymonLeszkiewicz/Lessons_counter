# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 8501

EXPOSE 8502

# Set the browser
ENV BROWSER="/usr/bin/google-chrome"

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["streamlit", "run", "Lessons_Counter.py"]
