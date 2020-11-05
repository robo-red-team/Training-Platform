FROM python:latest
RUN pip install flask flask_restful
WORKDIR /api
COPY . .
EXPOSE 8855
ENTRYPOINT ["python"]
CMD ["datastoreAPI.py"]