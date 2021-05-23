FROM php:7.4.2-apache-buster

ARG DEBIAN_FRONTEND=noninteractive

# Update
RUN apt-get clean && \
    apt-get -y update --fix-missing && \
    apt-get upgrade -y && \
    apt-get --no-install-recommends install -y apt-utils && \
    rm -rf /var/lib/apt/lists/*

# Install useful tools and install important libaries
RUN apt-get -y update && \
    apt-get -y --no-install-recommends install nano wget \
    dialog \
    libsqlite3-dev \
    libsqlite3-0 && \
    apt-get -y --no-install-recommends install default-mysql-client \
    zlib1g-dev \
    libzip-dev \
    libicu-dev && \
    apt-get -y --no-install-recommends install --fix-missing apt-utils \
    build-essential \
    git \
    curl \
    vim \
    net-tools \
    libonig-dev && \ 
    apt-get -y --no-install-recommends install --fix-missing libcurl4 \
    libcurl4-openssl-dev \
    zip \
    openssl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Install xdebug
RUN pecl install xdebug-2.9.8 && \
    docker-php-ext-enable xdebug 

## Install runkit
#RUN pecl install runkit7-4.0.0a2 && \
#    docker-php-ext-enable runkit7

# Install uopz
RUN pecl install uopz && \
    docker-php-ext-enable uopz 

	
# Install imagick
RUN apt-get update && \
    apt-get -y --no-install-recommends install --fix-missing libmagickwand-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pecl install imagick && \
    docker-php-ext-enable imagick

# Other PHP7 Extensions
RUN docker-php-ext-install pdo_mysql && \
    docker-php-ext-install pdo_sqlite && \
    docker-php-ext-install mysqli && \
    docker-php-ext-install curl && \
    docker-php-ext-install tokenizer && \
    docker-php-ext-install json && \
    docker-php-ext-install zip && \
    docker-php-ext-install -j$(nproc) intl

# Install ioncube loader
RUN mkdir -p /usr/local/ioncube
COPY ioncube_loader_lin_7.4.so /usr/local/ioncube
COPY .bashrc /root/.bashrc

# Generate cert
RUN mkdir -p /etc/apache2/ssl/
RUN openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -subj "/C=US/ST=./L=./O=./CN=phishpond.local" -keyout /etc/apache2/ssl/ssl.key -out /etc/apache2/ssl/ssl.crt

# Enable apache modules
RUN a2enmod proxy_http
RUN a2enmod rewrite headers
RUN a2enmod dump_io
RUN a2enmod ssl


# Copy in mail wrapper script
COPY phpsendmail /usr/local/bin/phpsendmail
RUN chmod +x /usr/local/bin/phpsendmail

# Cleanup
RUN rm -rf /usr/src/*

