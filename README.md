
# Selenium Test Automation Project

This project contains Selenium-based automated tests using Python and pytest. The tests are designed to perform various actions such as user registration, login, searching for items, and adding items to the cart on a demo webshop.

## Project Structure

- **Dockerfile**: (Optional) Dockerfile to create a containerized environment for running the tests.
- **test_data.xlsx**: An Excel file containing test data for registration and login tests.
- **test_main.py**: The main test script containing Selenium test cases.
- **.pytest_cache/**: Directory for caching pytest results.
- **.idea/**: Directory for storing IDE-related configuration files (if using an IDE like PyCharm).

Test Cases applied on : "https://demowebshop.tricentis.com/"

1. User Registration
Test Function: test_user_registration
Description: Automates the process of registering a new user using data from the test_data.xlsx file.
Expected Result: The registration should be successful, and the user should be redirected to the homepage.


2. User Login
Test Function: test_user_login
Description: Automates the process of logging in an existing user using data from the test_data.xlsx file.
Expected Result: The login should be successful, and the user's account name should be displayed on the homepage.'


3. Search Item
Test Function: test_search_item
Description: Automates the process of searching for an item in the web store.
Expected Result: The search results should include items that match the search term "laptop".


4. Add Item to Cart
Test Function: test_add_item_to_cart
Description: Automates the process of adding a searched item to the cart.
Expected Result: The item should be successfully added to the cart, and the cart quantity should update accordingly.


## Setup Instructions

1- **activate virtual env** :
     python -m venv venv
     source venv/bin/activate     

2. **Install Dependencies**:
    - Install the required Python libraries:
      ```
      pip3 install pytest pandas openpyxl selenium webdriver_manager faker
      ```
    - Make sure you have Chrome WebDriver installed and accessible in your PATH.

3. **Run the Tests**:
    - To execute the tests, simply run:
      ```
      pytest
      ```

3. **Docker Setup** (Optional):
    - If you prefer to run the tests inside a Docker container, use the provided Dockerfile to build an image and run the container.

## Notes

- Adjust the element locators (e.g., IDs, CSS selectors) in the test script if the webpage structure changes.
- Make sure the Chrome WebDriver version matches your installed Chrome browser version.


