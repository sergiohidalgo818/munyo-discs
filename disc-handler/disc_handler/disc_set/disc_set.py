import os
from typing import Union

from disc_handler.disc_set.disc_set_exceptions import (
    DiscSetFileNotFound,
    DiscSetRepeatedDisc,
    DiscSetNotSuchDisc,
)
import pandas as pd
from abc import abstractmethod


class DiscSet:
    csv_path: str

    def __init__(
        self,
        csv_path: Union[str, None] = None,
        first_col: Union[str, None] = None,
        second_col: Union[str, None] = None,
        **kwargs,
    ):
        self.csv_path = csv_path if csv_path is not None else kwargs.get("csv_path", "")
        if not os.path.exists(self.csv_path):
            raise DiscSetFileNotFound(f"File {self.csv_path} not found")

        self.first_col = (
            first_col if first_col is not None else kwargs.get("first_col", "artist")
        )
        self.second_col = (
            second_col if second_col is not None else kwargs.get("second_col", "disc")
        )

    @abstractmethod
    def frame_it(
        self,
    ) -> pd.DataFrame:
        """
        Returns a dataframe with the preference discs.

        Returns:
            pd.DataFrame: The dataframe with the preferences. The structure is stars, artist, disc.
        """
        pass

    def delete_collisions(self, other_csv_path: str, updated_path: str) -> None:
        """
        Writes a csv with no collisions.

        Args:
            other_csv_path (str): The path to the csv file.
            updated_path (str): The path to the updated csv file.
        """
        if not os.path.exists(other_csv_path) or not os.path.exists(self.csv_path):
            raise DiscSetFileNotFound(
                f"File {os.path.abspath(other_csv_path).split('/')[-1]} not found"
            )
        merged = pd.read_csv(self.csv_path, encoding="latin1").merge(
            pd.read_csv(other_csv_path, encoding="latin1")[["artist", "disc"]],
            on=["artist", "disc"],
            how="left",
            indicator=True,
        )

        clean_collisions = merged[merged["_merge"] == "left_only"].drop(
            columns=["_merge"]
        )  # type: ignore

        clean_collisions.to_csv(updated_path, encoding="latin1", index=False)

    def remove_disc(self, artist: str, disc: str) -> None:
        df = pd.read_csv(self.csv_path, encoding="latin1")
        if df[(df["artist"] == artist) & (df["disc"] == disc)].empty:
            raise DiscSetNotSuchDisc(f"Disc {artist} - {disc} not found")
        df = df[(df["artist"] != artist) | (df["disc"] != disc)]
        df.to_csv(self.csv_path, encoding="latin1", index=False)

    def modify_disc(
        self, artist: str, disc: str, new_artist: str, new_disc: str, stars: int = 0
    ) -> None:
        df = pd.read_csv(self.csv_path, encoding="latin1")

        if df[(df["artist"] == artist) & (df["disc"] == disc)].empty:
            self.add_disc(artist, disc, stars)

        else:
            df.loc[
                (df["artist"] == artist) & (df["disc"] == disc), ["artist", "disc"]
            ] = (
                new_artist,
                new_disc,
            )
        df.to_csv(self.csv_path, encoding="latin1", index=False)

    def add_disc(self, artist: str, disc: str, stars: int = 0) -> None:
        df = pd.read_csv(self.csv_path, encoding="latin1")
        if df[(df["artist"] == artist) & (df["disc"] == disc)].empty:
            new_row = pd.DataFrame([{"artist": artist, "disc": disc}])
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            raise DiscSetRepeatedDisc(f"Disc {artist} - {disc} already exists")
        df.to_csv(self.csv_path, encoding="latin1", index=False)

    def serialize(self) -> list[dict]:
        df = pd.read_csv(self.csv_path, encoding="latin1")
        df = df.where(pd.notnull(df), None).to_dict(orient="records")
        return df
