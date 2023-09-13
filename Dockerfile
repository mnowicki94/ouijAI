#ENV OPENAI_APIKEY=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
#NOT WORKING FOR SOME REASON


# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 8080/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY main.py .
COPY chatbot.py .
COPY features.py .
COPY ambient_c_motion.mp3 .


#COPY .env .
#COPY environment.yml .

#RUN pip install miniconda
#RUN pip conda env create -f environment.yml
#RUN conda activate ouijai-env

# Specify the command to run on container start
CMD [ "python", "./main.py" ]