from typing import Union
from disc_handler.disc_set.disc_set import DiscSet
import pandas as pd


class DiscSetOwned(DiscSet):
    csv_path: str
    first_col: str
    second_col: str

    def frame_it(self) -> pd.DataFrame:
        """
        Returns a dataframe with the obtained discs.

        Args:
            self.csv_path (str): The path to the csv file.

        Returns:
            pd.DataFrame: The dataframe with the preferences. The structure is artist, disc.
        """

        df = pd.read_csv(self.csv_path, encoding="latin1")

        if len(df.columns) > 1:
            return df

        df = pd.read_csv(
            self.csv_path, encoding="latin1", header=None, names=[self.first_col]
        )

        discs: list[Union[str, None]] = []
        for i, row in df.iterrows():
            if "-" in row[self.first_col]:
                parts = row[self.first_col].split("-")  # type: ignore
                df.at[i, self.first_col] = parts[0].strip()
                discs.append(parts[1].strip())
            else:
                discs.append(None)

        df[self.second_col] = discs
        df.dropna(inplace=True)

        return df
