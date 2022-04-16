FROM python:3.8-slim
WORKDIR /var/www

# Install
RUN pip install ogame numpy
RUN pip install supervisor
RUN mkdir /etc/supervisor
RUN mkdir /etc/supervisor/jobs

# Copy files
COPY ./etc/supervisor/supervisord.conf /etc/supervisor/supervisord.conf

# Command
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf", "--nodaemon"]


