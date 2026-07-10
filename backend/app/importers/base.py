from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

import pandas as pd


T = TypeVar("T")


class CSVAdapter(ABC, Generic[T]):
    """Base class for converting source-specific CSV files into normalized models."""

    required_columns: set[str] = set()

    def read_csv(self, file_path: str | Path) -> pd.DataFrame:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")

        dataframe = pd.read_csv(path)
        self.validate_columns(dataframe)

        return dataframe

    def validate_columns(self, dataframe: pd.DataFrame) -> None:
        missing_columns = self.required_columns - set(dataframe.columns)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required CSV columns: {missing}")

    @abstractmethod
    def transform_row(self, row: pd.Series) -> T:
        """Convert one source row into a normalized model."""
        raise NotImplementedError

    def import_file(self, file_path: str | Path) -> list[T]:
        dataframe = self.read_csv(file_path)

        return [
            self.transform_row(row)
            for _, row in dataframe.iterrows()
        ]