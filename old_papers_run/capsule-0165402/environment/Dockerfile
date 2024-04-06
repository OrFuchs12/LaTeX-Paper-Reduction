# hash:sha256:fa5626a47c3a76273f8d69a83725bc247e59fda812e9d9a716b1f35679d05fe3
FROM registry.codeocean.com/codeocean/miniconda3:4.12.0-python3.9-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN conda install -y --channel=conda-forge \
        numpy==1.24.3 \
        openpyxl==3.1.2 \
        pandas==2.0.2 \
        pdfplumber==0.9.0 \
        pypdf2==2.11.1 \
        regex==2023.6.3 \
        scipy==1.10.1 \
        tectonic==0.12.0 \
        xgboost==1.7.4 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    pdfminer-six \
    sklearn==0.0.post5
