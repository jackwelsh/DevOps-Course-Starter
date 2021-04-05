import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import pytest
import os
from todo_app import create_app
from threading import Thread
import config
import time
from dotenv import load_dotenv, find_dotenv


# Adding options to the firefox driver
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1400,2100")

# need to add a wait here for the elements to load in the dashboard as tests are failing otherwise!
@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox(options=options) as driver:
        yield driver


class BoardMaker:
    def __init__(self, config):
        self.url_prefix = "https://api.trello.com/1/"
        self.config = config.Config()
        self.query = {
            'key': self.config.TRELLO_KEY,
            'token': self.config.TRELLO_TOKEN
        }

    def create_board(self):
        """
        Creates a trello board for system testing
        Returns:
            String of newly created board_id
        """
        url = self.url_prefix+"boards/"
        query = self.query
        query["name"] = "temp_system_test_board"
        response = requests.post(url, params=query)
        response.raise_for_status()
        board_id = response.json()["id"].split("/")[-1].strip()
        return board_id

    def delete_board(self, board_id):
        """
        Deletes a Trello board created during system testing
        """
        url = self.url_prefix+"boards/"+board_id
        query = self.query
        query["id"] = board_id
        response = requests.delete(url, params=query)
        response.raise_for_status()


@pytest.fixture
def test_app():

    # Load testing variables from .env.test
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    boardMaker = BoardMaker(config)
    board_id = boardMaker.create_board()
    os.environ['TRELLO_BOARD'] = board_id
    
    # Create the test app
    test_app = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: test_app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield test_app

    # Use the app to create a test_client that can be used in our tests.
    thread.join(1)
    boardMaker.delete_board(board_id)


def test_task_journey(driver, test_app):
    driver.get('http://127.0.0.1:5000/')
    time.sleep(2)
    assert driver.title == 'To-Do App'

    card = {
        'todo': {
            'card name': '/html/body/div/div/div[3]/div[1]/div/div/h5',
            'card date': '/html/body/div/div/div[3]/div[1]/div/div/p[2]',
            'card desc': '/html/body/div/div/div[3]/div[1]/div[1]/div/p[1]',
            'card link': '/html/body/div/div/div[3]/div[1]/div[1]/div/a'
        },
        'done': {
            'card name': '/html/body/div/div/div[3]/div[3]/div/div/h5',
            'card date': '/html/body/div/div/div[3]/div[3]/div/div/p[2]',
            'card desc': '/html/body/div/div/div[3]/div[3]/div[1]/div/p[1]',
            'card link': '/html/body/div/div/div[3]/div[3]/div[1]/div/a'
        },
        'doing': {
            'card name': '/html/body/div/div/div[3]/div[2]/div/div/h5',
            'card date': '/html/body/div/div/div[3]/div[2]/div/div/p[2]',
            'card desc': '/html/body/div/div/div[3]/div[2]/div[1]/div/p[1]',
            'card link': '/html/body/div/div/div[3]/div[2]/div[1]/div/a'
        }
    }

    entries = {
        'task name': '/html/body/div/div/div[1]/div/form/div[1]/input',
        'description input': '/html/body/div/div/div[1]/div/form/div[2]/textarea',
        'date input': '/html/body/div/div/div[1]/div/form/div[3]/input',
        'new task button': '/html/body/div/div/div[1]/div/form/div[4]/button'
    }

    link = {
        'submit': '/html/body/div/div/div/div/form/div[5]/button[1]',
        'delete': '/html/body/div/div/div/div/form/div[5]/button[2]'
    }

    status = {
        'TODO': '//*[@id="radio1"]',
        'DOING': '//*[@id="radio2"]',
        'DONE': '//*[@id="radio3"]'
    }

    driver.find_element_by_xpath(
        entries['task name']).send_keys('Test Task Name')
    driver.find_element_by_xpath(
        entries['description input']).send_keys('Test Description')
    driver.find_element_by_xpath(
        entries['new task button']).click()

    cardTitle = driver.find_element_by_xpath(
        card['todo']['card name']).text
    cardDesc = driver.find_element_by_xpath(
        card['todo']['card desc']).text

    assert cardTitle == 'Test Task Name'
    assert cardDesc == 'Test Description'

    driver.find_element_by_xpath(
        card['todo']['card link']).click()
    driver.find_element_by_xpath(
        status['DONE']).click()
    driver.find_element_by_xpath(
        link['submit']).click()

    cardTitle = driver.find_element_by_xpath(
        card['done']['card name']).text
    cardDesc = driver.find_element_by_xpath(
        card['done']['card desc']).text

    assert cardTitle == 'Test Task Name'
    assert cardDesc == 'Test Description'

    driver.find_element_by_xpath(
        card['done']['card link']).click()
    driver.find_element_by_xpath(
        status['DOING']).click()
    driver.find_element_by_xpath(
        link['submit']).click()

    cardTitle = driver.find_element_by_xpath(
        card['doing']['card name']).text
    cardDesc = driver.find_element_by_xpath(
        card['doing']['card desc']).text

    assert cardTitle == 'Test Task Name'
    assert cardDesc == 'Test Description'

    driver.find_element_by_xpath(
        card['doing']['card link']).click()
    driver.find_element_by_xpath(
        link['delete']).click()
