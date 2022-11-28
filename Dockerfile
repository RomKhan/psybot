FROM python:3.10-alpine
WORKDIR /bot
COPY . .

RUN apk --no-cache add git openssh
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
