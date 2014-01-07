from selenium import webdriver

browser = webdriver.Firefox()

# Open the application home page.
browser.get('http://localhost:8000')
# Check that the page title is correct.
assert 'To-Do' in browser.title
# Quit the browser.
browser.quit()
