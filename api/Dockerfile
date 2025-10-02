FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    unzip \
    curl \
    fonts-liberation \
    libgtk-3-0 \
    libdbus-1-3 \
    libxtst6 \
    libx11-6 \
    libxrender1 \
    libxi6 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libstdc++6 \
    lsb-release \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

RUN GECKO_VERSION="v0.34.0" && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_VERSION/geckodriver-$GECKO_VERSION-linux64.tar.gz && \
    tar -xvzf geckodriver-$GECKO_VERSION-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKO_VERSION-linux64.tar.gz

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5550

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5550"]
