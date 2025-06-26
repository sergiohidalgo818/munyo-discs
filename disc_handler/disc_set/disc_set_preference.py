import os
from typing import Union
from disc_set.disc_set import DiscSet
from disc_set.disc_set_exceptions import DiscSetFileNotFound
import pandas as pd


class DiscSetPreference(DiscSet):
    csv_path: str
    first_col: str
    second_col: str
    third_col: str

    def __init__(
        self,
        csv_path: Union[str, None] = None,
        first_col: Union[str, None] = None,
        second_col: Union[str, None] = None,
        third_col: Union[str, None] = None,
        **kwargs,
    ):
        self.csv_path = csv_path if csv_path is not None else kwargs.get("csv_path", "")
        if not os.path.exists(self.csv_path):
            raise DiscSetFileNotFound(f"File {self.csv_path} not found")

        self.first_col = (
            first_col if first_col is not None else kwargs.get("first_col", "stars")
        )
        self.second_col = (
            second_col if second_col is not None else kwargs.get("second_col", "artist")
        )
        self.third_col = (
            third_col if third_col is not None else kwargs.get("third_col", "disc")
        )


def frame_it(self) -> pd.DataFrame:
    """
    Returns a dataframe with the preference discs.

    Returns:
        pd.DataFrame: The dataframe with the preferences. The structure is stars, artist, disc.
    """
    df = pd.read_csv(self.csv_path, encoding="latin1")

    df.rename(
        columns={
            df.columns[0]: self.first_col,  # type: ignore
            df.columns[1]: self.second_col,  # type: ignore
        },
        inplace=True,
    )

    last_star: Union[int, None] = None
    discs: list[str] = []

    for _, row in df.iterrows():
        if str(row[self.first_col]) != "nan":
            if "(en blanco)" == str(row[self.first_col]):
                row[self.first_col] = -1
            last_star = row[self.first_col]  # type: ignore
        else:
            row[self.first_col] = last_star

    for _, row in df.iterrows():
        if row[self.first_col] is not None:
            if not str(self.row[self.first_col]).isnumeric():
                row[self.first_col] = -1
                last_star = row[self.first_col]  # type: ignore

        else:
            row[self.second_col] = last_star

        if row[self.second_col] is not None and str(row[self.second_col]) != "nan":
            discs.append(row[self.second_col].split("-")[1].strip())  # type: ignore

            row[self.second_col] = row[self.second_col].split("-")[0].strip()  # type: ignore

    df.dropna(inplace=True)

    df[self.third_col] = discs

    return df
