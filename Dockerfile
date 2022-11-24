FROM ubuntu:22.04
RUN apt-get -y update
RUN apt-get install --no-install-recommends -y python3 python3-dev python3-venv python3-pip python3-wheel build-essential libmysqlclient-dev && \
 apt-get clean && rm -rf /var/lib/apt/lists/*
ADD . /my-flask-app
WORKDIR /my-flask-app
RUN pip install -r requirements.txt
EXPOSE 5000

# Ensure that the python outputs are streamed to the terminal
ENV PYTHONUNBUFFERED=1

# Run the app with gunicorn on port 5000 with 4 workers, using gevent worker
CMD ["gunicorn","-b", "0.0.0.0:5000", "-w", "4", "-k", "gevent", "--worker-tmp-dir", "/dev/shm", "wsgi:app"]