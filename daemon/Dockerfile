FROM ubuntu:20.04
MAINTAINER David Smith <davegsmith@gmail.com>

ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN  apt-get update && apt-get install -y wget
RUN apt-get install -y git-core build-essential autoconf automake libtool cmake libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y  libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev libopencv-dev libleptonica-dev leptonica-progs  tesseract-ocr-eng libtesseract-dev gimagereader  liblog4cplus-dev libcurl3-dev supervisor  
RUN apt-get install -y  python-dev python-numpy 


RUN git clone https://github.com/openalpr/openalpr.git && \
  cd openalpr/src && \
  cd ../src && \
  mkdir build && \
  cd build && \
  cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc .. && \
  make -j 8 && \
  make install

RUN pwd
RUN ls -lrt
RUN cd openalpr/src/bindings/python && \
  python3 -V && \
  python3 setup.py install 

# Allow the plate images to be persisted on the host
VOLUME /var/lib/openalpr/
VOLUME /etc/openalpr/

WORKDIR ~/

# Override script for "service" to allow alprlink to restart service
COPY service-override /bin/systemctl

# Startup script for OpenALPR services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY alprd.conf /etc/openalpr/alprd.conf

COPY src/webservice.py /opt/openalprapi/

EXPOSE 8080


CMD ["/usr/bin/supervisord"]
