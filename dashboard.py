import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def fetch_daily_sales():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306,
            database="projet"
        )
        cursor = conn.cursor()

        daily_sales = {}
        select_query = """
            SELECT SUBSTRING_INDEX(table_name, '_', 1) AS sale_date, COUNT(*) AS total_sales
            FROM information_schema.tables
            WHERE table_schema = 'projet' AND table_name LIKE '2024%'
            GROUP BY sale_date
        """
        cursor.execute(select_query)
        results = cursor.fetchall()

        for row in results:
            sale_date = row[0]
            total_sales = row[1]
            daily_sales[sale_date] = total_sales

        return daily_sales

    except mysql.connector.Error as e:
        print(f"Error fetching daily sales: {e}")
    finally:
        cursor.close()
        conn.close()

def plot_daily_sales(daily_sales, pdf_file):
    dates = list(daily_sales.keys())
    sales = list(daily_sales.values())

    plt.figure(figsize=(10, 6))
    plt.plot(dates, sales, marker='o', color='skyblue', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.title('Daily Sales Evolution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    pdf_file.savefig()  # Save the current figure to the PDF
    plt.close()  # Close the figure to avoid displaying it on the screen

if __name__ == "__main__":
    daily_sales = fetch_daily_sales()
    if daily_sales:
        with PdfPages('daily_sales.pdf') as pdf:
            plot_daily_sales(daily_sales, pdf)
        print("PDF generated successfully.")
    else:
        print("No data found.")
