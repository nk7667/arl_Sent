from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains  
import time  
import os  

#⭐ 配置你的 ChromeDriver 路径  或替换成其他浏览器
driver_path = "C:/Userschromedriver.exe"
#⭐ 配置你的灯塔策略配置路径  
url = "https://127.0.0.1:5003/policy"  
#Chrome 用户数据目录  
options = Options()  
options.add_argument("--ignore-certificate-errors")  
options.add_argument("--disable-blink-features=AutomationControlled")  

# ⭐确定你的Chrome 用户配置文件地址，是新生成的 注意编译器有无生成文件的权限 （首次需要手动登录，之后就可以复用此配置文件）
options.add_argument(f"--user-data-dir=C:\\Program Files\\Google\\Chrome\\Application\\133.0.6943.142")  
options.add_argument("--profile-directory=Default")  # 生成配置文件，可根据需要更改  

# 从文件中读取目标列表  
def read_targets(file_path):  
    targets = []  
    try:  
        with open(file_path, 'r', encoding='utf-8') as file:  
            for line in file:  
                line = line.strip()  
                if line:  
                    # 使用中文冒号分割名称和域名  
                    parts = line.split('：')  
                    if len(parts) == 2:  
                        university_name = parts[0].strip()  
                        domain = parts[1].strip()  
                        targets.append((university_name, domain))  
    except Exception as e:  
        print(f"读取文件出错: {e}")  
    return targets  

# 初始化浏览器  
service = Service(executable_path=driver_path)  
driver = webdriver.Chrome(service=service, options=options)  
wait = WebDriverWait(driver, 30)  

try:  
    # 访问目标灯塔网站 
    driver.get(url)  
    
    # 等待页面完全加载  
    time.sleep(5)  
    
    # 从桌面读取yuming.txt文件  
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  
    file_path = os.path.join(desktop_path, "yuming.txt")  
    
    # 读取目标列表  
    targets = read_targets(file_path)  
    print(f"从文件中读取了 {len(targets)} 个目标")  
    
    # 逐个处理目标  
    for idx, (university_name, domain) in enumerate(targets, 1):  
        print(f"\n处理第 {idx}/{len(targets)} 个目标: {university_name} - {domain}")  
        
        # 点击任务下发按钮  
        try:  
            print("点击任务下发按钮...")  
            button = wait.until(EC.element_to_be_clickable((By.XPATH,   
                '//button[contains(@class, "edit-icon") and contains(@class, "ant-btn")]')))  
            button.click()  
        except Exception as e:  
            print(f"点击任务下发按钮失败: {e}")  
      
        
        time.sleep(1)  
        
        # 填写任务名称
        print(f"填写任务名称: {university_name}")  
        try:  
            # 使用XPath定位任务名输入框  
            task_name_input = wait.until(EC.presence_of_element_located((By.XPATH,   
                '//input[@placeholder="请输入任务名称"]')))  
            task_name_input.clear()  
            task_name_input.send_keys(university_name)  
        except Exception as e:  
            print(f"定位任务名输入框失败: {e}")  
        
        # 填写目标域名  
        print(f"填写目标域名: {domain}")  
        try:  
            # 使用id精确定位目标文本区域  
            target_textarea = wait.until(EC.presence_of_element_located((By.ID, 'target')))  
            target_textarea.clear()  
            target_textarea.send_keys(domain)  
        except Exception as e:  
            print(f"通过ID定位目标文本区域失败: {e}")  
      
        
        # 然后选择任务类型  
        print("选择任务类型...")  
        try:  
            # 使用id精确定位任务类型下拉框  
            task_type_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'task_tag')))  
            driver.execute_script("arguments[0].click();", task_type_dropdown)  
        except Exception as e:  
            print(f"通过ID定位任务类型下拉框失败: {e}")  
 
        
        # 等待下拉选项出现并选择"资产侦查任务" 
        time.sleep(1)  
        try:  
            # 匹配下拉选项  
            asset_option = wait.until(EC.element_to_be_clickable((By.XPATH,   
                '//li[@role="option" and contains(@class, "ant-select-dropdown-menu-item") and contains(text(), "资产侦查任务")]')))  
            asset_option.click()  
            print("成功选择了资产侦查任务")  
        except Exception as e:  
            print(f"精确选择资产侦查任务失败: {e}")  
           
        
        # 点击确定按钮 - 使用精确的选择器  
        print("点击确定按钮...")  
        time.sleep(1)  
        try:  
         
            confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH,   
                '//button[@type="button" and contains(@class, "ant-btn-primary")]/span[text()="确 定"]/..')))  
            confirm_button.click()  
            print("成功点击确定按钮")  
        except Exception as e:  
            print(f"精确定位确定按钮失败: {e}")  
        
        print(f"✅ 成功为 {university_name} ({domain}) 下发任务！")  
        
        # 等待一段时间，确保任务提交成功  
        time.sleep(4)  
        
except Exception as e:  
    print(f"❌ 执行过程出错: {e}")  
    
finally:  
    time.sleep(5)  
    driver.quit()  
    print("🏁 自动化操作完成")