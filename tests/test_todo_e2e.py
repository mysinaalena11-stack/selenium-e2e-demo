from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import os

class TestTodoAppE2E:
    """Класс E2E тестов для To-Do приложения"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Фикстура для инициализации драйвера"""
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Фоновый режим
        chrome_options.add_argument("--no-sandbox")
        chrome_options.
add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.implicitly_wait(5)
        yield driver
        driver.quit()
    
    @pytest.fixture
    def app_url(self):
        """Фикстура для URL приложения"""
        # В GitHub Actions будет другой URL
        return "https://ваш-логин.github.io/selenium-e2e-demo/" if 'GITHUB_ACTIONS' in os.environ else "file://" + os.path.abspath("index.html")
    
    def test_add_new_task(self, driver, app_url):
        """Тест добавления новой задачи"""
        driver.get(app_url)
        
        # Вводим текст и добавляем задачу
        input_field = driver.find_element(By.ID, "taskInput")
        add_button = driver.find_element(By.ID, "addButton")
        
        input_field.send_keys("Купить продукты")
        add_button.click()
        
        # Проверяем, что задача добавилась
        tasks = driver.find_elements(By.CLASS_NAME, "task")
        assert len(tasks) == 1
        assert "Купить продукты" in tasks[0].text
    
    def test_complete_task(self, driver, app_url):
        """Тест отметки задачи как выполненной"""
        driver.get(app_url)
        
        # Добавляем задачу
        driver.find_element(By.ID, "taskInput").send_keys("Сделать ДЗ")
        driver.find_element(By.ID, "addButton").click()
        
        # Отмечаем как выполненную
        complete_btn = driver.find_element(By.XPATH, "//button[text()='✓']")
        complete_btn.click()
        
        # Проверяем стиль выполненной задачи
        task = driver.find_element(By.CLASS_NAME, "task")
        assert "completed" in task.get_attribute("class")
    
    def test_delete_task(self, driver, app_url):
        """Тест удаления задачи"""
        driver.get(app_url)
        
        # Добавляем задачу
        driver.find_element(By.ID, "taskInput").send_keys("Удаляемая задача")
        driver.find_element(By.ID, "addButton").click()
        
        # Удаляем задачу
        delete_btn = driver.find_element(By.XPATH, "//button[text()='✗']")
        delete_btn.click()
        
        # Проверяем, что список задач пуст
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "task"))
        )
        
        tasks = driver.find_elements(By.CLASS_NAME, "task")
        assert len(tasks) == 0
    
    def test_empty_task_validation(self, driver, app_url):
        """Тест: пустая задача не добавляется"""
        driver.get(app_url)
        
        initial_count = len(driver.find_elements(By.CLASS_NAME, "task"))
        driver.find_element(By.ID, "addButton").click()
        
        final_count = len(driver.find_elements(By.CLASS_NAME, "task"))
        assert final_count == initial_count, "Пустая задача не должна добавляться"
