# Crypto Exchange Data Downloader and Converter

This Django-based web application allows users to download data from crypto exchanges and convert it to convenient CSV and Excel formats.

## Features
- Connects to popular crypto exchanges using APIs to retrieve user data
- Supports multiple exchanges including Binance, Coinbase, and Kraken
- Provides the ability to filter and download data based on various criteria including date range and asset type
- Supports the conversion of data to CSV and Excel formats for easy analysis and manipulation

## Requirements
- Docker
- Docker Compose

## Installation
1. Clone the repository
2. Create a `.env` file in the root directory and set the required environment variables as shown in `.env.example`
3. Run `./run up` to build and start the containers
4. Open the web application in your web browser at `http://localhost:3000`

## Usage
1. Connect your exchange API to the application by providing the required API keys and permissions
2. Select the exchange and data criteria to download data from
3. Download the data in CSV or XSLX format
4. Analyze and manipulate the data as needed

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
