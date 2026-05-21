import requests
import urllib3

# Ocultar la advertencia de InsecureRequestWarning debido a verify=False (el equivalente a -k en curl)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def search_by_term(term, JSESSIONID,persistencia,TS01dc4fc6, OClmoOot,LFR_SESSION_STATE_20103,TS56819fee027, TS01afd22c,captchaId,length=10):
    cookies = {
        'JSESSIONID': JSESSIONID,
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'es_ES',
        'persistencia': persistencia,
        'TS01dc4fc6': TS01dc4fc6,
        'OClmoOot': OClmoOot,
        'LFR_SESSION_STATE_20103': LFR_SESSION_STATE_20103,
        'TS56819fee027': TS56819fee027,
        'TS01afd22c': TS01afd22c,
    }
    
    headers = {
        'Host': 'opendata.registradores.org',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Sec-Ch-Ua': '"Not-A.Brand";v="24", "Chromium";v="146"',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://opendata.registradores.org',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://opendata.registradores.org/directorio/-/sociedad',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=1, i',
        # 'Content-Length': '1001' # Omitido intencionalmente: requests lo calcula automáticamente.
    }
    
    data = (
        'draw=1&columns%5B0%5D%5Bdata%5D=denominacion.denominacion&columns%5B0%5D%5Bname%5D='
        '&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false'
        '&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false'
        '&columns%5B1%5D%5Bdata%5D=domicilioSocial.provincia&columns%5B1%5D%5Bname%5D='
        '&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false'
        '&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false'
        f'&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false'
        f'&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_captchaId={captchaId}'
        f'&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_term={term}'
        '&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_provincia='
        '&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_localidad='
        '&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_cnae='
        '&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_print_datatable=true'
    )
    
    url = (
        'https://opendata.registradores.org/directorio'
        '?p_p_id=org_registradores_opendata_portlet_BuscadorSociedadesPortlet'
        '&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=%2Fopendata%2Fsociedades'
        '&p_p_cacheability=cacheLevelPage'
        '&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_priv_r_p_mvcRenderCommandName=%2Fsociedades'
        '&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_priv_r_p_term='
        f'&_org_registradores_opendata_portlet_BuscadorSociedadesPortlet_priv_r_p_captchaId={captchaId}'
    )
    
    # verify=False equivale a -k / --insecure en cURL
    return requests.post(url, cookies=cookies, headers=headers, data=data, verify=False)
