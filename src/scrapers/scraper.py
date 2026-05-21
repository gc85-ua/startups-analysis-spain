import json
import logging
import pandas as pd
from copy import deepcopy
from typing import Any, List, Dict
from abc import ABC, abstractmethod
from src.shared.utils import random_delay
#from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import TimeoutException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)


class Scraper(ABC):
    """
    Abstract base class for web scrapers using undetected_chromedriver(Selenium).
    """

    def __init__(self, headless:bool=True, log_level=logging.INFO):
        """
        Initialize the Scraper with a Selenium WebDriver.
        
        :param self: self
        :param headless: Whether to run the browser in headless mode
        :type headless: bool
        :param log_level: Logging level for the scraper
        :type log_level: logging level, for example logging.INFO, logging.DEBUG, etc.
        """
        self._data: List[Dict] = []
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)
        self._skip_current_target: bool = False
        self._skip_reason: str = ""

        try:
            self._driver = uc.Chrome(headless=headless)
            self._wait = WebDriverWait(self._driver, 5)
        except Exception as e:
            self._logger.error(f"Error initializing WebDriver: {e}")
            raise

    def __enter__(self):
        """
        Context manager entry method.
        
        :param self: self
        :return: self
        :rtype: Scraper
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Context manager exit method.
        
        :param self: self
        :param exc_type: Exception type
        :param exc_value: Exception value
        :param traceback: Traceback object
        """
        if exc_type:
            self._logger.error(f"An error occurred: {exc_value}")
        self.close()

    def close(self):
        """
        Close the WebDriver instance.
        
        :param self: self
        """
        if hasattr(self, '_driver') and self._driver:
            self._driver.quit()

    def _append_data(self, item: Dict | List[Dict]) -> None:
        """
        Append a data item or a list of data items to the internal data storage.
        
        :param self: self
        :param item: Data item or list of data items to append
        :type item: Dict | List[Dict]
        """
        # Handle list input
        if isinstance(item, list):
            if not all(isinstance(elem, dict) for elem in item):
                self._logger.error("All items in the list must be dictionaries")
                raise ValueError("All items in the list must be dictionaries")
            self._data.extend(item)
            return

        # Validate non-list input
        if not isinstance(item, dict):
            self._logger.error("Data item must be a dictionary or a list of dictionaries")
            raise ValueError("Data item must be a dictionary or a list of dictionaries")

        # Ignore empty dicts with a warning
        if not item:
            self._logger.warning("Empty data item cannot be appended")
            return

        self._data.append(item)

    @abstractmethod
    def build_url(self, params:Dict[str,str]|None = None) -> str:
        """
        Build the URL for the scraper based on provided parameters.
        
        :param self: self
        :param params: Parameters for building the URL
        :type params: Dict[str, str] | None
        :return: Constructed URL
        :rtype: str
        """
        pass

    @abstractmethod
    def parse(self,**kwargs) -> Dict|List[Dict]:
        """
        Parse the content and extract data.
        
        :param self: self
        :return: Extracted data
        :rtype: Dict | List[Dict]
        """
        pass

    def wait_xpath_exists(self, xpath: str, timeout:float=5.0,expected:bool=True)->bool:
        """
        Wait until an element specified by the given XPath exists on the page.
        
        :param self: self
        :param xpath: XPath expression to locate the element
        :type xpath: str
        :param timeout: Timeout in seconds to wait for the element
        :return: exists flag
        :rtype: bool
        """
        exists = False
        try:
            self._wait.until(presence_of_element_located((By.XPATH, xpath)))
            exists = True
        except TimeoutException:
            if not expected:
                self._logger.debug(f"Element not found as expected in {self._driver.current_url} for xpath: {xpath} within {timeout} seconds")
            else:
                self._logger.warning(f"Element not found in {self._driver.current_url} for xpath: {xpath} within {timeout} seconds")
        except Exception as e:
            self._logger.error(f"Error while waiting for element in {self._driver.current_url} for xpath: {xpath}: {e}")
        finally:
            return exists
    
    def try_xpath(self, xpath: str):
        """
        Try to find an element using the given XPath.
        
        :param self: self
        :param xpath: XPath expression to locate the element
        :type xpath: str
        :return: The found element or None if not found
        """
        try:
            element = self._driver.find_element(By.XPATH, xpath)
            return element
        except Exception:
            self._logger.warning(f"Element not found in {self._driver.current_url} for xpath: {xpath}.")
            return None

    def navigate(self, target: Dict[str, str], **kwargs) -> None:
        """
        Navigate to the URL built from the target parameters.
        
        :param self: self
        :param target: Target parameters for building the URL
        :type target: Dict[str, str]
        :param kwargs: Additional keyword arguments
        """
        url = self.build_url(target)
        try:
            self._driver.get(url)
        except Exception as e:
            self._logger.error(f"Error navigating to {url}: {e}")
            raise
    def set_skip(self, reason:str) -> None:
        self._skip_current_target = True
        self._skip_reason = reason
        
    def check_skip(self) -> bool:
        """
        Check if the current target should be skipped.
        
        :param self: self
        :return: skip flag
        :rtype: bool
        """
        skip = deepcopy(self._skip_current_target)
        if skip:
            self._logger.info(f"Skipping current target. Reason: {self._skip_reason}")
            self._skip_reason = ""
        self._skip_current_target = False
        return skip
    
    def scrape(self, targets: List[Dict[str, str]], **kwargs)->None:
        """
        Template Method to scrape data for a list of targets.
        
        :param self: self
        :param targets: List of target parameters for scraping
        :type targets: List[Dict[str, str]]
        :param delay_interval: Interval range (min, max) in seconds to wait between scrapes
        :type delay_interval: tuple
        :param kwargs: Additional keyword arguments
        """
        delay_interval = kwargs.get("delay_interval", (1,2))

        for target in targets:
            try:
                self.navigate(target, **kwargs)
                if self.check_skip():
                    continue
                data = self.parse(**kwargs)
                self._append_data(data)
                self._logger.info(f"Scraped data: {data}")
                random_delay(*delay_interval)
            except Exception as e:
                self._logger.error(f"Error scraping target {target}: {e}")

    def get_data(self) -> List[Dict[str, Any]]:
        """
        Get a deep copy of the scraped data.
        
        :param self: Description
        :return: Description
        :rtype: List[Dict[str, Any]]
        """
        return deepcopy(self._data)

    def export_to_csv(self, filename="data.csv")->None:
        """
        Export the scraped data to a CSV file.
        
        :param self: self
        :param filename: Filename for the exported CSV file
        """
        try:
            df = pd.DataFrame(self._data)
            df.to_csv(filename, index=False)
        except Exception as e:
            self._logger.error(f"Error exporting to CSV: {e}")
            raise

    def export_to_json(self, filename="data.json")->None:
        """
        Export the scraped data to a JSON file.
        
        :param self: self
        :param filename: Filename for the exported JSON file
        """
        try:
            with open(filename, "w") as f:
                json.dump(self._data, f, indent=4)
        except Exception as e:
            self._logger.error(f"Error exporting to JSON: {e}")
            raise
