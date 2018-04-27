FROM weralwolf/de2-data:latest AS preprocessor

# Installing Basemap
RUN pip install --upgrade pip && \
    pip install pyproj numpy && \
    apt-get update && \
    apt-get install -y libgeos-dev && \
    apt-get autoclean && \
    wget https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz && \
    tar -xzvf v1.1.0.tar.gz && \
    cd basemap-1.1.0/ && \
    python setup.py install && \
    cd ../ && \
    rm -rf basemap-1.1.0/

# Installing project dependencies
RUN mkdir -p /processing/cache && \
    mkdir -p /processing/artifacts && \
    mkdir -p /processing/nacs && \
    mkdir -p /processing/wats

ENV CACHE_DIR="/processing/cache" \
    ARTIFACTS_DIR="/processing/artifacts" \
    NACS_DIR="/processing/nacs" \
    WATS_DIR="/processing/wats"

WORKDIR /usr/app
ADD Pipfile* ./

RUN export PATH=/usr/local/bin:$PATH && \
    ln -s /usr/local/bin/python /bin/python && \
    pip install pipenv && \
    pipenv install --system --dev && \
    pipenv install --system

COPY . /usr/app

CMD ["python", "./manage.py", "exec", "all"]
