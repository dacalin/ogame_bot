FROM python:3.8-slim
WORKDIR /var/www

# Install
RUN pip install ogame numpy

# Fix User uids to match ubuntu server
#RUN apk --no-cache add shadow
#RUN usermod -u 1000 www-data
#RUN groupmod -g 1000 www-data
#RUN usermod -u 82 xfs
#RUN groupmod -g 82 xfs
#RUN usermod -u 33 www-data
#RUN groupmod -g 33 www-data

