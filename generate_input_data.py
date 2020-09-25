import pandas as pd
import os
from math import tan, sin, cos, radians
import json
import requests


def isEarlierThanIMERG(year, month, day):
    if int(year) > 2000:
        return False
    if int(year) == 2000:
        if int(month) >= 6:
            return False
    return True


def rain2input(root):
    STATION_IDS = []
    with open('./station_ids.json') as json_file:
        STATION_IDS = json.load(json_file)
    file_paths = sorted(os.listdir(root))
    with open('input.csv', 'w+') as f:
        f.write('date')
        for sid in STATION_IDS:
            f.write(';' + sid)
        f.write('\n')
        for file_path in file_paths:
            if not file_path.endswith('csv'):
                continue
            date = file_path[:-4]
            year = date[:4]
            month = date[4:6]
            day = date[6:]
            if isEarlierThanIMERG(year, month, day):
                continue
            print(file_path)
            df = pd.read_csv(root + file_path, skipinitialspace=True)
            curr_ids = df.station.unique()
            rains = {}
            for sid in curr_ids:
                if sid not in STATION_IDS:
                    continue
                raw_rain = df.loc[df.station == sid]['PP01(mm)'].values
                raw_rain = raw_rain[raw_rain > 0]
                rains[sid] = sum(raw_rain)
            f.write('%s/%s/%s' % (day, month, year))
            for idx, sid in enumerate(STATION_IDS):
                if sid not in rains.keys():
                    f.write(';%s' % (-999))
                else:
                    f.write(';%s' % (rains[sid]))
            f.write('\n')


def latlon2xy(lat, lon):
    a = 6378137.0
    b = 6356752.314245
    long0 = radians(121)
    k0 = 0.9999
    dx = 250000
    e = (1-b**2/a**2)**0.5
    e2 = e**2/(1-e**2)
    n = (a-b)/(a+b)
    nu = a/(1-(e**2)*(sin(lat)**2))**0.5
    p = lon-long0

    A = a*(1 - n + (5/4.0)*(n**2 - n**3) + (81/64.0)*(n**4 - n**5))
    B = (3*a*n/2.0)*(1 - n + (7/8.0)*(n**2 - n**3) + (55/64.0)*(n**4 - n**5))
    C = (15*a*(n**2)/16.0)*(1 - n + (3/4.0)*(n**2 - n**3))
    D = (35*a*(n**3)/48.0)*(1 - n + (11/16.0)*(n**2 - n**3))
    E = (315*a*(n**4)/51.0)*(1 - n)

    S = A*lat - B*sin(2*lat) + C*sin(4*lat) - D*sin(6*lat) + E*sin(8*lat)

    K1 = S*k0
    K2 = k0*nu*sin(2*lat)/4.0
    K3 = (k0*nu*sin(lat)*(cos(lat)**3)/24.0) * (5 - tan(lat)
                                                ** 2 + 9*e2*(cos(lat)**2) + 4*(e2**2)*(cos(lat)**4))

    y = K1 + K2*(p**2) + K3*(p**4)

    K4 = k0*nu*cos(lat)
    K5 = (k0*nu*(cos(lat)**3)/6.0) * (1 - tan(lat)**2 + e2*(cos(lat)**2))

    x = K4*p + K5*(p**3) + dx
    return x, y


def parseStationInfoFromAPI():
    with open('./location.csv', 'w+') as f:
        f.write('X;Y;Z;CODE;ERRP;NDEC;NAME\n')
        r = requests.get(
            'https://sta.ci.taiwan.gov.tw/STA_Rain/v1.0/Things?$expand=Locations&$select=name,properties&$count=true')
        station_ids = []
        while True:
            data = json.loads(r.text)
            print(len(data['value']))
            for station in data['value']:
                fullname = station['name']
                _, sid, sname = fullname.split('-')
                station_ids.append(sid)
                x, y = station['Locations'][0]['location']['coordinates']
                f.write('%s;%s;%s;%s;%s;%s;%s\n' %
                        (x, y, 30, sid, 0.05, 0, sname))
            if '@iot.nextLink' not in data.keys():
                break
            print(data['@iot.nextLink'])
            r = requests.get(data['@iot.nextLink'])
    with open('station_ids.json', 'w+') as outfile:
        json.dump(station_ids, outfile)


def main():
    root = './Rain/Rain_1998-2017/'
    rain2input(root)
    # parseStationInfoFromAPI()


if __name__ == "__main__":
    main()
