FROM python:3.6.5 AS preprocessor

# Download datafiles
ENV FTP_NASA_SERVER="spdf.gsfc.nasa.gov" \
    PATH_NACS="/pub/data/de/de2/neutral_gas_nacs/n_T_1s_ascii/data" \
    PATH_WATS="/pub/data/de/de2/neutral_gas_wats/n_T_v_2s_ascii"

RUN mkdir /data && \
    cd /data && \
    wget -c -nv -m ftp://${FTP_NASA_SERVER}${PATH_NACS}/*.ASC && \
    mv ${FTP_NASA_SERVER}${PATH_NACS} nacs/ && \
    wget -nv -m ftp://${FTP_NASA_SERVER}${PATH_WATS}/*.asc && \
    mv ${FTP_NASA_SERVER}${PATH_WATS} wats && \
    rm -rf ${FTP_NASA_SERVER}

ENV DE2SOURCE_NACS_DIR="/data/nacs" \
    DE2SOURCE_WATS_DIR="/data/wats"

# Installing Basemap
ENV GEOS_DIR="/usr/local"
RUN pip install pyproj numpy && \
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

RUN pip install pipenv && \
    pipenv install --system --dev && \
    pipenv install --system

COPY . /usr/app
# ENTRYPOINT [""]
CMD ["python", "./0000_analysis.py]
