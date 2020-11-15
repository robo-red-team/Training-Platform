FROM python:latest
RUN pip install flask flask_restful uuid
WORKDIR /api
COPY . .
EXPOSE 8855
ENTRYPOINT ["python"]
CMD ["campaignManager.py"]