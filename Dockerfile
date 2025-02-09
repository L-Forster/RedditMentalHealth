FROM ubuntu:latest
LABEL authors="louis"

ENTRYPOINT ["top", "-b"]