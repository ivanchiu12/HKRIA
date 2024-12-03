import time
import pandas as pd
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import schedule
import datetime

# List of URLs, corresponding dataset names, and file paths
data_urls = [
    ("https://data.eastmoney.com/cjsj/yhll.html", "央行基准利率", r"C:\HKRIA\webscraping\data\央行基准利率.xlsx"),
    ("https://data.eastmoney.com/cjsj/gdzctz.html", "社会固定资产投资", r"C:\HKRIA\webscraping\data\社会固定资产投资.xlsx"),
    ("https://data.eastmoney.com/shibor/shibor/001,CNY,301.html", "上海银行间同业拆借利率SHIBOR", r"C:\HKRIA\webscraping\data\上海银行间同业拆借利率SHIBOR.xlsx"),
    ("https://data.eastmoney.com/cjsj/hjwh.html", "外汇和黄金储备", r"C:\HKRIA\webscraping\data\外汇和黄金储备.xlsx"),
    ("https://data.eastmoney.com/cjsj/cpi.html", "居民消费价格指数CPI", r"C:\HKRIA\webscraping\data\居民消费价格指数CPI.xlsx"), 
    ("https://data.eastmoney.com/cjsj/xfzxx.html", "消费者信心指数", r"C:\HKRIA\webscraping\data\消费者信心指数.xlsx"),
    ("https://data.eastmoney.com/cjsj/qyjqzs.html", "企业景气及企业家信心指数",  r"C:\HKRIA\webscraping\data\企业景气及企业家信心指数.xlsx"),
    ("https://data.eastmoney.com/cjsj/xfp.html", "社会消费品零售总额", r"C:\HKRIA\webscraping\data\社会消费品零售总额.xlsx" ),
    ("https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0L08&sj=2023", "社会融资总额", r"C:\HKRIA\webscraping\data\社会融资总额.xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0801&sj=202410", "进出口总额", r"C:\HKRIA\webscraping\data\进出口总值.xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0D01&sj=202410", "货币和准货币供应量", r"C:\HKRIA\webscraping\data\货币供应量.xlsx" ),
    
    ("https://data.stats.gov.cn/easyquery.htm?cn=B01", "GDP-季度", r"C:\HKRIA\webscraping\data\国内生产总值GDP.xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=C01", "GDP-年度", r"C:\HKRIA\webscraping\data\国内生产总值GDP_annuel.xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A040N&sj=2023", "失业率", r"C:\HKRIA\webscraping\data\失业率.xlsx"),
    # ("https://data.stats.gov.cn/easyquery.htm?cn=A01", "工业生产者出厂价格指数PPI", r"C:\HKRIA\webscraping\data\工业品出厂价格指数PPI.xlsx"),
    
    ("https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0801&sj=2023", "年度财政收支", r"C:\HKRIA\webscraping\data\财政收入支出.xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0C01&sj=202410", "月度财政收支", r"C:\HKRIA\webscraping\data\财政收入支出_月.xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A080401&sj=2023", "年度各项税收", r"C:\HKRIA\webscraping\data\财政税收.xlsx"),
    
    ("https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0B03&sj=202410", "综合PMI", r"C:\HKRIA\webscraping\data\采购经理指数(PMI).xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0B03&sj=202410", "制造业采购经理指数", r"C:\HKRIA\webscraping\data\采购经理指数(PMI).xlsx"),
    ("https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0B03&sj=202410", "非制造业采购经理指数", r"C:\HKRIA\webscraping\data\采购经理指数(PMI).xlsx"),


]

# Function to initialize the web driver
def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(executable_path=r"C:\\HKRIA\\chromedriver.exe"), options=options)
    return driver

