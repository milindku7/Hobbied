FROM python:3.8
ENV HOME /
WORKDIR /
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install pymongo
RUN pip3 install Flask --user
RUN pip install websockets
EXPOSE 8080
CMD python3 -u main.py