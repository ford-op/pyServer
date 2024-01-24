FROM python:3
ADD server.py server.py
ADD entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
EXPOSE 8080
ENTRYPOINT /entrypoint.sh