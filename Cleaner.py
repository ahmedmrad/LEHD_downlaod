import pandas as pd
import numpy as np
import glob
import os
import os.path
import time
import FTP_Downloader as ftp

os.chdir(os.getcwd())
path = 'Enter your own path'
# check if the URL is still working
url_link = 'https://lehd.ces.census.gov/data/lodes/LODES7'
state_mapping = pd.read_csv('state.csv')
all_files = sorted(
    [os.path.basename(x) for x in glob.glob(os.path.join(path, '*.csv'))])
# extract specific columns, you might want to choose other columns
columns_toExtract = [
    'w_geocode', 'Year', 'C000', 'CNS01', 'CNS02', 'CNS03', 'CNS04', 'CNS05',
    'CNS06', 'CNS07', 'CNS08', 'CNS09', 'CNS10', 'CNS11', 'CNS12', 'CNS13',
    'CNS14', 'CNS15', 'CNS16', 'CNS17', 'CNS18', 'CNS19', 'CNS20'
]


def state_getter():
    states = ftp.get_href(url_link, 9)
    state_list = []
    for state in states:
        state_list.append(state.split('/')[0])
    return state_list


def main():
    state_list = state_getter()
    counter = 0
    for state in state_list:
        for name in state_mapping['state']:
            if state == 'us' or state == 'pr' or state == 'vi':
                continue
            else:
                if state == name.lower():
                    file_perState = [
                        file for file in all_files
                        if state in file.split('_')[0]
                    ]
                    list_dframes = [
                        pd.read_csv(file_name) for file_name in file_perState
                    ]
                    for dataframe, file_name in zip(list_dframes,
                                                    file_perState):
                        dataframe['Year'] = file_name.split('_')[4].split('.')[
                            0]
                    list_dframes = [
                        pd.DataFrame(file_name, columns=columns_toExtract)
                        for file_name in list_dframes
                    ]
                    concatenated_dataFrame = pd.concat(
                        list_dframes, ignore_index=True)
                    concatenated_dataFrame.sort_values(by=['Year'])
                    concatenated_dataFrame.to_csv(
                        'enter your own path/LEHD_%s.csv'
                        % state_mapping['state_code'][counter],
                        index=False)
                    counter += 1


if __name__ == '__main__':
    main()
