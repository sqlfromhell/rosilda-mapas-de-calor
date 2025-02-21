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


def create_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_geojson(url):
    return gpd.read_file(url)


def map_regions(
    geo_df,
    column_name,
    region_mapping,
):
    geo_df[REGION_LABEL] = geo_df[column_name].map(
        region_mapping,
    )
    return geo_df


def plot_heatmap(
    geo_df,
    output_dir,
):
    base_df = pd.DataFrame(DATA)

    for index, row in base_df.iterrows():
        if index == "Total":
            continue

        data = row[1:]
        data = [int(x) for x in data]

        df = pd.DataFrame(
            {
                REGION_LABEL: REGIONS,
                "Valor": data,
            }
        )

        geo_df_merged = geo_df.merge(
            df,
            on=REGION_LABEL,
        )

        _, ax = plt.subplots(
            1,
            1,
            figsize=(10, 8),
        )

        geo_df_merged.plot(
            column="Valor",
            cmap="YlOrRd",
            legend=False,
            ax=ax,
            edgecolor="black",
        )

        # Create custom legend
        unique_values = sorted(set(df["Valor"]))
        for value in unique_values:
            color = plt.cm.YlOrRd(value / max(unique_values))
            ax.scatter(
                [],
                [],
                c=[color],
                label=f"{value}",
            )

        ax.legend()

        plt.title(row[0])
        plt.axis("off")
        plt.savefig(
            f"{output_dir}/{row[0].lower()}.png",
            dpi=900,
        )


def main():
    create_output_directory(OUTPUT_DIR)
    geojson = load_geojson(GEOJSON_URL)
    geojson = map_regions(
        geojson,
        COLUMN_NAME,
        REGION_MAPPING,
    )
    plot_heatmap(
        geojson,
        OUTPUT_DIR,
    )


if __name__ == "__main__":
    main()
