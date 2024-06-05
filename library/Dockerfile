FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV EMAIL_PASSWORD="oihn jrkr tsoc xdwv"
EXPOSE 5000
ENV FLASK_APP=library.py
CMD ["python", "library.py"]
