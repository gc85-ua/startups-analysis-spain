from typing import Dict, override
from src.shared.utils import random_delay
from src.shared.utils import save_as_json
from src.scrapers.scraper import Scraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
class AxesorScraper(Scraper):
    _current_nif: str = None
    @override
    def build_url(self, params:Dict[str,str]|None = None) -> str:
        return "https://www.axesor.es/"
    @override
    def navigate(self, target:Dict[str,str], **kwargs):
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.get(self.build_url())
        nif = target.get("nif", None)
        self._current_nif = nif
        if not nif:
            self._logger.error("NIF parameter is required in target")
            self.set_skip("NIF parameter is missing.")
            return
        xpath_input = '//*[@id="buscador-campo-nombre"]'
        xpath_submit = '//*[@id="buscador-submit"]'
        input = self._driver.find_element(By.XPATH, xpath_input)
        ActionChains(self._driver).move_to_element(input).click().perform()
        random_delay(*kwargs.get("delay_interval", (1,2)))
        for char in nif:
            input.send_keys(char)
            random_delay(0.2, 0.8)
        random_delay(*kwargs.get("delay_interval", (1,2)))
        submit = self._driver.find_element(By.XPATH, xpath_submit)
        ActionChains(self._driver).move_to_element(submit).click().perform()

        xpath_0_resultados = '//*[@id="tabEmpresas"]/div/div/p[contains(text(), "0")]'
        
        if self.wait_xpath_exists(xpath_0_resultados, expected=False):
            self.set_skip("No results found for the given query.")
        
        xpath_varios_resultados = '//*[@id="tablaEmpresas"]'
        if self.wait_xpath_exists(xpath_varios_resultados, expected=False):
            self._logger.warning(f"Multiple results found for NIF {nif}.")
            xpath_resultado = f'//span[contains(normalize-space(.), "{nif}")]/following-sibling::a'
            if self.wait_xpath_exists(xpath_resultado, timeout=5):
                resultado = self._driver.find_element(By.XPATH, xpath_resultado)
                ActionChains(self._driver).move_to_element(resultado).click().perform()

                random_delay(*kwargs.get("delay_interval", (1,2)))
            else:
                self.set_skip("Multiple results found, specific result not found.")

        return
    
    def parse(self, **kwargs) -> dict:
        export_artifact = kwargs.get("export_artifact", False)
        artifact_path = kwargs.get("artifact_path", "../data/cache/axesor/")
        timeout_xpath = kwargs.get("timeout_xpath", 5)
        
        
        xpath_datos_basicos = '//*[@id="c-section__menu1"]/div[2]/div/div[1]/div[1]/table'
        xpath_datos_contacto = '//*[@id="c-section__menu1"]/div[2]/div/div[1]/div[2]/table'
        xpath_datos_actividad = '//*[@id="c-section__menu1"]/div[2]/div/div[2]/div/table'
        
        xpath_nombre = '//th[contains(text(), "Nombre")]/following-sibling::td'
        xpath_cif = '//th[contains(text(), "CIF")]/following-sibling::td'
        xpath_forma_juridica = '//th[contains(text(), "Forma jurídica")]/following-sibling::td'
        xpath_fecha_constitucion = '//th[contains(text(), "Fecha de constitución")]/following-sibling::td'
        xpath_direccion = '//th[contains(text(), "Dirección")]/following-sibling::td'
        xpath_objeto_social = '//th[contains(text(), "Objeto social")]/following-sibling::td'
        xpath_cnae = '//th[contains(text(), "CNAE")]/following-sibling::td'
        #xpath_sic = '//th[contains(text(), "SIC")]/following-sibling::td'
        artifact = {}
        nombre = None
        cif = None
        forma_juridica = None
        fecha_constitucion = None
        direccion = None
        objeto_social = None
        cnae = None
        #sic = None
        try:
            
            if self.wait_xpath_exists(xpath_datos_basicos, timeout=timeout_xpath):
                nombre = self.try_xpath(xpath_nombre)
                cif = self.try_xpath(xpath_cif)
                forma_juridica = self.try_xpath(xpath_forma_juridica)
                fecha_constitucion = self.try_xpath(xpath_fecha_constitucion)
            if self.wait_xpath_exists(xpath_datos_contacto, timeout=timeout_xpath):
                direccion = self.try_xpath(xpath_direccion)
            if self.wait_xpath_exists(xpath_datos_actividad, timeout=timeout_xpath):
                objeto_social = self.try_xpath(xpath_objeto_social)
                cnae = self.try_xpath(xpath_cnae)
                #sic = self.try_xpath(xpath_sic)
            artifact = {
                "denominacion": nombre.text if nombre else None,
                "nif": cif.text if cif else None,
                "forma_juridica": forma_juridica.text if forma_juridica else None,
                "fecha_constitucion": fecha_constitucion.text if fecha_constitucion else None,
                "domicilio_social": direccion.text if direccion else None,
                "objeto_social": objeto_social.text if objeto_social else None,
                "cnae": cnae.text if cnae else None,
                #"sic": sic.text if sic else ""
            }
            if export_artifact:
                nif = artifact.get("nif", "unknown_nif")
                filename = f"{nif}.json"
                save_as_json(artifact, filename, artifact_path)
            if self._current_nif != artifact.get("nif", None):
                self._logger.warning(f"NIF mismatch: searched for {self._current_nif} but got {artifact.get('nif', None)}")

        except Exception as e:
            self._logger.error(f"Error during scraping: {e}")
        finally:
            return artifact