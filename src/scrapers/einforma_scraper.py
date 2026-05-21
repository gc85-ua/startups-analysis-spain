from typing import Dict, override
from selenium.webdriver.common.by import By
from src.scrapers.scraper import Scraper
from src.shared.utils import save_as_json

class EinformaScraper(Scraper):
    _current_nif = None

    @override
    def build_url(self, params: Dict[str, str] | None = None) -> str:
        url = "https://www.einforma.com/servlet/app/prod/ETIQUETA_EMPRESA/nif/{nif}"
        nif = params.get("nif", "") if params else None
        self._current_nif = nif
        return url.format(nif=nif)

    def extract_text_by_xpath(self, xpath) -> str | None:
        try:
            element = self.try_xpath(xpath)
            return (
                element.text.replace("Ver Mapa", "").strip()
                if element is not None
                else None
            )
        except Exception as e:
            self._logger.error(
                f"Error extracting data with XPath {xpath}: {e}")
        return None

    @override
    def parse(self, **kwargs) -> dict:

        export_artifact = kwargs.get("export_artifact", False)
        artifact_path = kwargs.get("artifact_path", "../data/cache/einforma/")


        xpath_denominacion = "//td[strong[contains(text(), 'Denominación:')]]/following-sibling::td[1]"
        xpath_domicilio_social = "//td[strong[contains(text(), 'Domicilio social actual:')]]/following-sibling::td[1]"
        xpath_localidad = "//td[strong[contains(text(), 'Localidad:')]]/following-sibling::td[1]"
        xpath_cnae_2009 = "//td[strong[contains(text(), 'CNAE 2009:')]]/following-sibling::td[1]"
        xpath_cnae_2025 = "//td[strong[contains(text(), 'CNAE 2025:')]]/following-sibling::td[1]"
        xpath_cnae_2009_2025 = "//td[strong[contains(text(), 'CNAE 2009 - 2025:')]]/following-sibling::td[1]"
        xpath_forma_juridica = "//td[strong[contains(text(), 'Forma Jurídica:')]]/following-sibling::td[1]"
        xpath_objeto_social = "//td[strong[contains(text(), 'Objeto Social:')]]/following-sibling::td[1]"

        artifact = {
            "nif": self._current_nif,
            "denominacion": self.extract_text_by_xpath(
                xpath_denominacion
            ),
            "domicilio_social": self.extract_text_by_xpath(
                xpath_domicilio_social
            ),
            "localidad": self.extract_text_by_xpath(
                xpath_localidad
            ),
            "cnae_2009": self.extract_text_by_xpath(
                xpath_cnae_2009
            ),
            "cnae_2025": self.extract_text_by_xpath(
                xpath_cnae_2025
            ),
            "cnae_2009-2025": self.extract_text_by_xpath(
                xpath_cnae_2009_2025
            ),
            "forma_juridica": self.extract_text_by_xpath(
                xpath_forma_juridica
            ),
            "objeto_social": self.extract_text_by_xpath(
                xpath_objeto_social
            )
        }

        if export_artifact:
            nif = artifact.get("nif", "unknown_cif")
            filename = f"{nif}.json"
            save_as_json(artifact, filename, artifact_path)

        return artifact

class EinformaAlternativeScraper(EinformaScraper):
    @override
    def build_url(self, params: Dict[str, str] | None = None) -> str:
        url = "https://www.einforma.com/rapp/resultados-busqueda?searchTerm={nif}&type=EMPRESAS"
        nif = params.get("nif", "") if params else None
        if not nif:
            raise ValueError("NIF parameter is required to build the URL.")
        self._current_nif = nif
        return url.format(nif=nif)
    @override
    def extract_text_by_xpath(self, xpath):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            return (
                " ".join(elements[0].text.split("\n")[1:])
                if len(elements) > 0
                else None
            )
        except Exception as e:
            self._logger.error(f"Error extrayendo datos con XPath {xpath}: {e}")
        return None
    
    @override
    def parse(self, **kwargs):

        export_artifact = kwargs.get("export_artifact", False)
        artifact_path = kwargs.get("artifact_path", "../data/cache/einforma/")

        xpath_denominacion = "//strong[contains(text(), 'Denominación')]/.."
        xpath_denominacion_antigua = "//strong[contains(text(), 'Denominación Antigua')]/.."
        xpath_web = "//strong[contains(text(), 'PÁGINA WEB')]/.."
        xpath_domicilio_social = "//strong[contains(text(), 'Domicilio Social')]/.."
        xpath_cnae_2009 = "//strong[contains(text(), 'Actividad CNAE 2009')]/.."
        xpath_cnae_2025 = "//strong[contains(text(), 'Actividad CNAE 2025')]/.."
        xpath_forma_juridica = "//strong[contains(text(), 'Forma Jurídica')]/.."
        xpath_fecha_constitucion = "//strong[contains(text(), 'Fecha de constitución')]/.."
        xpath_objeto_social = "//strong[contains(text(), 'Objeto Social')]/.."

        artifact = {
            "nif": self._current_nif,
            "denominacion": self.extract_text_by_xpath(xpath_denominacion),
            "denominacion_antigua": self.extract_text_by_xpath(
                xpath_denominacion_antigua
            ),
            "web": self.extract_text_by_xpath(xpath_web),
            "domicilio_social": self.extract_text_by_xpath(xpath_domicilio_social),
            "cnae_2009": self.extract_text_by_xpath(xpath_cnae_2009),
            "cnae_2025": self.extract_text_by_xpath(xpath_cnae_2025),
            "forma_juridica": self.extract_text_by_xpath(xpath_forma_juridica),
            "fecha_constitucion": self.extract_text_by_xpath(
                xpath_fecha_constitucion
            ),
            "objeto_social": self.extract_text_by_xpath(xpath_objeto_social),
        }

        if export_artifact:
            nif = artifact.get("nif", "unknown_cif")
            filename = f"{nif}.json"
            save_as_json(artifact, filename, artifact_path)
        
        return artifact

def get_data_from_nif(nif:str)->dict:
    einforma_scraper = EinformaScraper(headless=False)
    einforma_scraper.navigate({"nif": nif})
    data = einforma_scraper.parse(export_artifact=False)
    einforma_scraper.close()
    return data