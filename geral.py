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

REGION_LABEL = "Região"

DATA = [
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


def create_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_geojson(url):
    return gpd.read_file(url)


def map_regions(geo_df, column_name, mapping):
    geo_df[REGION_LABEL] = geo_df[column_name].map(mapping)
    return geo_df


def plot_heatmap(geo_df, output_path):
    df = pd.DataFrame(
        {
            REGION_LABEL: REGIONS,
            "Valor": DATA,
        }
    )

    geo_df_merged = geo_df.merge(df, on=REGION_LABEL)

    _, ax = plt.subplots(1, 1, figsize=(10, 8))
    geo_df_merged.plot(
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
    output_file = os.path.join(OUTPUT_DIR, "geral.png")
    geojson = load_geojson(GEOJSON_URL)
    geojson = map_regions(geojson, COLUMN_NAME, REGION_MAPPING)

    plot_heatmap(geojson, output_file)


if __name__ == "__main__":
    main()
