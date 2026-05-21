import requests


def get_json_from_powerbi(query: dict) -> dict:
    """
    Executes a query against the Power BI API and returns the response as a JSON object.

    :param query: A dictionary containing the query to be executed. It should include the URL, headers, and payload.
    :type query: dict
    :return: The response from the Power BI API as a JSON object.
    :rtype: dict
    """
    response = requests.post(
        query["url"], json=query["payload"], headers=query["headers"])
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def enisa_certified_startups() -> dict:
    """
    Query to fetch certified startups (ENISA) data from the Power BI API. Payload and headers are copied from browser requests.

    :return: query parameters dict
    :rtype: dict
    """
    URL = "https://wabi-west-europe-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"
    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es-ES,es;q=0.5",
        "ActivityId": "481437de-1558-0034-b3d5-df3092c1feb6",
        "Connection": "keep-alive",
        "Content-Length": "2839",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "wabi-west-europe-b-primary-api.analysis.windows.net",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "RequestId": "ce90fe79-1caf-5756-d9b0-a2b4de1f17ab",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "X-PowerBI-ResourceKey": "595f7d83-5084-411b-be17-8ace6a33cd64",
        "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
    }
    PAYLOAD = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [
                                        {
                                            "Name": "l",
                                            "Entity": "liferay7 certificacion_datos_cliente",
                                            "Type": 0,
                                        },
                                        {
                                            "Name": "l1",
                                            "Entity": "liferay7 comunidad_autonoma",
                                            "Type": 0,
                                        },
                                        {
                                            "Name": "e1",
                                            "Entity": "enisa_vwcertificaciones",
                                            "Type": 0,
                                        },
                                        {
                                            "Name": "l2",
                                            "Entity": "liferay7 provincia",
                                            "Type": 0,
                                        },
                                        {
                                            "Name": "c",
                                            "Entity": "Certificacion Comites",
                                            "Type": 0,
                                        },
                                        {
                                            "Name": "e",
                                            "Entity": "enisa_comites (3)",
                                            "Type": 0,
                                        },
                                        {
                                            "Name": "l3",
                                            "Entity": "liferay7 estados_certificacion",
                                            "Type": 0,
                                        },
                                    ],
                                    "Select": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "l"}
                                                },
                                                "Property": "razon_social",
                                            },
                                            "Name": "liferay7 certificacion_datos_cliente.razon_social",
                                            "NativeReferenceName": "Razón Social",
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "l1"}
                                                },
                                                "Property": "DESCRIPCION",
                                            },
                                            "Name": "liferay7 comunidad_autonoma.DESCRIPCION",
                                            "NativeReferenceName": "C.C.A.A",
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "l"}
                                                },
                                                "Property": "cif",
                                            },
                                            "Name": "liferay7 certificacion_datos_cliente.cif",
                                            "NativeReferenceName": "NIF",
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "l2"}
                                                },
                                                "Property": "Provincia",
                                            },
                                            "Name": "liferay7 provincia.Provincia",
                                            "NativeReferenceName": "Provincia",
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e1"}
                                                },
                                                "Property": "Fecha Estimada de Descertificación",
                                            },
                                            "Name": "enisa_vwcertificaciones.Fecha Estimada de Descertificación",
                                            "NativeReferenceName": "Fecha Estimada de Descertificación",
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "c"}
                                                },
                                                "Property": "FechaComité",
                                            },
                                            "Name": "Certificacion Comites.FechaComité",
                                            "NativeReferenceName": "Fecha de Certificación1",
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {"Source": "e1"}
                                                },
                                                "Property": "Fecha de efecto de pérdida de certificación",
                                            },
                                            "Name": "enisa_vwcertificaciones.Fecha de efecto de pérdida de certificación",
                                            "NativeReferenceName": "Fecha de efecto de pérdida de certificación",
                                        },
                                    ],
                                    "Where": [
                                        {
                                            "Condition": {
                                                "Comparison": {
                                                    "ComparisonKind": 2,
                                                    "Left": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "e"
                                                                }
                                                            },
                                                            "Property": "Fecha Comite",
                                                        }
                                                    },
                                                    "Right": {
                                                        "Literal": {
                                                            "Value": "datetime'2023-05-03T00:00:00'"
                                                        }
                                                    },
                                                }
                                            }
                                        },
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "l3"
                                                                    }
                                                                },
                                                                "Property": "idEstado",
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [{"Literal": {"Value": "8L"}}],
                                                        [{"Literal": {"Value": "9L"}}],
                                                        [{"Literal": {"Value": "10L"}}],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "400L"
                                                                }
                                                            }
                                                        ],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "410L"
                                                                }
                                                            }
                                                        ],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "420L"
                                                                }
                                                            }
                                                        ],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "430L"
                                                                }
                                                            }
                                                        ],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "440L"
                                                                }
                                                            }
                                                        ],
                                                    ],
                                                }
                                            }
                                        },
                                    ],
                                },
                                "Binding": {
                                    "Primary": {
                                        "Groupings": [
                                            {"Projections": [
                                                0, 1, 2, 3, 4, 5, 6]}
                                        ]
                                    },
                                    "DataReduction": {
                                        "DataVolume": 3,
                                        "Primary": {"Window": {"Count": 3000}},
                                    },
                                    "Version": 1,
                                },
                                "ExecutionMetricsKind": 1,
                            }
                        }
                    ]
                },
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "e7873e50-0d0b-41de-b99a-d517ff6f8e34",
                    "Sources": [
                        {
                            "ReportId": "2294bb50-820f-4a8e-9f0d-58428746ce59",
                            "VisualId": "b19c0cc61075c6a6510a",
                        }
                    ],
                },
            }
        ],
        "cancelQueries": [],
        "modelId": 4045844,
    }

    return {
        "url": URL,
        "headers": HEADERS,
        "payload": PAYLOAD
    }


