from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


def test_show_all_pets(driver):
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"


def test_all_pets_are_exist(driver): # Присутствуют все питомцы
    WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))).click()
    count_pets = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]') # Общее количество питомцев
    pets = driver.find_element(By.XPATH, '//tbody') # Питомца на доске
    count_pet = count_pets.text.split()
    pet = pets.text.split('×')
    assert (len(pet)-1) == int(count_pet[2])




def test_pets_have_name_species_age(driver): # У всех питомцев есть имя, возраст и порода
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    driver.implicitly_wait(5)
    all_pets = driver.find_element(By.XPATH, '//tbody')
    info_of_all_pets = all_pets.text.split('\n')
    x = [] # кнопка удаления питомца (×)
    info_list = []
    names = []
    species = []
    age = []
    for i in info_of_all_pets:
        if i != '×':
            info_list.append(i)
        else:
            x.append(i)
    info_list = [j.split() for j in info_list]
    for i in info_list:
        names.append(i[0])
        species.append(i[1])
        age.append(i[2])

    for i in names:
        assert i != '' and i != int # проверяем, что строка "имя" не пустая
    for i in species:
        assert i != '' and i != int # проверяем, что строка "порода" не пустая
    for i in age:
        assert i != '' # проверяем, что строка "возраст" не пустая

    """В случае, если количество имен, пород, возрастов меньше кнопок удаления питомца - у питомца отсутствует имя, порода или возраст"""
    assert len(names) < len(x)
    assert len(species) < len(x)
    assert len(age) < len(x)


def test_pets_images(driver): # Хотя бы у половины питомцев есть фото
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    count_pets = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    count_pet = count_pets.text.split() # Количество питомцев
    count = 1 # Счетчик тегов tr
    images = []
    for i in range(int(count_pet[2])):
        all_my_pets = driver.find_elements(By.XPATH, f'//*[@id="all_my_pets"]/table[1]/tbody/tr[{count}]/th/img')
        count += 1
        for i in range(len(all_my_pets)):
            if all_my_pets[i].get_attribute('src') != '':
                images.append(all_my_pets[i].get_attribute('src'))

    assert len(images) >= round(int(count_pet[2])/2)


def test_same_names(driver): # Проверка на одинаковые иммена
    WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Мои питомцы")]'))).click()
    pets = driver.find_element(By.XPATH, '//tbody')
    pets_list = pets.text.split('\n')
    list_info_of_pets = [i for i in pets_list if i != '×']
    list_of_list_info_of_pets = [i.split() for i in list_info_of_pets]
    names = [] # Список всех имен
    uniq_names = [] # Список уникальных имен
    same_names = [] # Список совпадающих имен
    for i in list_of_list_info_of_pets:
        names.append(i[0]) # Создаем список всех имен
    for i in names:
        if i not in uniq_names:
            uniq_names.append(i) # Создаем список уникальных имен
        else:
            same_names.append(i) # Создем список совпадающих имен, шобы было

    assert len(names) != len(uniq_names) # Проверяем, равно ли количество всех имен списку уникальных имен, если не равно - есть одинаковые имена