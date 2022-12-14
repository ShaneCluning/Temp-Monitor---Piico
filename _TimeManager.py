import ntptime
import time

NTP_TIME_REFRESH_DELAY = 60 * 60 * 1000  # 1 hour


ntptime.host = "pool.ntp.org"
next_ntp_check_time = 0


def checkNTP():
    global next_ntp_check_time
    now = time.ticks_ms()
    try:
        if time.ticks_diff(next_ntp_check_time, now) <= 0:
            print("Updating NTP")
            next_ntp_check_time = time.ticks_add(now, NTP_TIME_REFRESH_DELAY)
            refreshNTP()
    except Exception as err:
        print("error: %s, %s" % (str(err), str(type(err).__name__)))


def refreshNTP():
    ntptime.settime()


def getISO8601TimeString():
    raw_time = time.gmtime()

    iso_string = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        raw_time[0], raw_time[1], raw_time[2], raw_time[3], raw_time[4], raw_time[5]
    )

    return iso_string
