# Base Dockerfile for SLEAP benchmarking...

FROM ubuntu:18.04

LABEL maintainer="SLEAP Developers (Probably)"

# Create path for conda and add it to the container's path
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update
RUN apt-get install -y wget

# Install anaconda via wget
# Echo the conda shell script into bashrc so it starts when container is created
# Echo conda activate base into the bashrc so you're in base environment at start
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && /opt/conda/bin/conda clean -a -f -y \
    && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
    && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
    && echo "conda activate base" >> ~/.bashrc

RUN conda env update --quiet --name base --file environment.yml \
    && conda clean --all -f -y \
    && rm environment.yml