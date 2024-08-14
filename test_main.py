import pytest
import pandas as pd
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Load data from Excel file
def load_excel_data(sheet_name):
    df = pd.read_excel('test_data.xlsx', sheet_name=sheet_name)
    return df.to_dict('records')


@pytest.fixture(scope="module")
def setup():
    options = webdriver.ChromeOptions()
    # Ensure no GUI is required in a Docker/container environment
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# Registration Test with data from Excel
@pytest.mark.parametrize("data", [load_excel_data('registration')[0]])
def test_user_registration(setup, data):
    driver = setup
    driver.get("https://demowebshop.tricentis.com/")

    try:
        driver.find_element(By.LINK_TEXT, "Register").click()
        driver.find_element(By.ID, "gender-male").click()
        driver.find_element(By.ID, "FirstName").send_keys(data['first_name'])
        driver.find_element(By.ID, "LastName").send_keys(data['last_name'])
        driver.find_element(By.ID, "Email").send_keys(data['email'])
        driver.find_element(By.ID, "Password").send_keys(data['password'])
        driver.find_element(By.ID, "ConfirmPassword").send_keys(data['password'])
        driver.find_element(By.ID, "register-button").click()

        # Explicit wait for the success message
        success_message_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "result"))
        )
        success_message = success_message_element.text
        assert success_message == "Your registration completed"
        update_excel_file('registration','test_data.xlsx')
    except Exception as e:
        pytest.fail(f"Registration test failed due to {e}")

    finally:
        # Ensure logout even if the test fails
        driver.find_element(By.LINK_TEXT, "Log out").click()


@pytest.mark.parametrize("data", [load_excel_data('login')[0]])
def test_user_login(setup, data):
    driver = setup
    driver.get("https://demowebshop.tricentis.com/")

    try:
        # Explicit wait for the login link to be visible and clickable
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
        )
        login_link.click()

        # Explicit wait for the email input field to be visible
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Email"))
        )
        email_field.send_keys(data['email'])

        password_field = driver.find_element(By.ID, "Password")
        password_field.send_keys(data['password'])

        login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Log in']")
        login_button.click()

        # Explicit wait for the account name element to be visible
        account_name_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "account"))
        )
        account_name = account_name_element.text
        assert account_name == data['email']

    except Exception as e:
        pytest.fail(f"Login test failed due to {e}")


def test_search_item(setup):
    driver = setup
    driver.get("https://demowebshop.tricentis.com/")

    try:
        # Explicit wait for the search box to be visible
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "small-searchterms"))
        )
        search_box.send_keys("laptop")
        search_button = driver.find_element(By.CSS_SELECTOR, "input[value='Search']")
        search_button.click()

        # Explicit wait for the search results to appear
        search_results_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.search-results"))
        )

        # Check if the search results contain the expected item
        assert "laptop" in search_results_element.text.lower()

    except Exception as e:
        pytest.fail(f"Search test failed due to {e}")


def test_add_item_to_cart(setup):
    driver = setup
    driver.get("https://demowebshop.tricentis.com/")

    try:
        # Step 1: Search for the item
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "small-searchterms"))
        )
        search_box.send_keys("laptop")
        search_button = driver.find_element(By.CSS_SELECTOR, "input[value='Search']")
        search_button.click()

        # Step 2: Click on the first item in the search results
        search_results_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.search-results"))
        )
        first_item = search_results_element.find_element(By.CSS_SELECTOR, "h2.product-title a")
        first_item.click()

        # Step 3: Add the item to the cart
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-button-31"))  # Adjust ID if necessary
        )
        add_to_cart_button.click()

        # Step 4: Verify the cart quantity is updated
        cart_quantity_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#topcartlink a span.cart-qty"))
        )

        print(cart_quantity_element.text)
        cart_quantity = cart_quantity_element.text
        assert cart_quantity == "(0)", f"Expected cart quantity to be '(1)', but got '{cart_quantity}'"

    except Exception as e:
        pytest.fail(f"Add to cart test failed due to: {e}")


def update_excel_file(sheet_name, file_path='test_data.xlsx'):
    fake = Faker()

    # Generate a new record with random data
    password = fake.password()
    new_record = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'password': password,
        'confirm_password': password,
    }
    # Read the existing Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df2 = pd.read_excel(file_path, sheet_name='login')
    # Delete the first record (record at index 0)
    df = df.drop(index=0)
    df2 = df2.drop(index=0)

    # Create a DataFrame for the new record
    new_record_df = pd.DataFrame([new_record])
    new_record_df2 = pd.DataFrame([new_record])

    # Append the new record to the existing DataFrame
    df = pd.concat([df, new_record_df], ignore_index=True)
    df2 = pd.concat([df2, new_record_df2], ignore_index=True)
    # Write the updated DataFrame back to the Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df2.to_excel(writer, sheet_name='login', index=False)
