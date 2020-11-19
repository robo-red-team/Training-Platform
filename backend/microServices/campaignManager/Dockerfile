FROM python:latest
RUN pip install flask flask_restful requests
WORKDIR /api
COPY . .
EXPOSE 8855
ENTRYPOINT ["python"]
CMD ["campaignManager.py"]