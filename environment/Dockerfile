# hash:sha256:30fced7308f59ca7d0f34a5727c20432402483318ff26c44a76a5f3a35757142
FROM registry.codeocean.com/codeocean/miniconda3:4.12.0-python3.9-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN conda install -y --channel=conda-forge \
        essential_generators==0.9.2 \
        numpy==1.24.3 \
        openpyxl==3.1.2 \
        pandas==2.0.1 \
        pathlib==1.0.1 \
        pdfminer==20191125 \
        pdfplumber==0.9.0 \
        regex==2023.5.5 \
        tectonic==0.13.0 \
        time==1.8 \
    && conda clean -ya
