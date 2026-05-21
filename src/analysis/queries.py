import duckdb


def query(query_str):
    return duckdb.query(query_str).to_df()


TOP_PROVINCES_BY_GRADUATES = """
    SELECT 
        cpro,
        ambito_de_estudio,
        SUM(egresados) AS total_egresados,
        SUM(egresados_hombres) AS total_egresados_hombres,
        SUM(egresados_mujeres) AS total_egresados_mujeres
    FROM {df} 
    WHERE 
        anno = 2024 
        AND codigo_universidad != '000' 
        AND ambito_de_estudio != 'Total' 
        AND grupo_de_edad = 'Total'
    GROUP BY 
        cpro,
        ambito_de_estudio
    QUALIFY ROW_NUMBER() OVER (PARTITION BY ambito_de_estudio ORDER BY SUM(egresados) DESC) = 1
    ORDER BY 
        cpro ASC;
"""


def get_top_provinces_by_graduates(df):
    return query(TOP_PROVINCES_BY_GRADUATES.format(df=df))


PIVOT_STUDY_FIELD = """
    PIVOT (
        -- 1. Select the base data you want to work with
        SELECT 
            cpro,
            ambito_de_estudio,
            egresados
        FROM {df} 
        WHERE anno BETWEEN {start_year} AND {end_year}
          AND codigo_universidad != '000' 
          AND ambito_de_estudio != 'Total' 
          AND grupo_de_edad = 'Total'
    ) 
    -- 2. Define the column that will become the new headers
    ON ambito_de_estudio 

    -- 3. Define the aggregation to fill the new cells
    USING SUM(egresados)

    -- 4. Define the rows that will group the data
    GROUP BY 
        cpro
    ORDER BY 
        cpro DESC;
"""


def get_pivot_study_field(df, start_year=2021, end_year=2024):
    return query(
            PIVOT_STUDY_FIELD.format(df=df, start_year=start_year, end_year=end_year)
        ).merge(
            query(
                """
                    SELECT 
                        cpro,
                        SUM(egresados) as total
                    FROM {df}
                    WHERE anno BETWEEN {start_year} AND {end_year}
                        AND codigo_universidad != '000' 
                        AND ambito_de_estudio == 'Total' 
                        AND grupo_de_edad = 'Total'
                    group by cpro
                    ORDER BY cpro
                """.format(df=df, start_year=start_year, end_year=end_year)
            ), on='cpro', how='left'
        ).fillna(0, inplace=True)
