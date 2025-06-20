
# Gas Price Finder ⛽🇫🇷


## Table of Contents

  - [Overview](https://www.google.com/search?q=%23overview)
  - [Features](https://www.google.com/search?q=%23features)
  - [Installation](https://www.google.com/search?q=%23installation)
  - [Usage](https://www.google.com/search?q=%23usage)
  - [Future Enhancements (Roadmap)](https://www.google.com/search?q=%23future-enhancements-roadmap)
  - [License](https://www.google.com/search?q=%23license)

## Overview

Welcome to **Gas Price Finder** – your essential Python desktop application for discovering the most affordable fuel options across France\! This intuitive tool is meticulously designed to pull real-time fuel data directly from the French Government's public API. Whether you're looking for Gazole (Diesel), E10, E85, SP98, or SP95, Gas Price Finder quickly processes this information to highlight the lowest prices in your specified postal code area, ensuring you make smart fueling choices.

## ✨ Features

  * **Real-time Data Acquisition:** Fetches the very latest fuel price data directly from the official French Government public API.
  * **Optimized Performance:** Thanks to recent improvements, data is downloaded and efficiently stored in memory once, making subsequent price verifications remarkably fast.
  * **Localized Price Discovery:** Simply input a French postal code to swiftly find the best fuel deals in your desired region.
  * **Comprehensive Fuel Coverage:** Identifies and displays the lowest price for Gazole, and also provides up-to-date prices for E10, E85, SP98, and SP95 available at the best-priced station.
  * **Station Location Details:** Provides the precise address of the gas station offering the lowest prices, making it easy to plan your route.
  * **Enhanced User Interface:** Boasts a cleaner, more organized graphical interface with improved button positioning for a smoother user experience.

## 🛠️ Installation

To set up Gas Price Finder on your machine, follow these simple steps:

1.  **Ensure Python 3.x is installed:**
    If you don't have Python, download it from [python.org](https://www.python.org/).

2.  **Install Required Libraries:**
    Open your terminal or command prompt and run the following command to install the necessary Python packages:

    ```bash
    pip install requests beautifulsoup4 wget
    ```

    *(Note: `tkinter` is typically included with standard Python installations, and `os`, `zipfile`, `json` are built-in modules.)*

## 🚀 Usage

Using Gas Price Finder is straightforward:

1.  **Launch the Application:**
    Navigate to the directory containing `gasprice.py` in your terminal and execute:

    ```bash
    python gasprice.py
    ```

2.  **Download Latest Prices:**
    Upon the application window appearing, click the **"Download Prices"** button. This is a crucial step that fetches and loads the most current fuel data. You'll receive a confirmation message once the download and processing are complete.

3.  **Enter Your Postal Code:**
    Next, click the **"Code Postale"** button. A small pop-up window will prompt you to enter the French postal code for the area where you wish to find prices.

4.  **Verify Prices:**
    Once the postal code is entered (and after you've downloaded the data), click the **"Verify Price"** button. The application will then display the lowest fuel prices available in your specified region, along with the address of the corresponding gas station.

## 🚧 Future Enhancements (Roadmap)

We are committed to continuously improving Gas Price Finder. Here's a glimpse of what's planned for future versions:

  * **Customizable Location Search:** Enhance the ability for users to specify towns or broader geographical areas, not just postal codes.
  * **Database Integration:** Implement a robust database backend to store historical fuel data, paving the way for advanced features like price trend analysis and offline access.
  * **Fuel Type Selection:** Introduce options for users to select specific fuel types they want to search for, providing more tailored results.
  * **Enhanced Price Logic:** Further refine the price comparison algorithms to ensure even greater accuracy and a more seamless user experience across all fuel types and stations.
  * **Ongoing UI Improvements:** Continued development and polishing of the user interface for a more modern, intuitive, and fluid experience.

## 📄 License

This project is licensed under the MIT License.

-----