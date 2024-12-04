from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def test_add_new_drug():
    """Test case for adding a new drug."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Navigate to the new drug page
        driver.get("http://127.0.0.1:5001/new-drug")
        print("Navigated to the new drug page.")

        # Fill in the drug information
        driver.find_element(By.NAME, 'name').send_keys("Test Drug")
        driver.find_element(By.NAME, 'company').send_keys("Test Company")
        driver.find_element(By.NAME, 'type').send_keys("Prescription")
        driver.find_element(By.NAME, 'description').send_keys("This is a test drug.")
        driver.find_element(By.NAME, 'stock').send_keys("100")

        # Wait for the submit button (input element) and click
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.add-button'))
        )
        submit_button.click()

        # Verify redirection to inventory monitoring page
        WebDriverWait(driver, 10).until(EC.url_contains("/inv-monitoring"))
        print("Test Passed: New drug added and redirected successfully.")

        try:
            # Delete the test drug to avoid filling the database with vacuous data
            table = driver.find_element(By.CSS_SELECTOR, 'table')
            rows = table.find_elements(By.CSS_SELECTOR, 'tbody > tr')     # Get all rows within the table body
            last_row = rows[-1]
            delete_button = last_row.find_element(By.XPATH, './/button[contains(text(), "Delete")]')    # .// searches for any descendants
            delete_button.click()
            WebDriverWait(driver, 10).until(EC.url_contains("/delete-drug"))
            driver.find_element(By.CSS_SELECTOR, 'input[value="Yes"]').click()
            print("Test drug sucessfully deleted in cleanup.")
        except Exception as e:
            print("Failed to delete test drug in cleanup. ")

    except Exception as e:
        print("Test Failed in test_add_new_drug: ", e)
    finally:
        driver.quit()
        
def test_order_tracking():
    """Test case for verifying the order tracking page."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # Navigate to the order tracking page
        driver.get("http://127.0.0.1:5001/order-tracking")
        print("Navigated to the order tracking page.")

        # Verify the page loads and contains a table
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("Test Passed: Order tracking page loaded successfully.")
    except Exception as e:
        print("Test Failed in test_order_tracking: ", e)
    finally:
        driver.quit()

def test_add_new_order():
    """Test case for adding a new order."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Navigate to the new order page
        driver.get("http://127.0.0.1:5001/new-order")
        print("Navigated to the new order page.")

        # Fill in the order information
        driver.find_element(By.NAME, 'name').send_keys("Test Order")
        driver.find_element(By.NAME, 'date_of_purchase').send_keys("2004")
        driver.find_element(By.NAME, 'date_of_purchase').send_keys(Keys.TAB)
        driver.find_element(By.NAME, 'date_of_purchase').send_keys("0101")
        driver.find_element(By.NAME, 'pickup_or_delivery').send_keys("P")
        driver.find_element(By.NAME, 'status').send_keys("A")

        # Wait for the submit button (input element) and click
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.add-button'))
        )
        submit_button.click()

        # Verify redirection to order tracking page
        WebDriverWait(driver, 10).until(EC.url_contains("/order-tracking"))
        print("Test Passed: New order added and redirected successfully.")

        try:
            # Delete the test order to avoid filling the database with vacuous data
            table = driver.find_element(By.CSS_SELECTOR, 'table')
            rows = table.find_elements(By.CSS_SELECTOR, 'tbody > tr')     # Get all rows within the table body
            last_row = rows[-1]
            delete_button = last_row.find_element(By.XPATH, './/button[contains(text(), "Delete")]')    # .// searches for any descendants
            delete_button.click()
            WebDriverWait(driver, 10).until(EC.url_contains("/delete-order"))
            driver.find_element(By.CSS_SELECTOR, 'input[value="Yes"]').click()
            print("Test order sucessfully deleted in cleanup.")
        except Exception as e:
            print("Failed to delete test order in cleanup. ",)

    except Exception as e:
        print("Test Failed in test_add_new_order: ", e)
    finally:
        driver.quit()

def test_inv_monitoring():
    """Test case for verifying the inventory monitoring page."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # Navigate to the inventory monitoring page
        driver.get("http://127.0.0.1:5001/inv-monitoring")
        print("Navigated to the inventory monitoring page.")

        # Verify the page loads and contains a table
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("Test Passed: Inventory Monitoring page loaded successfully.")
    except Exception as e:
        print("Test Failed in test_inv-monitoring: ", e)
    finally:
        driver.quit()

def test_browse_drug():
    """Test case for verifying the browse drugs page."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # Navigate to the browse drugs page
        driver.get("http://127.0.0.1:5001/browse-drug")
        print("Navigated to the browse drugs page.")

        # Verify the page loads and contains a table
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("Test Passed: Browse Drugs page loaded successfully.")
    except Exception as e:
        print("Test Failed in test_browse_drug: ", e)
    finally:
        driver.quit()

def test_drug_info():
    """Test case for verifying the drug info page."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # Navigate to the drug info page
        driver.get("http://127.0.0.1:5001/drug-info")
        print("Navigated to the drug info page.")

        # Verify the page loads and contains a table
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#info-section")))
        print("Test Passed: Drug info page loaded successfully.")
    except Exception as e:
        print("Test Failed in test_drug_info: ", e)
    finally:
        driver.quit()

def test_dashboard():
    """Test case for verifying the dashboard page."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        # Navigate to the dashboard page
        driver.get("http://127.0.0.1:5001/")
        print("Navigated to the dashboard page.")

        # Verify the page loads and contains a table
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("Test Passed: Dashboard page loaded successfully.")
    except Exception as e:
        print("Test Failed in test_dashboard: ", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    # Run the test cases
    print("Running test for adding a new drug...")
    test_add_new_drug()
    print("\nRunning test for order tracking...")
    test_order_tracking()
    print("\nRunning test for adding a new order...")
    test_add_new_order()
    print("\nRunning test for inventory monitoring...")
    test_inv_monitoring()
    print("\nRunning test for browse drug...")
    test_browse_drug()
    print("\nRunning test for drug info...")
    test_drug_info()
    print("\nRunning test for dashboard...")
    test_dashboard()
