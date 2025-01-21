import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = ".outputs"
GEOJSON_URL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"  # noqa
COLUMN_NAME = "name"

DATA = {
    "Empresa": ["ÂNIMA", "COGNA", "YDUQS", "SER", "CRUZEIRO DO SUL", "VITRU"],
    "SUL": [5, 4, 3, 2, 4, 2],
    "SUDESTE": [14, 2, 9, 6, 7, 0],
    "CENTRO-OESTE": [2, 6, 0, 0, 1, 0],
    "NORTE": [0, 1, 5, 8, 0, 0],
    "NORDESTE": [8, 3, 10, 11, 1, 0],
}

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


def load_brazil_geojson(url):
    return gpd.read_file(url)


def map_regions(geo_df, column_name, region_mapping):
    geo_df[REGION_LABEL] = geo_df[column_name].map(region_mapping)
    return geo_df


def create_dataframe(data):
    return pd.DataFrame(data)


def generate_heatmap(geo_df, df, output_dir):
    for index, row in df.iterrows():
        if index == "Total":
            continue

        df_temp = pd.DataFrame(
            {
                REGION_LABEL: [
                    "SUL",
                    "SUDESTE",
                    "CENTRO-OESTE",
                    "NORTE",
                    "NORDESTE",
                ],
                "Valor": row[1:],
            }
        )

        geo_df_merged = geo_df.merge(df_temp, on=REGION_LABEL)

        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        geo_df_merged.plot(
            column="Valor",
            cmap="YlOrRd",
            legend=True,
            ax=ax,
            edgecolor="black",
        )

        plt.title(row[0])
        plt.axis("off")
        plt.savefig(f"{output_dir}/{row[0].lower()}.png", dpi=300)
        plt.close(fig)


def main():
    create_output_directory(OUTPUT_DIR)
    brasil_geojson = load_brazil_geojson(GEOJSON_URL)
    brasil_geojson = map_regions(brasil_geojson, COLUMN_NAME, REGION_MAPPING)
    df = create_dataframe(DATA)
    generate_heatmap(brasil_geojson, df, OUTPUT_DIR)


if __name__ == "__main__":
    main()
