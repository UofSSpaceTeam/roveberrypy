FROM frolvlad/alpine-python3

RUN apk add --update git

ADD requirements.txt /src/requirements.txt

RUN pip3 install -r /src/requirements.txt

COPY ./roverprocess /src/roverprocess

COPY main.py /src

EXPOSE 8080

WORKDIR /src

RUN git clone https://github.com/UofSSpaceTeam/rover-webui.git

RUN mv rover-webui/WebUI ./WebUI && rm -rf rover-webui

RUN ls WebUI

CMD ["python3", "main.py"]
