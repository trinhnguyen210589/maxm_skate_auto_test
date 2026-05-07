"""
Pages package for MaxmAuto test framework.
Contains all Page Object classes following the Page Object Model (POM) pattern.
"""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.home_page import HomePage

__all__ = ['BasePage', 'LoginPage', 'HomePage']