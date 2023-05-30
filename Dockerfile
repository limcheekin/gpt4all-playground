FROM python:3.10-slim

# MODEL_NAME is blank even it's value is passed with env()
RUN echo "model name: $MODEL_NAME" 

#RUN cat token.txt