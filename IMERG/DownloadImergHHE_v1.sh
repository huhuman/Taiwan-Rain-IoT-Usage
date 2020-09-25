#!/bin/bash
Now=`date -u -d'7 hour ago'  +%Y%m%d%H`
NowYear=`date -u -d'7 hour ago'  +%Y`
NowMonth=`date -u -d'7 hour ago'  +%m`
NowDate=`date -u -d'7 hour ago'  +%d`
NowHour=`date -u -d'7 hour ago'  +%H`
NowDayOfYear=`date -u -d'7 hour ago'  +%j`
NowInSec=`date -u -d'7 hour ago'  +%s`
sHHMMInSec=$(($NowInSec - ($NowInSec % (30 * 60))))
sHHMMSS=`date -u -d"@$sHHMMInSec" +%H%M%S`
sHH=`date -u -d"@$sHHMMInSec" +%H`
sMM=`date -u -d"@$sHHMMInSec" +%M`
eHHMMInSec=$(($NowInSec - ($NowInSec % (30 * 60)) + (30*60) - 1))
eHHMMSS=`date -u -d"@$eHHMMInSec" +%H%M%S`
nHHHH=$(printf "%04d" $((10#$sHH*60 + $sMM)))
FileName=$FileTitle$NowYear$NowMonth$NowDate'.'$NowHour'00.dat.gz'
GPMHost='https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3'
GPMProduct='/GPM_3IMERGHHE.05'
EarthDataUser='fangwlp'
EarthDataPass='ILoveDerby82'
GPMPath='/'$NowYear'/'$NowDayOfYear'/3B-HHR-E.MS.MRG.3IMERG.'$NowYear$NowMonth$NowDate'-S'$sHHMMSS'-E'$eHHMMSS'.'$nHHHH'.V05B.HDF5.nc?precipitationCal[2680:2959][961:1200],lat[961:1200],lon[2680:2959]'

echo $GPMHost$GPMProduct$GPMPath

cd I:/Testbed_for_tools/FEWS_Laos
'C:/Program Files/Git/bin/wget.exe' -c --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --user=$EarthDataUser --password=$EarthDataPass --content-disposition $GPMHost$GPMProduct$GPMPath

#https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGHHE.05/2018/212/3B-HHR-E.MS.MRG.3IMERG.20180731-S000000-E002959.0000.V05B.HDF5.nc?precipitationCal[2680:2959][961:1200],lat[961:1200],lon[2680:2959]