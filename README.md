# Daily Sales Tracker

## Description

This Python script connects to a MySQL database to fetch daily sales data and plots the sales evolution over time using Matplotlib. The resulting graph is saved to a PDF file.

## Prerequisites

- Python 3.x
- `mysql-connector-python` library
- `matplotlib` library

## Installation

1. Install Python 3.x from the [official website](https://www.python.org/downloads/).
2. Install required Python libraries using pip:

    ```bash
    pip install mysql-connector-python matplotlib
    ```

3. Ensure MySQL is installed and running on your system.

## Usage

1. Ensure your MySQL server is running and accessible.
2. Modify the database connection parameters in the script (`host`, `user`, `password`, `port`, `database`) to match your MySQL setup.
3. Run the script using Python:

    ```bash
    python daily_sales_tracker.py
    ```

4. If sales data is found in the database, a PDF file named `daily_sales.pdf` will be generated in the current directory containing the sales evolution graph. If no data is found, a message indicating so will be displayed.
