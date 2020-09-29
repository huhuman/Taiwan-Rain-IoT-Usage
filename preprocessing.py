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
    for auto_file, metro_file in zip(auto_list, metro_list):
        auto_df = pd.read_csv(
            folder_path + auto_file, skipinitialspace=True, encoding='big5')
        metro_df = pd.read_csv(
            folder_path + metro_file, skipinitialspace=True, encoding='big5')
        dtime_list = auto_df['DTIME'].str.split(
            ' ', expand=True).iloc[:, 0].unique()
        print('Total days of %s are %s' %
              (dtime_list[0][:-3], len(dtime_list)))
        for date in dtime_list:
            print('Processing ' + date)
            # auto "DTIME","ID","CNAME","R"
            auto_target = auto_df.loc[auto_df['DTIME'].str.contains(date)]
            auto_target = auto_target.loc[auto_target['R'] > 0]
            auto_station_list = auto_df.ID.unique()
            # metro "DTIME","ST_NO","C_STATION","DD_RMN"
            metro_target = metro_df.loc[metro_df['DTIME'].str.contains(date)]
            metro_target = metro_target.loc[metro_target['DD_RMN'] > 0]
            metro_station_list = metro_df.ST_NO.unique()
            with open(export_path + date + '.csv', 'w+') as f:
                f.write('date, station, PP01(mm)\n')
                for sid in auto_station_list:
                    station_rain_info = auto_target.loc[auto_target.ID == sid]
                    rain = station_rain_info.iloc[:, -1].sum()
                    f.write('%s,%s,%s\n' %
                            (date, sid, rain))
                for sid in metro_station_list:
                    station_rain_info = metro_target.loc[metro_target.ST_NO == sid]
                    rain = station_rain_info.iloc[:, -1].sum()
                    f.write('%s,%s,%s\n' %
                            (date, sid, rain))

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


def main():
    # processRainHistory('./Rain/Rain_1998-2017.txt')
    processRain2018('./Rain/Rain_2018/')


if __name__ == "__main__":
    main()
