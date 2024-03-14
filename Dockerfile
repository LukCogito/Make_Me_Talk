FROM debian:latest

WORKDIR /app

# Install python3 and pip3
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Install required libraries
ARG INST_SCRIPT=libinstall.sh
COPY ./${INST_SCRIPT} /app/${INST_SCRIPT}
RUN chmod +x /app/${INST_SCRIPT}.sh && /app/${INST_SCRIPT}.sh

COPY . /app/