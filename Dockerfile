FROM python:3.8-alpine

#Adds packages necessary for the application
RUN apk update && apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev

ARG PROJECT_NAME=broker-api

RUN mkdir /$PROJECT_NAME
WORKDIR /$PROJECT_NAME

# Install Requirements
ADD requirements.txt /$PROJECT_NAME
RUN pip3 install -r /$PROJECT_NAME/requirements.txt

#Exposes port 3000
EXPOSE 3000

#Setting COMMIT variable
ARG COMMIT
ENV COMMIT=$COMMIT

#Deploy of code
ADD . /$PROJECT_NAME

CMD ./bin/app.sh
