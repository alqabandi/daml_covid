import requests
import pathlib
from datetime import datetime
from data_collection.config import US_STATES

def download_series_as_json(series_suffix: str, state: str, staging_path: str, api_key: str):
    """
    Download a series for a state and save the json
    """

    series_name = state + series_suffix
    download_path = staging_path + "/" + series_name + ".json"
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_name}&file_type=json&api_key={api_key}"
    response = requests.get(url)
    with open(download_path, "bw") as f:
        f.write(response.content)


if __name__ == "__main__":
    download_date = datetime.now().strftime("%Y%m%d")
    staging_path = "data/staging/" + download_date

    pathlib.Path(staging_path).mkdir(parents=True, exist_ok=True)

    for state in US_STATES:
        print(f"Downloading data for state {state}")
        download_series_as_json(
            state=state,
            series_suffix="ICLAIMS",
            api_key="195c7d6137f182e2db230b4202ba4cd7",
            staging_path=staging_path,
        )



def download_covid_tracking_json(series_suffix: str, staging_path: str):
    """
    Download a series for a state and save the json
    """

    series_name = series_suffix
    download_path = staging_path + "/" + series_name + ".json"
    url = "https://covidtracking.com/api/v1/states/daily.json"
    response = requests.get(url)
    with open(download_path, "bw") as f:
        f.write(response.content)


if __name__ == "__main__":
    download_date = datetime.now().strftime("%Y%m%d")
    staging_path = "data/staging/" + download_date

    pathlib.Path(staging_path).mkdir(parents=True, exist_ok=True)

    print(f"Downloading data from CovidTracking")
    download_covid_tracking_json(
            series_suffix="covidtracking",
            staging_path=staging_path,
        )