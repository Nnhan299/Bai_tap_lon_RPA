from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import datetime
import schedule

def crawl_data():
    # 1. Vào website đã chọn.
    driver = webdriver.Chrome()
    driver.get('https://alonhadat.com.vn/')
    wait = WebDriverWait(driver, 10)


    advanced_search = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Tìm kiếm nâng cao')]")))
    advanced_search.click()

    # 2. Click chọn bất kì Tỉnh/TP(Hà Nội, Đà Nẵng, Hồ Chí Minh, …). 
    province_select = wait.until(EC.presence_of_element_located((By.ID, "tinh")))
    province_options = province_select.find_elements(By.TAG_NAME, "option")
    popular_provinces = ['Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Bình Dương', 'Đồng Nai', 'Hải Phòng']
    filtered_options = [opt for opt in province_options if opt.text.strip() in popular_provinces]
    random_province = random.choice(filtered_options)
    random_province.click()

    # Chọn bất kì loại nhà đất(Căn hộ chung cư, nhà, đất, …).
    properties_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "properties")))
    property_checkboxes = properties_div.find_elements(By.TAG_NAME, "input")
    checkbox = random.choice(property_checkboxes)
    checkbox.click()

    # 3. Click nút "Tìm kiếm"
    time.sleep(0.5)
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Tìm kiếm']")))
    search_button.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".content-item")))

    # 4. Lấy tất cả dữ liệu(Tiêu đề, Mô tả, Địa chỉ, Diện tích, Giá) hiển thị ở bài viết.
    titles = []
    descriptions = []
    addresses = []
    areas = []
    prices = []

    posts = driver.find_elements(By.CSS_SELECTOR, ".content-item")
    print(f"Tìm thấy {len(posts)} bài viết")
    main_window = driver.current_window_handle
    
    # 5. Lấy tất cả dữ liệu của các trang.
    for post in posts:
        try:
            # Lấy link và click vào bài viết
            title_element = post.find_element(By.CSS_SELECTOR, ".ct_title a")
            title = title_element.text.strip()
            link = title_element.get_attribute('href')
            
            # Mở link trong tab mới
            driver.execute_script(f"window.open('{link}', '_blank');")
            time.sleep(1)
            
            # Chuyển sang tab mới
            new_window = [window for window in driver.window_handles if window != main_window][0]
            driver.switch_to.window(new_window)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "detail")))
            
            # Lấy thông tin chi tiết
            try:
                description = driver.find_element(By.CLASS_NAME, "detail").text.strip()
            except:
                description = "Không có thông tin"
                
            try:
                address = driver.find_element(By.CLASS_NAME, "address").text.strip()
            except:
                address = "Không có thông tin"
                
            try:
                area = driver.find_element(By.CLASS_NAME, "square").text.strip()
            except:
                area = "Không có thông tin"
                
            try:
                price = driver.find_element(By.CLASS_NAME, "price").text.strip()
            except:
                price = "Không có thông tin"

            # Thêm vào danh sách
            titles.append(title)
            descriptions.append(description)
            addresses.append(address)
            areas.append(area)
            prices.append(price)

           
            driver.close()
            driver.switch_to.window(main_window)
            
           
            time.sleep(random.uniform(0.5, 1))
            
        except Exception as e:
            print(f"Lỗi khi lấy bài: {e}")
            try:
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(main_window)
            except:
                print("Không thể xử lý lỗi tab, khởi tạo lại driver...")
                driver.quit()
                driver = webdriver.Chrome()
                driver.get('https://alonhadat.com.vn/')
            continue

    print(f"Số bài viết tìm được: {len(titles)}")

    # 6. Lưu ra file CSV
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'alonhadat_data.csv'
    df = pd.DataFrame({
        'Tiêu đề': titles,
        'Mô tả': descriptions,
        'Địa chỉ': addresses,
        'Diện tích': areas,
        'Giá': prices
    })
    df.to_csv(filename, index=False, encoding='utf-8-sig')

    print(f"Đã lưu dữ liệu vào file: {filename}")
    driver.quit()
    
    
# 7. Set lịch chạy vào lúc 6h sáng hằng ngày.
schedule.every().day.at("06:00").do(crawl_data)
while True:
    schedule.run_pending()
    time.sleep(60)
