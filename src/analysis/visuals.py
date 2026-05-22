import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon
from matplotlib.colors import ListedColormap

plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    #'text.usetex': True,
    'pgf.rcfonts': False,   # Fuente con serifa para coherencia con el texto
    "font.size": 11,          # Tamaño base
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "grid.alpha": 0.1         # Rejilla más sutil
})


def desplazar_canarias_provincias(gdf, dx=5.0, dy=7.5):
    """
    Desplaza las provincias de Canarias (35 y 38) para que quepan en el recuadro.
    """
    # Códigos INE de Las Palmas (35) y S.C. Tenerife (38)
    is_prov =  gdf.columns.str.contains('cod_prov').any()
    is_ccaa = gdf.columns.str.contains('cod_ccaa').any()
    if not (is_prov or is_ccaa):
        raise ValueError("El GeoDataFrame debe contener una columna 'cod_prov' o 'cod_ccaa' para identificar Canarias.")
    codes_prov_canarias = ['35', '38']
    codes_ccaa_canarias = ['4']
    id_col = 'cod_prov' if is_prov else 'cod_ccaa'
    codes_canarias = codes_prov_canarias if is_prov else codes_ccaa_canarias
    gdf_peninsula = gdf[~gdf[id_col].isin(codes_canarias)].copy()
    gdf_canarias = gdf[gdf[id_col].isin(codes_canarias)].copy()

    def translate_geom(geom, x_off, y_off):
        if geom.is_empty:
            return geom
        if isinstance(geom, Polygon):
            return Polygon([(x + x_off, y + y_off) for x, y in geom.exterior.coords])
        elif isinstance(geom, MultiPolygon):
            return MultiPolygon([translate_geom(p, x_off, y_off) for p in geom.geoms])
        return geom

    gdf_canarias['geometry'] = gdf_canarias['geometry'].apply(
        lambda x: translate_geom(x, dx, dy))
    return pd.concat([gdf_peninsula, gdf_canarias])


def generar_mapa(gdf_base, df_datos, col_id_df, col_valor, col_id_mapa='cod_prov', title=None, col_valor_label=None, save_file=None, width=14, custom_color_map=None):
    # 1. Preparación de IDs
    df_datos = df_datos.copy()
    df_datos[col_id_df] = df_datos[col_id_df].astype(str).str.zfill(2)
    gdf_base[col_id_mapa] = gdf_base[col_id_mapa].astype(str).str.zfill(2)

    # 2. Unión de datos
    mapa_final = gdf_base.merge(
        df_datos, left_on=col_id_mapa, right_on=col_id_df, how='left')

    # Convertimos a numérico por si acaso hay strings, para que la escala funcione
    mapa_final[col_valor] = pd.to_numeric(
        mapa_final[col_valor], errors='coerce')

    # 3. Desplazamiento de Canarias (usando tu función previa)
    mapa_final = desplazar_canarias_provincias(mapa_final)

    # 4. Configuración del gráfico
    fig, ax = plt.subplots(1, 1, figsize=(width, width * 0.618))  # Relación áurea para estética

    # Color para los nulos
    color_nulos = "#dcdde1"  # Un gris claro profesional

    cmap_personalizado = 'OrRd' if not custom_color_map else ListedColormap([custom_color_map[val] for val in sorted(mapa_final[col_valor].dropna().unique())])

    # Dibujar el mapa
    mapa_final.plot(
        column=col_valor,
        cmap=cmap_personalizado,
        linewidth=0.5,
        ax=ax,
        edgecolor='0.4',
        legend=True,
        # Configuración refinada de la barra de color
        legend_kwds={
            'label': f"{col_valor}" or col_valor_label,
            'orientation': "vertical",
            'shrink': 0.6,
            'pad': 0.02
        },
        missing_kwds={
            "color": color_nulos,
            "label": "Sin datos / Valor cero"
        }
    )

    # 5. AÑADIR CASO PARA DATOS NULOS EN LA LEYENDA
    # Como la colorbar no incluye el gris, creamos un parche manual
    patch_nulos = mpatches.Patch(
        color=color_nulos, label='Sin registros / Datos nulos')

    # Añadimos la leyenda del parche (se suele colocar en una esquina)
    ax.legend(handles=[patch_nulos], loc='lower right',
              frameon=True, fontsize=10)

    # Título y limpieza
    #title = title if title else f"Mapa de {col_valor}"
    ax.set_title(title) if title else None
    ax.axis('off')

    plt.tight_layout()

    if save_file:
        plt.savefig(save_file,
                    format='pdf',
                    bbox_inches='tight',
                    pad_inches=0.05)
    plt.show()
