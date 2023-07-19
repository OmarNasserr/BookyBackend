from datetime import datetime, timedelta, date
from booking_app.helper import BookingAppHelper


class PlaygroundSerializerHelper():

    # this function is used to calculate all available hours from playground.open_time to
    # playground.close_time in hours
    def get_all_available_hours(playground):
        TIME_FORMAT = "%H:%M:%S"
        start = datetime.strptime(
            playground.open_time, TIME_FORMAT).time()
        close = datetime.strptime(
            playground.close_time, TIME_FORMAT).time()
        hours_available = []
        while start <= close:
            hours_available.append(start)

            if (start.hour != 23):  # because hours must stay between 0 and 23
                # this increases time by 1 hour
                start = start.replace(hour=start.hour + 1)
            else:
                return hours_available

        return hours_available

    # ----------------------------------------------------------------
    # this function return paired available hours 13:00:00-14:00:00,etc
    def get_all_available_paired_hours(playground, date):

        hours_available = BookingAppHelper.get_playground_available_booking_hours(
            playground.id, date, PlaygroundSerializerHelper.get_all_available_hours(playground)
        )

        hours_available = PlaygroundSerializerHelper.calc_paired_hours(
            hours_available)

        return hours_available

    def calc_paired_hours(hours_available):
        hours_available_pair = []
        for i in range(len(hours_available)):
            try:
                if hours_available[i + 1] == PlaygroundSerializerHelper.time_operations(
                        hours_available[i], 1, "add"):  # checks if next hour is equal to current hour+1 this
                    hours_available_pair.append(  # means that this hour is available to be booked
                        str(hours_available[i]) + ' - ' +  # therfore display both hours side by side
                        str(hours_available[i + 1]))  # ex:
                    # hours_available[..,13:00:00,14:00:00,15:00:00..]
                    # we display 13:00:00-14:00:00
                    #           14:00:00-15:00:00
                else:
                    hours_available_pair.append(  # else means that the next hour is booked which is
                        str(hours_available[i]) + ' - ' +  # hour[i+1], but from hour[i] to hour[i+1] which is hour[i]
                        str(PlaygroundSerializerHelper.time_operations(  # isn't booked therfore we display
                            hours_available[i], 1, "add")))  # hour[i]-(hour[i]+1) "-not hour[i+1]-"
            except:  # ex: hours_available[..,13:00:00,15:00:00,..]
                pass  # we display 13:00:00-14:00:00
                #           15:00:00-16:00:00
                # as from 14:00:00 to 15:00:00 is booked
        return hours_available_pair

    def time_operations(time1, time2, operation):
        if operation == "add":  # adds time2 to time1
            result = datetime.combine(
                date.today(), time1) + timedelta(hours=time2)
            return result.time()
        else:
            result = datetime.combine(  # subtract time2 from time1
                date.today(), time1) - timedelta(hours=time2)
            return result.time()
