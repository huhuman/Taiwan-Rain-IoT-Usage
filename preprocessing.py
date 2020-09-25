import os
import json
import pandas as pd
import numpy as np

# Definition of the Parameters: PP01 降水量(mm)
# RAIN_COLUMN_NAMES = ["CD01", "CD02", "CD03", "CD04", "CD05", "CD06", "CD07", "CD08", "CD09", "CD10",
#                      "CD11", "EP03", "PP01", "PP02", "PS01", "PS02", "PS03", "RH01", "RH02", "RH03",
#                      "ST01", "ST02", "ST03", "ST04", "ST05", "ST06", "ST07", "ST08", "ST09", "ST10",
#                      "ST11", "ST12", "SS01", "SS02", "SS03", "TS01", "TS02", "TS03", "TS04", "TS05",
#                      "TS06", "TS07", "TX01", "TX02", "TX03", "TX04", "TX05", "VS01", "WD01", "WD02",
#                      "WD03", "WD04", "WD05", "WD06", "UV01", ]

'''Special Value in the Data Array
-9991:儀器故障待修
-9996:資料累計於後
-9997:因不明原因或故障而無資料
-9998:雨跡(Trace)
-9999:未觀測而無資料
* In addition to the above columns, there will also be spaces for 'date' and 'stno'.
'''
RAIN_DATA = {}


def processRainHistory(txtPath):
    startRecordData = False
    number_of_lines = 0
    with open(txtPath, 'r', encoding='big5') as f:
        content = f.readline()
        while content:
            header = content[0:2]
            if '#' in header:
                startRecordData = True
                column_name = content.split(' ')[-1].replace('\n', '')
                print(column_name)
                # column_index = RAIN_COLUMN_NAMES.index(column_name)
                content = f.readline()
                continue
            if startRecordData:
                number_of_lines += 1
                if number_of_lines % 100000 == 0:
                    print(number_of_lines)
                stno = content[:6]
                date = content[7:17]
                year_month_day = date[:8]
                value = float(content[18:].replace(' ', '').replace('\n', ''))
                RAIN_DATA.setdefault(year_month_day, [[], [], []])[
                    0].append(date)
                RAIN_DATA.setdefault(year_month_day, [[], [], []])[
                    1].append(stno)
                RAIN_DATA.setdefault(year_month_day, [[], [], []])[
                    2].append(value)
            else:
                print(content)
            content = f.readline()
    print(RAIN_DATA.keys())
    for date_key in RAIN_DATA.keys():
        with open('./Rain/Rain_1998-2017/%s.csv' % (date_key), 'w+') as outfile:
            outfile.write('date, station, PP01(mm)\n')
            dates, stations, rains = RAIN_DATA[date_key]
            for d, st, r in zip(dates, stations, rains):
                outfile.write('%s, %s, %s\n' % (d, st, r))


def processRain2018(folder_path):
    export_path = folder_path + '../Processed_Rain_2018/'
    os.makedirs(export_path, exist_ok=True)
    auto_list = sorted([filename for filename in os.listdir(
        folder_path) if 'Auto' in filename])
    metro_list = sorted([filename for filename in os.listdir(
        folder_path) if 'Metro' in filename])
    auto_df = pd.read_csv(
        folder_path + auto_list[0], skipinitialspace=True, encoding='big5')
    metro_df = pd.read_csv(
        folder_path + metro_list[0], skipinitialspace=True, encoding='big5')
    dtime_list = np.unique(auto_df['DTIME'].values)
    dtime_list = np.append(
        dtime_list, np.unique(metro_df['DTIME'].values))
    dtime_list = np.unique(dtime_list)
    curr_date, dt_candidates = "", []
    for dt in dtime_list:
        date = dt.split(' ')[0]
        date = date.replace('-', '')
        if curr_date == "":
            curr_date = date
            dt_candidates = [dt]
            continue
        if date == curr_date:
            dt_candidates.append(dt)
        else:
            with open(export_path + curr_date + '.csv', 'w+') as f:
                print('Processing ' + curr_date)
                f.write('date, station, PP01(mm)\n')
                for dt_c in dt_candidates:
                    hour = dt_c.split(' ')[1].split(':')[0]
                    filter_df = auto_df.loc[auto_df['DTIME'] == dt_c, :]
                    auto_df = auto_df.loc[auto_df['DTIME'] != dt_c, :]
                    for _, row in filter_df.iterrows():
                        f.write('%s,%s,%s\n' %
                                (curr_date + hour, row[1], row[3]))
                    filter_df = metro_df.loc[metro_df['DTIME'] == dt_c, :]
                    metro_df = metro_df.loc[metro_df['DTIME'] != dt_c, :]
                    for _, row in filter_df.iterrows():
                        f.write('%s,%s,%s\n' %
                                (curr_date + hour, row[1], row[3]))
            curr_date = date

    # Code for checking station completeness
    # tmp_df = pd.read_csv('./rain_20200501.csv',
    #                      skipinitialspace=True, encoding='big5')
    # print(tmp_df['station_id'].unique().shape)
    # df = pd.read_csv('./Rain/rain_station.csv', skipinitialspace=True)
    # sids = df['station_id'].values
    # with open('show.csv', 'w+') as f:
    #     for sid in tmp_df['station_id'].unique():
    #         if sid in sids:
    #             f.write('%s\n' % (sid))
    #         else:
    #             print(sid)


def processRainRaw(folder_path):
    # df = pd.read_csv(folder_path + 'rain_20191201.csv', skipinitialspace=True)
    # # df = pd.read_csv('./Rain/Rain_1998-2017/20171231.csv',
    # #                  skipinitialspace=True)
    # # df = pd.read_csv('./Rain/Rain_2018/AutoRain_201801.csv',
    # #                  skipinitialspace=True, encoding='big5')
    # # print(df.head())
    # locations = pd.read_csv(
    #     folder_path + 'rain_station.csv', skipinitialspace=True)

    # locations = locations['station_id'].unique()
    # actual_station = df['station_id'].unique()
    # # actual_station = df['station'].unique()
    # # actual_station = df['ID'].unique()
    # print(locations.shape)
    # print(actual_station.shape)

    # count = 0
    # # locations = [loc[:-1] for loc in locations]
    # for sid in actual_station:
    #     if sid not in locations:
    #         # print(sid)
    #         count += 1
    # print(count)
    pass


def readRainIoT(dataset_root):
    pass


def main():
    # processRainHistory('./Rain/Rain_1998-2017.txt')
    # processRain2018('./Rain/Rain_2018/')
    processRainRaw('./Rain/')


if __name__ == "__main__":
    main()
