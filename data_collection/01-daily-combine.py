import pathlib
import pandas as pd
from data_collection.config import US_STATES
from datetime import datetime
import json

def load_json_as_dataframe(series_suffix: str, state: str, staging_path: str):
    series_name = state + series_suffix
    json_path = staging_path + "/" + series_name + ".json"
    with open(json_path, "r") as f:
        json_data = json.load(f)

    df = pd.DataFrame(json_data["observations"])
    df.loc[:, "state"] = state
    return df

def load_and_combine_fred_data(download_date: str):

    df_list = list()
    for state in US_STATES:
        staging_path = "data/staging/" + download_date
        df = load_json_as_dataframe(
            series_suffix="ICLAIMS",
            state=state,
            staging_path=staging_path)
        df_list.append(df[["date", "value", "state"]])
    combined_df = pd.concat(df_list)
    output_dir = "data/combined"
    output_file = output_dir + "/iclaims.csv"

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"Writing combined data to file {output_file}")
    combined_df.to_csv(output_file, index=False)
    print("done")


if __name__ == "__main__":
    load_and_combine_fred_data(
        download_date=datetime.now().strftime("%Y%m%d")
    )


def load_covidtracking_dataframe(series_suffix: str, staging_path: str):
    series_name = series_suffix
    json_path = staging_path + "/" + series_name + ".json"
    with open(json_path, "r") as f:
        json_data = json.load(f)

    ct = pd.DataFrame(json_data)
    return ct

def load_and_combine_all_data(download_date: str):

    iclaims = pd.read_csv("data/combined/iclaims.csv")
    iclaims['date'] = pd.to_datetime(iclaims['date'].astype(str), format='%Y-%m-%d', errors='coerce')
    iclaims['number_of_iclaims'] = iclaims['value']
    iclaims.drop('value', axis=1, inplace=True)
    pop = pd.read_csv("data/static/state_populations.csv")
    pop['state'] = pop["state_code"]
    lon_lat= pd.read_csv("data/static/long-lat-states.csv")
    state_actions = pd.read_csv("data/static/state_actions.csv")
    staging_path = "data/staging/" + download_date
    ct = load_covidtracking_dataframe(
            series_suffix="covidtracking",
            staging_path=staging_path)
    ct = ct.drop(['hash'], axis=1)
    #ct["date"] = datetime.datetime.strptime("30-Jan-02", '%d-%b-%y').strftime("%Y%m%d")
    ct['date'] = pd.to_datetime(ct['date'].astype(str), format='%Y-%m-%d', errors='coerce')

    output_dir = "data/combined"
    output_file = output_dir + "/covidtracking.csv"

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"Writing covidtracking data to file {output_file}")
    ct.to_csv(output_file, index=False)
    #combined_df = pd.concat([ct, pop, lon_lat, state_actions], keys='state')
    combined_df = pd.merge(left=ct, right=pop, how='left', on='state')
    combined_df = pd.merge(left = combined_df, right = lon_lat,  how='left',on='state')
    combined_df = pd.merge(left=iclaims, right=combined_df, how="right", on=['state', 'date'])
    combined_df = pd.merge(left=combined_df, right=state_actions,  how='inner',on='state')

    output_dir = "data/combined"
    output_file = output_dir + "/combined.csv"
    print(f"Combining covidtracking and fred, and writing data to file {output_file}")


    combined_df.to_csv(output_file, index=False)
    print("done")
    return

if __name__ == "__main__":
    load_and_combine_all_data(
        download_date=datetime.now().strftime("%Y%m%d")
    )