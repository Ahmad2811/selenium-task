# Use a specific version of Ubuntu to ensure package availability
FROM ubuntu:20.04

# Avoiding interactive dialogue from apt-get and setting default timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg curl lsb-release python3 python3-pip unzip && \
    wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome.deb || apt-get -f install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* google-chrome.deb


RUN apt-get install -y libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libxkbcommon0 libxdamage1 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libatspi2.0-0 libgtk-3-0

# Verify Chrome installation
RUN google-chrome --version

# Install ChromeDriver
RUN wget -q "https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Set the working directory
WORKDIR /usr/src/app

# Copy your application files
COPY . /usr/src/app

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install pytest pandas openpyxl selenium webdriver_manager faker

# Run tests or specify the default command
CMD ["pytest"]
