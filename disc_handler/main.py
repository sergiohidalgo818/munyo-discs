import os
import pandas as pd
from history.history import History


def main():
    data_path: str = "data"
    preferences_csv: str = "discos-munyo-preference.csv"
    obtained_csv: str = "discos-munyo-obtained.csv"
    updated_csv: str = "discos-munyo-updated.csv"
    preferences_path: str = os.path.join(data_path, preferences_csv)
    obtained_path: str = os.path.join(data_path, obtained_csv)
    updated_path: str = os.path.join(data_path, updated_csv)

    preferences_df: pd.DataFrame = History(preferences_path).from_csv_to_preference()
    obtained_df: pd.DataFrame = History(obtained_path).from_csv_to_obtained()

    merged = preferences_df.merge(
        obtained_df[["artist", "disc"]],
        on=["artist", "disc"],
        how="left",
        indicator=True,
    )
    preferences_df = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])  # type: ignore

    preferences_df.to_csv(updated_path, encoding="latin1", index=False)


if __name__ == "__main__":
    main()
