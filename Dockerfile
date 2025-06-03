FROM python
WORKDIR /usr/src/app
EXPOSE 8000
ENTRYPOINT ["tail", "-f", "/dev/null"]