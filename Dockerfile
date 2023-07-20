FROM python:3.10-alpine
RUN apk --no-cache add git openssh
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN pip install "cython<3.0.0" && pip install --no-build-isolation pyyaml==6.0

WORKDIR /bot
COPY requirements.txt requirements.txt
RUN --mount=type=ssh pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN --mount=type=ssh pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
