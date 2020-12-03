#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta
# import time
from time import sleep
import os
import pytz
import tzlocal
import logging

from astral.location import Location

logger = logging.getLogger(__name__)


# params = {"lat": 40.177200, "lng": 44.503490, "date": "today"}
# f = r"https://api.sunrise-sunset.org/json?"


def get_loc_from_ip():
    # import requests

    #   Try to reach ipinfo a max of 15 times, if no connection or html response not OK log and wait
    con_err_msg = 'Can\'t reach https://ifconfig.co/ (Network may be down). Waiting 5 minutes to try again...'
    for i in range(15):
        try:
            # g = requests.get('https://ipinfo.io/json')
            g = requests.get('https://ifconfig.co/json')
        except (requests.exceptions.ConnectionError, ConnectionAbortedError,
                ConnectionRefusedError, ConnectionResetError):
            logger.warning(con_err_msg)
            sleep(300)
        else:
            if not g.status_code == 200:
                logger.warning(con_err_msg)
                sleep(300)
            else:
                return g

    return


def main():
    loc = get_loc_from_ip()
    loc = json.loads(loc.text)
    # loc['latitude'], loc['longitude'] = (float(x) for x in loc['loc'].strip().split(','))
    # loc['time_zone'] = tzlocal.get_localzone().zone
    # print(loc['ip'])

    try:
        location = Location()
        location.name = loc['city']
        # print(location.name)
        location.region = loc['region_name']
        # print(location.region)
        location.latitude = loc['latitude']
        # print(location.latitude)
        location.longitude = loc['longitude']
        # print(location.longitude)
        location.timezone = loc['time_zone']
        # print(location.timezone)
    except ValueError as e:
        logger.error(str(e))
        return

    sunrise = location.sun()['sunrise'].replace(second=0) + timedelta(minutes=0)
    sunset = location.sun()['sunset'].replace(second=0) + timedelta(minutes=0)
    today = datetime.now().astimezone(pytz.timezone("Asia/Yerevan")) + timedelta(minutes=0)

    dawn = sunrise.astimezone(pytz.timezone("Asia/Yerevan")).strftime('%H:%M:%S')
    dusk = sunset.astimezone(pytz.timezone("Asia/Yerevan")).strftime('%H:%M:%S')
    now = today.strftime('%H:%M:%S')
    print(f'Dawn: {dawn}')
    print(f'Dusk: {dusk}')
    print(f'Now: {now}')

    if now < dawn:
        print("oh still dark")
        os.system("gsettings set org.gnome.desktop.interface gtk-theme 'Mc-OS-CTLina-Gnome-Dark-1.3.2'")
    elif dawn < now < dusk:
        print("it a brand new day")
        os.system("gsettings set org.gnome.desktop.interface gtk-theme 'McOS-CTLina-Gnome-1.3.2'")
    else:
        print("oh is dark")
        os.system("gsettings set org.gnome.desktop.interface gtk-theme 'Mc-OS-CTLina-Gnome-Dark-1.3.2'")

    return sunrise.astimezone(pytz.timezone("Asia/Yerevan")), sunset.astimezone(pytz.timezone("Asia/Yerevan"))


# def sunrisesunset(f):
#     os.environ['TZ'] = 'Asia/Yerevan'
#     timezone = pytz.timezone("Asia/Yerevan")
#     time.tzset()
#     a = requests.get(f, params=params)
#     a = json.loads(a.text)
#     sunup = datetime.strptime(a["results"]["sunrise"], '%I:%M:%S %p').astimezone(tz=timezone)
#     sundown = datetime.strptime(a["results"]["sunset"], '%I:%M:%S %p').astimezone(tz=timezone)
#     day_length = datetime.strptime(a["results"]["day_length"], '%H:%M:%S').astimezone(tz=timezone)
#
#     today = datetime.now().astimezone(tz=timezone) + timedelta(0, 0)
#     # now = datetime.now().replace(microsecond=0) + timedelta(days=365, microseconds=0)
#     now = today.time().replace(microsecond=0)
#     sunrise = sunup + timedelta(0, 14400,microseconds=0)
#     sunset = sundown + timedelta(0, 14400, microseconds=0)
#     sunset.strftime('%H:%M:%S')
#     print(sunrise.time())
#     print(f'sunset: {sunset}')
#     print(today.timetz().replace(microsecond=0))
#     print("-->", now, " -->", sunrise)
#     # if now < sunrise:
#     #     print("oh still dark")
#     #     os.system("gsettings set org.gnome.desktop.interface gtk-theme 'Mc-OS-CTLina-Gnome-Dark-1.3.2'")
#     # elif sunrise < now < sunset:
#     #     print("it a brand new day")
#     #     os.system("gsettings set org.gnome.desktop.interface gtk-theme 'McOS-CTLina-Gnome-1.3.2'")
#     # else:
#     #     print("oh is dark")
#     #     os.system("gsettings set org.gnome.desktop.interface gtk-theme 'Mc-OS-CTLina-Gnome-Dark-1.3.2'")


if __name__ == '__main__':
    main()
