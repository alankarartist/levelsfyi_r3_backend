# Sensor Data Processing Application

This project is a web application designed to ingest, process, and store sensor data using Flask, MongoDB, and Python. The application architecture consists of an API service and a MongoDB database, managed using Docker Compose.

## Features

- **API Service**: Built with Flask, the API service handles incoming requests to ingest sensor data.
- **Data Ingestion**: Data ingestion and processing are handled by `ingestion.py`.
- **Data Retrieval**: Data retrieval is handled by `retrieval.py`.
- **Database**: MongoDB is used to store sensor data.
- **Dockerized Setup**: Docker Compose is used to set up and manage the API service and MongoDB.

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
