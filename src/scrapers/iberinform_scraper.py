from src.scrapers.scraper import Scraper
from typing import Dict, override
from src.shared.utils import save_as_json, random_delay
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class IberinformScraper(Scraper):
    
    @override
    def build_url(self, params:Dict[str,str]|None = None) -> str:
        url = "https://www.iberinform.es/Iberinform2019/busquedaEmpresa/cuerpo/0?criterioBusqueda={nif}&pagina=1"
        nif = params.get("nif", None) if params else None
        return url.format(nif=nif)
    
    @override
    def navigate(self, target:Dict[str,str], **kwargs):
        delay_interval = kwargs.get("delay_interval", (1,2))
        timeout_xpath = kwargs.get("timeout_xpath", 5)
        
        nif = target.get("nif", None)
        if not nif:
            self._logger.error("NIF parameter is required in target")
            self.set_skip("NIF parameter is missing.")
            return
        
        self._current_nif = nif
        self._driver.get(self.build_url(target))
        xpath_first_anchor = '//*[@id="resultsSearchIber"]/div/div/div/table/tbody/tr/td[1]/a'
        
        if not self.wait_xpath_exists(xpath_first_anchor, timeout=timeout_xpath):
            self.set_skip("No results found for the given query.")
            return
        
        first_anchor = self._driver.find_element(By.XPATH, xpath_first_anchor)
        random_delay(*delay_interval)
        ActionChains(self._driver).move_to_element(first_anchor).click().perform()
        return
    
    def extract_text_by_xpath(self, xpath) -> str | None:
        try:
            if self.wait_xpath_exists(xpath, timeout=5):
                element = self.try_xpath(xpath)
                return (
                    element.text.strip()
                    if element is not None
                    else None
                )
            else:
                return None
        except Exception as e:
            self._logger.error(
                f"Error extracting data with XPath {xpath}: {e}")
        return None

    @override
    def parse(self, **kwargs) -> dict:

        export_artifact = kwargs.get("export_artifact", False)
        artifact_path = kwargs.get("artifact_path", "../data/cache/iberinform/")

        xpath_estado = '//*[@id="content"]/section[2]/div/div/div[3]/span'

        xpath_contenedor_empresa = '//*[@id="detalleEmpresa"]'
        xpath_denominacion = '//h3[contains(normalize-space(text()),"Denominación")]/following-sibling::div[@class="info"]/p'
        xpath_marcas_nombres_comerciales = '//h3[contains(normalize-space(text()),"Marcas y nombres comerciales")]/following-sibling::div[@class="info"]/p'
        xpath_nif = '//h3[contains(normalize-space(text()),"CIF/NIF de")]/following-sibling::div[@class="info"]'
        xpath_forma_juridica = '//h3[contains(normalize-space(text()),"Forma jurídica")]/following-sibling::div[@class="info"]/p'
        xpath_direccion = '//h3[contains(normalize-space(text()),"Dirección de")]/following-sibling::div[@class="info"]/a'
        xpath_codigo_postal = '//h3[contains(normalize-space(text()),"Código postal")]/following-sibling::div[@class="info"]/p'
        xpath_municipio = '//h3[contains(normalize-space(text()),"Municipio")]/following-sibling::div[@class="info"]/p'
        xpath_provincia = '//h3[contains(normalize-space(text()),"Provincia")]/following-sibling::div[@class="info"]/p'
        xpath_web = '//h3[contains(normalize-space(text()),"web")]/following-sibling::div[@class="info"]/span'
        xpath_cnae = '//h3[contains(normalize-space(text()),"CNAE")]/following-sibling::div[@class="info"]/p'
        xpath_objeto_social = '//h3[contains(normalize-space(text()),"Objeto social de")]/following-sibling::div[@class="info"]/p'
        xpath_sector_empresa = '//h3[contains(normalize-space(text()),"Sector de la empresa")]/following-sibling::div[@class="info"]/p'
        xpath_fecha_constitucion = '//h3[contains(normalize-space(text()),"Fecha de constitución")]/following-sibling::div[@class="info"]/p'

        xpath_contenedor_facturacion = '//*[@id="content"]/section[3]/div/div/div[2]/div[1]'
        xpath_tramo_facturacion = '//h3[contains(normalize-space(text()),"Tramo de facturación")]/following-sibling::p'
        xpath_tramo_capital_social = '//h3[contains(normalize-space(text()),"Tramo de capital social")]/following-sibling::p'
        xpath_evolucion_ventas = '//h3[contains(normalize-space(text()),"Evolución ventas")]/following-sibling::p'
        xpath_tamanno_empresa = '//h3[contains(normalize-space(text()),"Tamaño de empresa")]/following-sibling::p'
        xpath_empleados = '//h3[contains(normalize-space(text()),"Empleados")]/following-sibling::p'

        artifact = {}
        if self.wait_xpath_exists(xpath_contenedor_empresa, timeout=5):
            artifact.update({
                "nif": self.extract_text_by_xpath(xpath_nif),
                "estado": self.extract_text_by_xpath(xpath_estado),
                "denominacion": self.extract_text_by_xpath(xpath_denominacion),
                "marcas_nombres_comerciales": self.extract_text_by_xpath(xpath_marcas_nombres_comerciales),
                "forma_juridica": self.extract_text_by_xpath(xpath_forma_juridica),
                "direccion": self.extract_text_by_xpath(xpath_direccion),
                "codigo_postal": self.extract_text_by_xpath(xpath_codigo_postal),
                "municipio": self.extract_text_by_xpath(xpath_municipio),
                "provincia": self.extract_text_by_xpath(xpath_provincia),
                "web": self.extract_text_by_xpath(xpath_web),
                "cnae": self.extract_text_by_xpath(xpath_cnae),
                "objeto_social": self.extract_text_by_xpath(xpath_objeto_social),
                "sector_empresa": self.extract_text_by_xpath(xpath_sector_empresa),
                "fecha_constitucion": self.extract_text_by_xpath(xpath_fecha_constitucion)
            })
        if self.wait_xpath_exists(xpath_contenedor_facturacion, timeout=5):
            artifact.update({
                "tramo_facturacion": self.extract_text_by_xpath(xpath_tramo_facturacion),
                "tramo_capital_social": self.extract_text_by_xpath(xpath_tramo_capital_social),
                "evolucion_ventas": self.extract_text_by_xpath(xpath_evolucion_ventas),
                "tamaño_empresa": self.extract_text_by_xpath(xpath_tamanno_empresa),
                "empleados": self.extract_text_by_xpath(xpath_empleados)
            })

        if export_artifact:
            nif = artifact.get("nif", "unknown_nif")
            filename = f"{nif}.json"
            save_as_json(artifact, filename, artifact_path)
        
        return artifact