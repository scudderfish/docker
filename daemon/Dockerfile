FROM ubuntu:16.04
MAINTAINER Matt Hill <matthill@openalpr.com>


# Setup gpg key and deb repo
RUN apt-get update && apt-get install -y wget && \
    apt-get update && apt-get install -y \
      openalpr openalpr-daemon openalpr-utils libopenalpr-dev \
      python-openalpr \
      supervisor && \
      touch /usr/share/openalpr/is_docker && \
      rm -rf /var/lib/apt/lists/*


# Adjust beanstalkd to also allow remote connections
RUN sed -i 's/BEANSTALKD_LISTEN_ADDR\s*=\s*127.0.0.1/BEANSTALKD_LISTEN_ADDR=0.0.0.0/' /etc/default/beanstalkd

# Expose the beanstalkd port and the web service
EXPOSE 11300 8355

# Allow the plate images to be persisted on the host
VOLUME /var/lib/openalpr/
VOLUME /etc/openalpr/

WORKDIR ~/

# Override script for "service" to allow alprlink to restart service
COPY service-override /bin/systemctl

# Startup script for OpenALPR services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# send over the license key and the alprd configuration
#COPY license.conf /etc/openalpr/license.conf
COPY alprd.conf /etc/openalpr/alprd.conf





RUN apt-get update && apt-get install -y python-pip python-openalpr

COPY src/requirements.txt /opt/openalprapi/

RUN pip install -r /opt/openalprapi/requirements.txt

# send over the license key 
#COPY license.conf /etc/openalpr/license.conf

COPY src/webservice.py /opt/openalprapi/

EXPOSE 8080


CMD ["/usr/bin/supervisord"]
