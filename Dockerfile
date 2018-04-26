FROM weralwolf/de2-data:latest AS preprocessor

# Installing Basemap
ENV GEOS_DIR="/usr/local"
RUN pip install --upgrade pip && \
    pip install pyproj numpy && \
    mkdir build && \
    cd build/ && \
    wget https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz && \
    tar -xzvf v1.1.0.tar.gz && \
    cd basemap-1.1.0/geos-3.3.3/ && \
    ./configure --prefix=$GEOS_DIR && \
    make && \
    make install && \
    cd .. && \
    python setup.py install && \
    cd ../.. && \
    rm -rf build/

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
# ENTRYPOINT [""]
# CMD ["python", "./0000_analysis.py]
