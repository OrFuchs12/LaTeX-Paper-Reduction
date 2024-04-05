# hash:sha256:99c2ef05a0632fc2ff73aadba020dcbe3e7307818ab72289d1c47d5682c60464
FROM registry.codeocean.com/codeocean/miniconda3:4.12.0-python3.9-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN conda install -y --channel=conda-forge \
        catboost==1.1.1 \
        essential_generators==0.9.2 \
        networkx==3.1 \
        numpy==1.24.3 \
        openpyxl==3.1.2 \
        pandas==2.0.1 \
        pathlib==1.0.1 \
        pdfminer==20191125 \
        pdfplumber==0.9.0 \
        pypdf2==2.11.1 \
        regex==2023.5.5 \
        tectonic==0.13.1 \
        time==1.8 \
        xgboost==1.7.4 \
    && conda clean -ya