def recidi_science_and_technology_parks() -> dict:
    """
    Query to fetch science and technology parks (RECIDI) data from the Power BI API. Payload and headers are copied from browser requests.

    :return: query parameters dict
    :rtype: dict
    """
    URL = "https://wabi-west-europe-e-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"
    HEADERS = {

        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es-ES,es;q=0.5",
        "ActivityId": "bdb455a9-b2c1-4444-ae5e-72acaf360eb4",
        "Connection": "keep-alive",
        "Content-Length": "2854",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "wabi-west-europe-e-primary-api.analysis.windows.net",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "RequestId": "0fd14f89-5729-3f97-127b-a42bbf87e355",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "X-PowerBI-ResourceKey": "40dd20f7-4361-40d7-a026-8e21d7d90875",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Brave\";v=\"144\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\""
    }
    PAYLOAD = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [
                                        {
                                            "Name": "h",
                                            "Entity": "RECIDI",
                                            "Type": 0
                                        }
                                    ],
                                    "Select": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "ACRONIMO"
                                            },
                                            "Name": "Hoja1.ACRONIMO",
                                            "NativeReferenceName": "ACRONIMO"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "Nombre"
                                            },
                                            "Name": "Hoja1.Nombre_Entidad_Mostrar",
                                            "NativeReferenceName": "Nombre_Entidad_Mostrar"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "PROVINCIA"
                                            },
                                            "Name": "Hoja1.PROVINCIA",
                                            "NativeReferenceName": "PROVINCIA1"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "ENLACE WEB"
                                            },
                                            "Name": "Hoja1.ENLACE WEB",
                                            "NativeReferenceName": "ENLACE WEB"
                                        }
                                    ],
                                    "Where": [
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "h"
                                                                    }
                                                                },
                                                                "Property": "Categoria web"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Parque científico y/o tecnológico'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        }
                                    ],
                                    "OrderBy": [
                                        {
                                            "Direction": 1,
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "h"
                                                        }
                                                    },
                                                    "Property": "ACRONIMO"
                                                }
                                            }
                                        }
                                    ]
                                },
                                "Binding": {
                                    "Primary": {
                                        "Groupings": [
                                            {
                                                "Projections": [
                                                    0,
                                                    1,
                                                    2,
                                                    3
                                                ]
                                            }
                                        ]
                                    },
                                    "DataReduction": {
                                        "DataVolume": 3,
                                        "Primary": {
                                            "Window": {
                                                "Count": 500
                                            }
                                        }
                                    },
                                    "Version": 1
                                },
                                "ExecutionMetricsKind": 1
                            }
                        }
                    ]
                },
                "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"h\",\"Entity\":\"RECIDI\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"ACRONIMO\"},\"Name\":\"Hoja1.ACRONIMO\",\"NativeReferenceName\":\"ACRONIMO\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"Nombre\"},\"Name\":\"Hoja1.Nombre_Entidad_Mostrar\",\"NativeReferenceName\":\"Nombre_Entidad_Mostrar\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"PROVINCIA\"},\"Name\":\"Hoja1.PROVINCIA\",\"NativeReferenceName\":\"PROVINCIA1\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"ENLACE WEB\"},\"Name\":\"Hoja1.ENLACE WEB\",\"NativeReferenceName\":\"ENLACE WEB\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"Categoria web\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Parque científico y/o tecnológico'\"}}]]}}}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"ACRONIMO\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "9d6cdf08-e074-4454-8ca5-544846fcda74",
                    "Sources": [
                        {
                            "ReportId": "a7a0f6af-78fd-4c15-b913-1f874596bfc3",
                            "VisualId": "715caa9607c89e868bab"
                        }
                    ]
                }
            }
        ],
        "cancelQueries": [],
        "modelId": 5201471
    }
    response = requests.post(URL, json=PAYLOAD, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def recidi_somma_severo_ochoa() -> dict:
    """
    Query to fetch data about Severo Ochoa centers of excellence (RECIDI) from the Power BI API. Payload and headers are copied from browser requests.

    :return: query parameters dict
    :rtype: dict
    """
    URL = "https://wabi-west-europe-e-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"
    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es-ES,es;q=0.5",
        "ActivityId": "8d96f578-9c4b-40d6-ba6f-c50d1bedf415",
        "Connection": "keep-alive",
        "Content-Length": "3490",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "wabi-west-europe-e-primary-api.analysis.windows.net",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "RequestId": "d4145d1e-d8f5-30bc-4435-97118036f220",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "X-PowerBI-ResourceKey": "40dd20f7-4361-40d7-a026-8e21d7d90875",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Brave\";v=\"144\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\""
    }
    PAYLOAD = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [
                                        {
                                            "Name": "h",
                                            "Entity": "RECIDI",
                                            "Type": 0
                                        }
                                    ],
                                    "Select": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "ACRONIMO"
                                            },
                                            "Name": "Hoja1.ACRONIMO",
                                            "NativeReferenceName": "ACRONIMO"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "ENLACE WEB"
                                            },
                                            "Name": "Hoja1.ENLACE WEB",
                                            "NativeReferenceName": "ENLACE WEB1"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "PROVINCIA"
                                            },
                                            "Name": "Hoja1.PROVINCIA",
                                            "NativeReferenceName": "PROVINCIA1"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "SECTOR"
                                            },
                                            "Name": "Hoja1.SECTOR",
                                            "NativeReferenceName": "Área científica"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "Nombre"
                                            },
                                            "Name": "Hoja1.Nombre_Entidad_Mostrar",
                                            "NativeReferenceName": "Nombre_Entidad_Mostrar"
                                        }
                                    ],
                                    "Where": [
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "h"
                                                                    }
                                                                },
                                                                "Property": "SOMMA"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Severo Ochoa'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        },
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "h"
                                                                    }
                                                                },
                                                                "Property": "Categoria web"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Centro Excelencia SOMMA'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        }
                                    ],
                                    "OrderBy": [
                                        {
                                            "Direction": 2,
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "h"
                                                        }
                                                    },
                                                    "Property": "SECTOR"
                                                }
                                            }
                                        }
                                    ]
                                },
                                "Binding": {
                                    "Primary": {
                                        "Groupings": [
                                            {
                                                "Projections": [
                                                    0,
                                                    1,
                                                    2,
                                                    3,
                                                    4
                                                ]
                                            }
                                        ]
                                    },
                                    "DataReduction": {
                                        "DataVolume": 3,
                                        "Primary": {
                                            "Window": {
                                                "Count": 500
                                            }
                                        }
                                    },
                                    "Version": 1
                                },
                                "ExecutionMetricsKind": 1
                            }
                        }
                    ]
                },
                "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"h\",\"Entity\":\"RECIDI\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"ACRONIMO\"},\"Name\":\"Hoja1.ACRONIMO\",\"NativeReferenceName\":\"ACRONIMO\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"ENLACE WEB\"},\"Name\":\"Hoja1.ENLACE WEB\",\"NativeReferenceName\":\"ENLACE WEB1\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"PROVINCIA\"},\"Name\":\"Hoja1.PROVINCIA\",\"NativeReferenceName\":\"PROVINCIA1\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"SECTOR\"},\"Name\":\"Hoja1.SECTOR\",\"NativeReferenceName\":\"Área científica\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"Nombre\"},\"Name\":\"Hoja1.Nombre_Entidad_Mostrar\",\"NativeReferenceName\":\"Nombre_Entidad_Mostrar\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"SOMMA\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Severo Ochoa'\"}}]]}}},{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"Categoria web\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Centro Excelencia SOMMA'\"}}]]}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"SECTOR\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "9d6cdf08-e074-4454-8ca5-544846fcda74",
                    "Sources": [
                        {
                            "ReportId": "a7a0f6af-78fd-4c15-b913-1f874596bfc3",
                            "VisualId": "edefaa90061db0a77ab5"
                        }
                    ]
                }
            }
        ],
        "cancelQueries": [],
        "modelId": 5201471
    }

    return {
        "url": URL,
        "headers": HEADERS,
        "payload": PAYLOAD
    }


