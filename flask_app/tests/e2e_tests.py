from selenium import webdriver
from selenium.webdriver.common.by import By
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
    except Exception as e:
        print("Test Failed in test_add_new_drug:", e)
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
        print("Test Failed in test_order_tracking:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    # Run the test cases
    print("Running test for adding a new drug...")
    test_add_new_drug()
    print("\nRunning test for order tracking...")
    test_order_tracking()