# Function to click the dropdown and select an option
def select_third_option(driver):
    try:
        # Wait for dropdown to load
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dtHead')))
        
        # Find and click the dropdown
        dt_heads = driver.find_elements(By.CLASS_NAME, 'dtHead')
        if dt_heads:
            dt_heads[0].click()
            time.sleep(1)  # Allow the dropdown to load
            
            # Find and click the third option
            dt_list = driver.find_element(By.CLASS_NAME, 'dtList')
            options = dt_list.find_elements(By.TAG_NAME, 'li')
            if len(options) >= 3:
                options[2].click()
                time.sleep(3)  # Wait for the data to load
            else:
                print("Less than 3 options available in the dropdown.")
                return False
        else:
            print("Dropdown not found.")
            return False
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error while selecting third option: {e}")
        return False
    return True

# Function to scrape table data
def scrape_table_data(driver):
    try:
        # Locate the table and extract HTML
        table = driver.find_element(By.CLASS_NAME, 'table_fix')
        html_content = table.get_attribute('outerHTML')
        df = pd.read_html(io.StringIO(html_content), header=0)[0]
        return df
    except NoSuchElementException as e:
        print(f"Table not found: {e}")
        return None

# Function to scrape table data for Eastmoney
def scrape_table_data_eastmoney(driver):
    all_data = []
    while True:
        try:
            # Locate the table and extract HTML
            table = driver.find_element(By.CLASS_NAME, 'table-model')
            html_content = table.get_attribute('outerHTML')
            df = pd.read_html(io.StringIO(html_content), header=0)[0]
            all_data.append(df)
        except NoSuchElementException as e:
            print(f"Table not found: {e}")
            break
        
        # Check if next page button exists and click it
        try:
            next_button = driver.find_element(By.XPATH, "//a[text()='下一页']")
            next_button.click()
            time.sleep(2)  # Wait for the new page to load
        except NoSuchElementException:
            break
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return None

# Main function to scrape dataset
def scrape_dataset(url, dataset_name, file_path):
    # Load existing data or create a new DataFrame
    try:
        existing_df = pd.read_excel(file_path)
    except FileNotFoundError:
        existing_df = pd.DataFrame()
    
    # Initialize the WebDriver
    driver = initialize_driver()
    try:
        # Load the webpage
        driver.get(url)

        # Select the third option from the dropdown if available
        if "stats.gov.cn" in url:

            if not select_third_option(driver):
                return
            df = scrape_table_data(driver)    
            if df is not None:
                # Transpose the DataFrame to match the expected format
                df = df.set_index(df.columns[0]).transpose().reset_index()
                df.rename(columns={'index': '时间'}, inplace=True)
                
                # Clean and format the data
                df = df.apply(pd.to_numeric, errors='ignore')
                
                # Update the existing DataFrame
                combined_df = pd.concat([df, existing_df], ignore_index=True)
                combined_df.drop_duplicates(subset='时间', keep='last', inplace=True)
                
                # Save the updated DataFrame to Excel
                combined_df.to_excel(file_path, index=False)
                print(f"Data for {dataset_name} successfully updated.")
            else:
                print(f"Failed to scrape table data for {dataset_name}.")
        
        # Scrape the table data
        if "eastmoney.com" in url:
            df = scrape_table_data_eastmoney(driver)        
            print(df)
            if df is not None:
                # Update the existing DataFrame
                combined_df = pd.concat([df, existing_df], ignore_index=True)
                combined_df.drop_duplicates(inplace=True)
                
                # Save the updated DataFrame to Excel
                combined_df.to_excel(file_path, index=False)
                print(f"Data for {dataset_name} successfully updated.")
            else:
                print(f"Failed to scrape table data for {dataset_name}.")
    finally:
        driver.quit()

# Execute scraping for all datasets
if __name__ == "__main__":
    for url, dataset_name, file_path in data_urls:
        scrape_dataset(url, dataset_name, file_path)
'''
# Function to run all scraping tasks
def run_all_scraping_tasks():
    for url, dataset_name, file_path in data_urls:
        scrape_dataset(url, dataset_name, file_path)

# Schedule the task to run every Monday at 09:00 AM
schedule.every().monday.at("09:00").do(run_all_scraping_tasks)

# Keep the script running to check for the scheduled task
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
'''