def recidi_somma_maria_maeztu() -> dict:
    """
    Query to fetch data about María de Maeztu centers of excellence (RECIDI) from the Power BI API. Payload and headers are copied from browser requests.

    :return: query parameters dict
    :rtype: dict
    """
    URL = "https://wabi-west-europe-e-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"
    HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-ES,es;q=0.5',
        'ActivityId': '8d96f578-9c4b-40d6-ba6f-c50d1bedf415',
        'Connection': 'keep-alive',
        'Content-Length': '3246',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'wabi-west-europe-e-primary-api.analysis.windows.net',
        'Origin': 'https://app.powerbi.com',
        'Referer': 'https://app.powerbi.com/',
        'RequestId': 'e307ce00-ff0e-b9f8-25f6-8920b1248a28',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'X-PowerBI-ResourceKey': '40dd20f7-4361-40d7-a026-8e21d7d90875',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Brave";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    PAYLOAD = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [
                                        {
                                            "Name": "h",
                                            "Entity": "RECIDI",
                                            "Type": 0
                                        }
                                    ],
                                    "Select": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "ACRONIMO"
                                            },
                                            "Name": "Hoja1.ACRONIMO",
                                            "NativeReferenceName": "ACRONIMO"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "ENLACE WEB"
                                            },
                                            "Name": "Hoja1.ENLACE WEB",
                                            "NativeReferenceName": "ENLACE WEB1"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "PROVINCIA"
                                            },
                                            "Name": "Hoja1.PROVINCIA",
                                            "NativeReferenceName": "PROVINCIA1"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "SECTOR"
                                            },
                                            "Name": "Hoja1.SECTOR",
                                            "NativeReferenceName": "Área científica"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "h"
                                                    }
                                                },
                                                "Property": "Nombre"
                                            },
                                            "Name": "Hoja1.Nombre_Entidad_Mostrar",
                                            "NativeReferenceName": "Nombre_Entidad_Mostrar"
                                        }
                                    ],
                                    "Where": [
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "h"
                                                                    }
                                                                },
                                                                "Property": "SOMMA"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'María de Maeztu'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        },
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "h"
                                                                    }
                                                                },
                                                                "Property": "Categoria web"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Centro Excelencia SOMMA'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        }
                                    ]
                                },
                                "Binding": {
                                    "Primary": {
                                        "Groupings": [
                                            {
                                                "Projections": [
                                                    0,
                                                    1,
                                                    2,
                                                    3,
                                                    4
                                                ]
                                            }
                                        ]
                                    },
                                    "DataReduction": {
                                        "DataVolume": 3,
                                        "Primary": {
                                            "Window": {
                                                "Count": 500
                                            }
                                        }
                                    },
                                    "Version": 1
                                },
                                "ExecutionMetricsKind": 1
                            }
                        }
                    ]
                },
                "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"h\",\"Entity\":\"RECIDI\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"ACRONIMO\"},\"Name\":\"Hoja1.ACRONIMO\",\"NativeReferenceName\":\"ACRONIMO\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"ENLACE WEB\"},\"Name\":\"Hoja1.ENLACE WEB\",\"NativeReferenceName\":\"ENLACE WEB1\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"PROVINCIA\"},\"Name\":\"Hoja1.PROVINCIA\",\"NativeReferenceName\":\"PROVINCIA1\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"SECTOR\"},\"Name\":\"Hoja1.SECTOR\",\"NativeReferenceName\":\"Área científica\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"Nombre\"},\"Name\":\"Hoja1.Nombre_Entidad_Mostrar\",\"NativeReferenceName\":\"Nombre_Entidad_Mostrar\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"SOMMA\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'María de Maeztu'\"}}]]}}},{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"h\"}},\"Property\":\"Categoria web\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Centro Excelencia SOMMA'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":1}}]}",
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "9d6cdf08-e074-4454-8ca5-544846fcda74",
                    "Sources": [
                        {
                            "ReportId": "a7a0f6af-78fd-4c15-b913-1f874596bfc3",
                            "VisualId": "13620a609c3b22815e75"
                        }
                    ]
                }
            }
        ],
        "cancelQueries": [],
        "modelId": 5201471
    }

    return {
        "url": URL,
        "headers": HEADERS,
        "payload": PAYLOAD
    }


