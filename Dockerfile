FROM weralwolf/de2-data:latest AS datalayer
FROM python:3.6 AS mainland

ENV PYTHONUNBUFFERED=1

# Install tini for process PID 1
# Reasoning: https://engineeringblog.yelp.com/2016/01/dumb-init-an-init-for-docker.html
ARG TINI_VERSION='0.18.0'

ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENTRYPOINT ["/tini", "--"]

# Install datalayer
COPY --from=datalayer /data /data

ENV DE2SOURCE_NACS_DIR="/data/nacs" \
    DE2SOURCE_WATS_DIR="/data/wats"

# Installing Basemap
ARG BASEMAP_VERSION='1.1.0'
COPY ./patches /patches

RUN pip install --upgrade pip && \
    pip install pyproj numpy && \
    apt-get update && \
    apt-get install -y libgeos-dev && \
    apt-get autoclean && \
    mkdir build && \
    cd build/ && \
    wget -nv https://github.com/matplotlib/basemap/archive/v$BASEMAP_VERSION.tar.gz && \
    tar -xzf v$BASEMAP_VERSION.tar.gz && \
    cd basemap-$BASEMAP_VERSION/ && \
    patch lib/mpl_toolkits/basemap/__init__.py < /patches/0000_basemap.patch && \
    python setup.py install && \
    cd ../../ && \
    rm -rf build/ /patches

# Setup project environment
RUN mkdir -p /processing/cache && \
    mkdir -p /processing/artifacts && \
    mkdir -p /processing/nacs && \
    mkdir -p /processing/wats

ENV CACHE_DIR="/processing/cache" \
    ARTIFACTS_DIR="/processing/artifacts" \
    NACS_DIR="/processing/nacs" \
    WATS_DIR="/processing/wats"

# Project working files
WORKDIR /usr/app
ADD Pipfile* ./

RUN export PATH=/usr/local/bin:$PATH && \
    ln -s /usr/local/bin/python /bin/python && \
    pip install pipenv && \
    pipenv install --system --dev && \
    pipenv install --system

COPY . /usr/app

CMD ["python", "./manage.py", "exec", "all"]
