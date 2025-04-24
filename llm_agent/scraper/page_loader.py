from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup headless driver
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

def page_loader(path):
    driver.get(path)

    # 💡 Refresh in case dynamic rendering lags on first load
    if "products.html" in path:
        driver.refresh()
        print("🔄 Refreshed product page to force metadata load.")

        try:
            # 💡 This waits specifically for product RAM field to be populated
            WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.ID, "product-ram").text.strip() != ""
            )
            print("✅ Product metadata loaded.")
        except Exception as e:
            print("⚠️ Warning: Product metadata not loaded in time.", e)

    driver.implicitly_wait(3)
    elements = driver.find_elements(By.XPATH, "//*")
    element_list = []
    id_counter = 1

    for el in elements:
        try:
            tag = el.tag_name.lower()
            data = {"id": id_counter, "tag": tag}
            if (text := el.text.strip()):
                data["text"] = text
            for attr in ["href", "src", "alt", "type", "role", "aria-label", "class"]:
                val = el.get_attribute(attr)
                if val:
                    data[attr.replace("-", "_")] = val if attr != "class" else val.split()
            if len(data) > 1:
                element_list.append(data)
                id_counter += 1
        except:
            continue

    return {
        "elements": element_list,
        "raw": driver.page_source
    }

def close_driver():
    driver.quit()