def recidi_entities_from_region(cod_ccaa: str) -> dict:
    URL = 'https://wabi-west-europe-e-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true'
    HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'es-ES,es;q=0.5',
        'ActivityId': '49060ad3-a96b-4e9d-a91b-daff9230aca0',
        'Connection': 'keep-alive',
        'Content-Length': '1725',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'wabi-west-europe-e-primary-api.analysis.windows.net',
        'Origin': 'https://app.powerbi.com',
        'Referer': 'https://app.powerbi.com/',
        'RequestId': '95bed488-7df1-9f72-f9ca-2fd05cf42c8a',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'X-PowerBI-ResourceKey': '40dd20f7-4361-40d7-a026-8e21d7d90875',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Brave";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    PAYLOAD = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [
                                        {
                                            "Name": "r",
                                            "Entity": "RECIDI",
                                            "Type": 0
                                        }
                                    ],
                                    "Select": [
                                        {
                                            "Aggregation": {
                                                "Expression": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "r"
                                                            }
                                                        },
                                                        "Property": "ACRONIMO"
                                                    }
                                                },
                                                "Function": 3
                                            },
                                            "Name": "Min(RECIDI.ACRONIMO)",
                                            "NativeReferenceName": "Primera fecha: ACRONIMO"
                                        },
                                        {
                                            "Aggregation": {
                                                "Expression": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "r"
                                                            }
                                                        },
                                                        "Property": "Nombre"
                                                    }
                                                },
                                                "Function": 3
                                            },
                                            "Name": "Min(RECIDI.Nombre_Entidad_Mostrar)",
                                            "NativeReferenceName": "Primera fecha: Nombre_Entidad_Mostrar"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "r"
                                                    }
                                                },
                                                "Property": "UbicacionMAPA"
                                            },
                                            "Name": "RECIDI.UbicacionMAPA",
                                            "NativeReferenceName": "UbicacionMAPA"
                                        },
                                        {
                                            "Aggregation": {
                                                "Expression": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "r"
                                                            }
                                                        },
                                                        "Property": "ID_ENTIDAD"
                                                    }
                                                },
                                                "Function": 5
                                            },
                                            "Name": "CountNonNull(RECIDI.ID_ENTIDAD)",
                                            "NativeReferenceName": "Recuento de ID_ENTIDAD"
                                        },
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "r"
                                                    }
                                                },
                                                "Property": "Categoria web"
                                            },
                                            "Name": "RECIDI.Categoria web",
                                            "NativeReferenceName": "Categoria web"
                                        }
                                    ],
                                    "Where": [
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "r"
                                                                    }
                                                                },
                                                                "Property": "COD_CCAA"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": f"'{cod_ccaa}'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        }
                                    ],
                                    "OrderBy": [
                                        {
                                            "Direction": 2,
                                            "Expression": {
                                                "Aggregation": {
                                                    "Expression": {
                                                        "Column": {
                                                            "Expression": {
                                                                "SourceRef": {
                                                                    "Source": "r"
                                                                }
                                                            },
                                                            "Property": "ID_ENTIDAD"
                                                        }
                                                    },
                                                    "Function": 5
                                                }
                                            }
                                        }
                                    ]
                                },
                                "Binding": {
                                    "Primary": {
                                        "Groupings": [
                                            {
                                                "Projections": [
                                                    0,
                                                    1,
                                                    2,
                                                    3
                                                ]
                                            }
                                        ]
                                    },
                                    "Secondary": {
                                        "Groupings": [
                                            {
                                                "Projections": [
                                                    4
                                                ]
                                            }
                                        ]
                                    },
                                    "DataReduction": {
                                        "DataVolume": 4,
                                        "Primary": {
                                            "Top": {}
                                        },
                                        "Secondary": {
                                            "Top": {}
                                        }
                                    },
                                    "SuppressedJoinPredicates": [
                                        0,
                                        1
                                    ],
                                    "Version": 1
                                }
                            }
                        }
                    ]
                },
                "QueryId": ""
            }
        ],
        "cancelQueries": [],
        "modelId": 5201471
    }

    return {
        "url": URL,
        "headers": HEADERS,
        "payload": PAYLOAD
    }