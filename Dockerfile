FROM python:3.8-slim-buster

# Install Chromium.
RUN apt-get update && \
  apt-get install -y gnupg2 wget && \
  rm -rf /var/lib/apt/lists/* && \
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
  apt-get update && \
  apt-get install -y google-chrome-stable && \
  rm -rf /var/lib/apt/lists/*

# Copy and install deps in container
COPY src/habra_bot.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

# Define working dir
WORKDIR /bots

# Define default cmd
CMD ["python3", "habra_bot.py"]
