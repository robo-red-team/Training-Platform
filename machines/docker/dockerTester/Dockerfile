FROM python:latest
RUN pip install flask flask_restful
WORKDIR /webApp
COPY . .
EXPOSE 8855
ENTRYPOINT ["python"]
CMD ["startServer.py"]