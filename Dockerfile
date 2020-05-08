FROM alpine:3.8

RUN apk add --no-cache \
        bash \
        firefox-esr \
        python3

WORKDIR /grabber
ADD . /grabber/

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "grabber.py"]
