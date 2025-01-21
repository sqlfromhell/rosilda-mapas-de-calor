import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = ".outputs"
GEOJSON_URL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"  # noqa
COLUMN_NAME = "name"

REGIONS = [
    "SUL",
    "SUDESTE",
    "CENTRO-OESTE",
    "NORTE",
    "NORDESTE",
]

VALUES = [
    20,
    38,
    9,
    14,
    33,
]

REGION_MAPPING = {
    "Paraná": "SUL",
    "Santa Catarina": "SUL",
    "Rio Grande do Sul": "SUL",
    "São Paulo": "SUDESTE",
    "Rio de Janeiro": "SUDESTE",
    "Espírito Santo": "SUDESTE",
    "Minas Gerais": "SUDESTE",
    "Goiás": "CENTRO-OESTE",
    "Mato Grosso": "CENTRO-OESTE",
    "Mato Grosso do Sul": "CENTRO-OESTE",
    "Acre": "NORTE",
    "Amazonas": "NORTE",
    "Roraima": "NORTE",
    "Amapá": "NORTE",
    "Rondônia": "NORTE",
    "Pará": "NORTE",
    "Tocantins": "NORTE",
    "Bahia": "NORDESTE",
    "Sergipe": "NORDESTE",
    "Alagoas": "NORDESTE",
    "Pernambuco": "NORDESTE",
    "Paraíba": "NORDESTE",
    "Rio Grande do Norte": "NORDESTE",
    "Ceará": "NORDESTE",
    "Piauí": "NORDESTE",
    "Maranhão": "NORDESTE",
}

REGION_LABEL = "Região"


def create_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_geojson(url):
    return gpd.read_file(url)


def create_dataframe(regions, values):
    return pd.DataFrame({REGION_LABEL: regions, "Valor": values})


def map_regions(geo_df, column_name, mapping):
    if column_name not in geo_df.columns:
        raise ValueError(
            f"Column '{column_name}' not found in the GeoDataFrame!",
        )
    geo_df[REGION_LABEL] = geo_df[column_name].map(mapping)
    return geo_df


def merge_data(geo_df, df):
    return geo_df.merge(df, on=REGION_LABEL)


def plot_heatmap(geo_df, output_path):
    _, ax = plt.subplots(1, 1, figsize=(10, 8))
    geo_df.plot(
        column="Valor",
        cmap="YlOrRd",
        legend=True,
        ax=ax,
        edgecolor="black",
    )
    plt.title("BRASIL")
    plt.axis("off")
    plt.savefig(output_path, dpi=300)


def main():
    create_output_directory(OUTPUT_DIR)
    brasil = load_geojson(GEOJSON_URL)
    df = create_dataframe(REGIONS, VALUES)
    brasil = map_regions(brasil, COLUMN_NAME, REGION_MAPPING)
    brasil = merge_data(brasil, df)
    plot_heatmap(brasil, os.path.join(OUTPUT_DIR, "geral.png"))


if __name__ == "__main__":
    main()
