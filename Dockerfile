FROM python:3.10-bullseye

RUN mkdir /app &&\
    pip3 install flask &&\
    pip3 install waitress

WORKDIR /app

COPY monitor /app

EXPOSE 80  

ENTRYPOINT ["waitress-serve", "--port", "80", "app:app"]