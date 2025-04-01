# Gas Price Finder

## Introduction

This Python program retrieves the lowest fuel prices (starting with Diesel) from the public data provided by the French Government. It processes the data to identify the lowest price for Gazole (Diesel) and other fuel types.

## Features
- Fetches real-time fuel price data from the French Government's public API.
- Identifies the lowest price for Gazole (Diesel).
- Displays additional fuel prices (E10, E85, SP98, SP95) when available.
- Provides the location of the gas station with the lowest price.

## Requirements
- Python 3.x
- Required libraries:
  - `requests`
  - `BeautifulSoup` (from `bs4`)
  - `tkinter`
  - `wget`

## Usage
1. Run the program.
    ```bash
    py gasprice.py
    
2. Dowload the latest price using the "Download Prices" Button
3. Select "Verify Price" Button
3. Enter your postal code when prompted.
3. View the lowest fuel prices and the location of the gas station.

## Notes
- Currently, the program focuses on finding the lowest Gazole (Diesel) price.
- Future updates will include better handling of additional fuel types and improved error management.
- Future updates will include better UI 

## License
This project is licensed under the MIT License.
