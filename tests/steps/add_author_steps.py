from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By  # Importing By for an alternative solution if needed
import time

# driver = webdriver.Chrome('/Users/m_azizi/Desktop/masterschool/learning_sqlalchamy/chromedriver')
use_step_matcher("re")


@given("I am on the homepage")
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get("http://localhost:5000/")


@when("I choose to add a new author")
def step_impl(context):
    author_link = context.driver.find_element(By.XPATH, "//a[text()='Add an Author']")
    author_link.click()


@when("I fill out the author details")
def step_impl(context):
    input_name = context.driver.find_element(By.XPATH, "//input[@id='name']")
    birthdate_field = context.driver.find_element(By.XPATH, "//input[@id='birthdate']")
    death = context.driver.find_element(By.XPATH, "//input[@id='date_of_death']")
    submit_button = context.driver.find_element(By.XPATH, "//form[@action='/add_author']//button[@type='submit']")
    # print(death)
    input_name.send_keys("Shubham Singh")
    time.sleep(5)
    birthdate_field.clear()
    birthdate_field.send_keys("01-01-1987")
    time.sleep(5)
    death.clear()
    death.send_keys("01-01-2050")
    time.sleep(5)
    submit_button.click()
    time.sleep(5)


@when("go back to homepage")
def step_impl(context):
    home_link = context.driver.find_element(By.XPATH, "//a[text()='Home']")
    home_link.click()
    time.sleep(5)


@then("the new author should be added")
def step_impl(context):
    # Add assertion logic here, like checking the URL or a success message.
    context.driver.quit()

