import pandas as pd
from pathlib import Path


class CSVExporter:

    @staticmethod
    def export(dataframe):

        output = Path("output")

        output.mkdir(exist_ok=True)

        caminho = output / "curriculos_extraidos.csv"

        dataframe.to_csv(
            caminho,
            index=False,
            encoding="utf-8-sig"
        )

        return caminho