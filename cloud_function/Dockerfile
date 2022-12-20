# Define function directory
ARG FUNCTION_DIR="/function"

ARG BASE_IMAGE="python:3.10-slim"
FROM ${BASE_IMAGE}  as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Install dependencies for aws runtime API
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY lambda.py interfaces.py model.pkl ${FUNCTION_DIR}/

# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY requirements.txt  .
RUN  pip install \
     -r requirements.txt \
     --target ${FUNCTION_DIR} \
        awslambdaric


# Multi-stage build: grab a fresh copy of the base image
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Install runtime system dependencies
#RUN apt-get update && apt-get install -y \
#    libgomp1

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ENV FUNCTION_DIR=${FUNCTION_DIR}

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

CMD [ "lambda.lambda_handler" ]