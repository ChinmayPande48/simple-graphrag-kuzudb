import kagglehub
from kagglehub import KaggleDatasetAdapter

def load_imdb_data(file_path="imdb_top_1000.csv"):
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows",
        file_path,
    )
    
    return df