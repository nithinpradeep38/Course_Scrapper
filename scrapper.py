import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
from bs4 import BeautifulSoup
from logger import scrapLogger

class Scrapper:

    def __init__(self, driver_path):
        try:
            self.driver_path= driver_path
            self.logger= scrapLogger.ineuron_logger()

        except Exception as e:
            raise e

    def get_courselink(self,url= "https://courses.ineuron.ai/"):

        def findkeys(node, kv):
            if isinstance(node, list):
                for i in node:
                    for x in findkeys(i, kv):
                        yield x
            elif isinstance(node, dict):
                if kv in node:
                    yield node[kv]
                for j in node.values():
                    for x in findkeys(j, kv):
                        yield x

        try:

            uClient = uReq(url)
            CoursePage = uClient.read()
            data = bs(CoursePage, "html.parser")
            for i in data("script")[14]:
                temp = json.loads(i)
                course_list = list(findkeys(temp, 'courses'))[0].keys()
                course_url = []
                course_url = ["https://courses.ineuron.ai/" + i.replace(" ", "-") for i in course_list]
                self.logger.info("Course links obtained")
            return course_url
        except Exception as e:
            self.logger.exception("Exception occuered while obtaining course links", e)
            raise e


    def get_courseinfo(self, courselinks):
        try:
            allcourse_info= []
            options = webdriver.ChromeOptions()
            options.add_argument("headless")  # headless driver option
            driver = webdriver.Chrome(executable_path=self.driver_path,
                                  options=options)
            for link in courselinks:

                driver.get(link)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                loadtime = 10
                wait = WebDriverWait(driver, loadtime)
                xPath = '//*[@id="__next"]/footer'
                wait.until(ec.visibility_of_element_located((By.XPATH, xPath)))

                try:
                    view_more = wd.find_element(By.CLASS_NAME, "CurriculumAndProjects_view-more-btn__3ggZL")
                    view_more.click()
                except:
                    pass

                try:
                    features = driver.find_elements(by=By.CLASS_NAME, value="CoursePrice_course-features__2qcJp")[0].text
                    features = features.split("\n")
                except:
                    features= "Not found"

                try:
                    description= driver.find_elements_by_class_name("Hero_course-desc__26_LL")[0].text
                except:
                    description= "Not found"

                try:
                    response = requests.get(link)
                    t = response.text
                    soup = BeautifulSoup(driver.page_source, features="html.parser")
                    course_learning = soup.find_all('div', {'class': 'CourseLearning_card__WxYAo card'})
                    learning = []
                    for i in range(len(course_learning[0].find_all("li"))):
                        learning.append(course_learning[0].find_all("li")[i].text)
                except:
                    learning= "Not found"


                try:
                    course_requirements = soup.find_all('div', {'class': 'CourseRequirement_card__3g7zR requirements card'})
                    requirements = []
                    for i in range(len(course_requirements[0].find_all("li"))):
                        requirements.append(course_requirements[0].find_all("li")[i].text)
                except:
                    requirements= "Not found"

                try:
                    course_curriculum_data_tags = soup.find_all('div', {
                        'class': "CurriculumAndProjects_curriculum-accordion__2pppc CurriculumAndProjects_card__7HqQx card"})

                    curriculum = []
                    for i in range(len(course_curriculum_data_tags)):
                        curriculum.append(course_curriculum_data_tags[i].span.text)
                except:
                    curriculum= "Not found"
                    self.logger.info(f"{link} has been parsed successfully")

                course_info= {'link': link, 'features': features, 'description': description, 'learning': learning, 'curriculum': curriculum}
                allcourse_info.append(course_info)
            driver.close()
            return allcourse_info
        except Exception as e:
            self.logger.error("Error in extracting course info: ", e)
            raise e