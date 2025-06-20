# Gas Price Finder ⛽🇫🇷

## Overview

**Gas Price Finder** is a user-friendly Python desktop application that helps you find the cheapest fuel prices at French gas stations. It fetches real-time data directly from the French Government's public API, allowing you to compare prices for Gazole (Diesel), E10, E85, SP98, and SP95 in your area. With an intuitive interface and fast performance, Gas Price Finder makes it easy to save money every time you refuel.

---

## ✨ Features

- **Live Data:** Always up-to-date fuel prices from the official French Government API.
- **Fast Performance:** Downloads and processes data once, enabling instant price checks.
- **Easy Search:** Enter a postal code or city name to find the best fuel deals nearby.
- **Comprehensive Coverage:** See the lowest prices for all major fuel types.
- **Station Details:** Get the address of the station with the best price.
- **Modern UI:** Clean, organized interface with clear buttons and feedback.

---

## 🛠️ Installation

1. **Install Python 3.x:**  
   Download from [python.org](https://www.python.org/) if not already installed.

2. **Install Required Libraries:**  
   Open your terminal and run:
   ```bash
   pip install requests beautifulsoup4 wget
   ```
   > *Note: `tkinter` is included with most Python installations. `os`, `zipfile`, and `json` are built-in modules.*

---

## 🚀 Usage

1. **Start the Application:**  
   In your terminal, navigate to the project folder and run:
   ```bash
   python gasprice.py
   ```

2. **Download Latest Prices:**  
   Click **"Download Prices"** in the app to fetch the newest fuel data.

3. **Set Your Location:**  
   - To search by postal code, click **"Set Postal Code"** and enter your code.
   - To search by city, enter the city name and click **"Chercher par Ville"**.

4. **View Prices:**  
   Click **"Verify Prices"** to display the lowest prices and station addresses for each fuel type.

5. **Exit:**  
   Click **"Exit"** to close the application.

---

## 🧩 Example Screenshot

![image](https://github.com/user-attachments/assets/fd4fea0a-2269-43ee-8598-8caf5c2122df)


---

## 📝 Roadmap

Planned improvements for future releases:

- **Advanced Location Search:** Search by town or broader area, not just postal code.
- **Database Support:** Store historical prices for trend analysis and offline access.
- **Custom Fuel Selection:** Choose which fuel types to display.
- **Smarter Price Comparison:** Improved algorithms for even more accurate results.
- **UI Enhancements:** Ongoing improvements for a smoother experience.

---

## 📄 License

This project is licensed under the MIT License.

---

*Made with ❤️ for drivers in France!*
