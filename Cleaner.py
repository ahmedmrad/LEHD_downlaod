import pandas as pd
import glob
import os
import os.path
import FTP_Downloader as ftp


def get_files(path):
    """Get list of all files with their respective path

    :param path: path of the file to get
    :type path:
    :returns all_files: list of all available csv files
    :rtype all_files: list
    """
    all_files = sorted(
    [os.path.basename(x) for x in glob.glob(os.path.join(path, '*.csv.gz'))])
    return all_files


def state_getter(url_link):
    """Create a list of states

    :param url_link: url link to download the available states
    :type url_link str
    :returns state_list: list of available states
    :rtype state_list: list
    """
    states = ftp.get_href(url_link, 10)
    state_list = []
    for state in states:
        state_list.append(state.split('/')[0])
    return state_list


def main():
    current_path = os.getcwd()
    path_to_files = current_path + '/lehd_files'
    output_folder = path_to_files + '/concatenated_files'
    state_list = state_getter('https://lehd.ces.census.gov/data/lodes/LODES7')
    all_files = get_files(path_to_files)
    for state in state_list:
        if state == 'us' or state == 'pr' or state == 'vi':
                continue
            else:
                file_perState = [file for file in all_files if state in file.split('_')[0]]
                list_dframes = [pd.read_csv(file_name,compression='gzip') for file_name in file_perState]
                for dataframe, file_name in zip(list_dframes,file_perState):
                    dataframe['Year'] = file_name.split('_')[4].split('.')[0]
                    list_dframes = [pd.DataFrame(file_name) for file_name in list_dframes]
                    concatenated_dataFrame = pd.concat(list_dframes, ignore_index=True)
                    concatenated_dataFrame.sort_values(by=['Year'])
                    concatenated_dataFrame.to_csv('{0}/LEHD_{1}.csv'.format(output_folder,state), index=False)

if __name__ == '__main__':
    main()
