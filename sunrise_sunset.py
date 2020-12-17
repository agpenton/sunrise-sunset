#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta
from time import sleep
import os
import pytz
import logging

from astral.location import Location

logger = logging.getLogger(__name__)


def get_loc_from_ip():

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
        location.name = loc['country']
        location.region = loc['country_iso']
        location.latitude = loc['latitude']
        location.longitude = loc['longitude']
        location.timezone = loc['time_zone']
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
    print(f"You are in {location.name} and the timezone is {location.timezone}")

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


if __name__ == '__main__':
    main()
