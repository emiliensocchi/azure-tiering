FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 python3-pip git -y

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]