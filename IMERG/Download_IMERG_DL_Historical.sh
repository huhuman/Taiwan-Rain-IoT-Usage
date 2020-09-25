#!/bin/bash
os=$(uname -s)
if [[ "$os" != "Darwin" ]]; then
    exit 1
fi
input_startdate="$1"
input_enddate="$2"

mkdir $input_startdate/
rm -r $input_startdate/*

range_lon='[2990:3030]'
range_lat='[1109:1159]'
startdate=`date -j -f "%Y-%m-%d" "$input_startdate" +"%Y-%m-%d"` || exit 1
enddate=`date -j -f "%Y-%m-%d" "$input_enddate" +"%Y-%m-%d"` || exit 1
# 119, 21, 123, 26
# https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGDL.06/2019/12/3B-DAY-L.MS.MRG.3IMERG.20191216-S000000-E235959.V06.nc4.nc4?precipitationCal[0:0][2990:3030][1109:1159],time,lon[2990:3030],lat[1109:1159],nv
GPMHost='https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3'
GPMProduct='/GPM_3IMERGDL.06'

EarthDataUser='b02501030@gmail.com'
EarthDataPass='As0930909157'
urldate="$input_startdate"

while [ "$urldate" != "$enddate" ] 
do
    echo $urldate
    NowYear=`date -j -f "%Y-%m-%d" "$urldate" +"%Y"`
    NowMonth=`date -j -f "%Y-%m-%d" "$urldate" +"%m"`
    NowDate=`date -j -f "%Y-%m-%d" "$urldate" +"%d"`
    GPMPath='/'$NowYear'/'$NowMonth'/3B-DAY-L.MS.MRG.3IMERG.'$NowYear$NowMonth$NowDate'-S000000-E235959.V06.nc4.nc4?precipitationCal[0:0]'$range_lon''$range_lat',time,lon'$range_lon',lat'$range_lat',nv'
    echo "$GPMHost$GPMProduct$GPMPath"
    cd $input_startdate/
    curl -n -c ~/.urs_cookies -b ~/.urs_cookies -LJO --url $GPMHost$GPMProduct$GPMPath
    cd ../
    urldate=$(date -j -v +1d -f "%Y-%m-%d" "$urldate" +"%Y-%m-%d")
done