# Platform-2-Envoy

This application can be run most easily through docker.

## Installation
Clone the repository by running the following command in your terminal or command prompt:
```
git clone https://github.com/walkerad03/Platform-2-Envoy.git
cd Platform-2-Envoy
```

## Docker

Docker Installation Page: https://www.docker.com/products/docker-desktop/

Make sure you have [Docker Desktop][dd] installed and running on your machine. Then follow these steps:
1. Build the application:
    ```
    docker build -t platform-2-envoy .
    ```
2. Run the application using Docker by executing the following command:
    ```
    docker run -p 8080:8080 platform-2-envoy
    ```
3. Once the application is running, you can access it through your web browser using the following URL: http://localhost:8080.

**Please Note:** In case you are using MacOS, it is possible that you will need to prefix your Docker commands with `sudo`, as Docker requires administrator privleges to run.


[dd]:[https://www.docker.com/products/docker-desktop/]
