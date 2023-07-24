from location_app.models import City
from rest_framework.response import Response
from rest_framework import status
import re
import datetime

from .helper import BookingAppHelper
from playground_app.helper import PlaygroundSerializerHelper
from playground_app.models import Playground
from .models import Booking
from helper_files.time_operations_helper import TimeOperationsHelper
from helper_files.status_code import Status_code


class BookingAppValidations():

    def validate_booking_created(self, data, valid, err):
        h_m_s_regex = "^(((([0-1][0-9])|(2[0-3])):?[0-5][0-9]:?[0-5][0-9]+$))"
        yyyy_mm_dd_regex = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"

        if valid:
            if not re.match(h_m_s_regex, data['start_time']):
                return Response(data={'message': "Booking's start_time doesn't match time H:M:S format",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if not re.match(h_m_s_regex, data['end_time']):
                return Response(data={'message': "Booking's end_time doesn't match time H:M:S format",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if data['start_time'] == data['end_time']:
                return Response(data={'message': "Booking's start_time and end_time can't be the same",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if TimeOperationsHelper.convert_str_time_format(
                    data['start_time']) > TimeOperationsHelper.convert_str_time_format(
                data['end_time']):
                return Response(data={'message': "Booking's start_time can't be greater than end_time",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if not re.match(yyyy_mm_dd_regex, data['date']):
                return Response(data={'message': "Booking's date doesn't match time YYYY-MM-DD format.",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if not City.objects.filter(city_name=data['city']).exists:
                return Response(data={'message': "No city was found with the name " + str(data['city']),
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)

            if 'expiration_time' in data.keys():
                if not re.match(h_m_s_regex, data['expiration_time']):
                    return Response(data={
                        'message': "Expiration time doesn't match time H:M:S format.",
                        'status': Status_code.bad_request},
                        status=Status_code.bad_request)

                elif TimeOperationsHelper.convert_str_time_format(
                        data['expiration_time']) <= datetime.datetime.now().time():
                    return Response(data={
                        'message': "Expiration time can not be less than or equal datetime.now()",
                        'status': Status_code.bad_request},
                        status=Status_code.bad_request)

            if 'payment_status' in data.keys():
                if data['payment_status'] not in ['pending', 'paid']:
                    return Response(data={
                        'message': "payment_status has only two options 'pending' or 'paid'",
                        'status': Status_code.bad_request},
                        status=Status_code.bad_request)

            is_booking_available, availabe_hours = BookingAppValidations.validate_booking_time(
                self, data)
            if is_booking_available:
                return Response(data={"message": "Booking was created successfully.",
                                      'status': Status_code.created},
                                status=Status_code.created)
            else:
                return Response(data={'message': "Playground is already booked",
                                      'status': Status_code.bad_request,
                                      "availabe_hours_to_be_booked": availabe_hours, },
                                status=Status_code.bad_request)

        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)

    def validate_booking_update(self, data, valid, err, instance):
        h_m_s_regex = "^(((([0-1][0-9])|(2[0-3])):?[0-5][0-9]:?[0-5][0-9]+$))"
        yyyy_mm_dd_regex = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
        if valid:
            if not data:
                return Response(data={'message': "Can not update a booking with an empty body.",
                                      'status': Status_code.bad_request},
                                status=Status_code.bad_request)
            if 'start_time' in data.keys():
                if not re.match(h_m_s_regex, data['start_time']):
                    return Response(data={'message': "Booking's start_time doesn't match time H:M:S format.",
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)

            if 'end_time' in data.keys():
                if not re.match(h_m_s_regex, data['end_time']):
                    return Response(data={'message': "Booking's end_time doesn't match time H:M:S format.",
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)

            if 'start_time' in data.keys() and 'end_time' in data.keys():
                if data['start_time'] == data['end_time']:
                    return Response(data={'message': "Booking's start_time and end_time can't be the same.",
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)
            if 'start_time' in data.keys() and 'end_time' in data.keys():
                if TimeOperationsHelper.convert_str_time_format(
                        data['start_time']) > TimeOperationsHelper.convert_str_time_format(data['end_time']):
                    return Response(data={'message': "Booking's start_time can't be greater than end_time.",
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)
            if 'date' in data.keys():
                if not re.match(yyyy_mm_dd_regex, data['date']):
                    return Response(data={'message': "Booking's date doesn't match time YYYY-MM-DD format.",
                                          'status': Status_code.bad_request},
                                    status=Status_code.bad_request)

            if 'payment_status' in data.keys():
                if data['payment_status'] not in ['pending', 'paid']:
                    return Response(data={
                        'message': "payment_status has only two options 'pending' or 'paid'.",
                        'status': Status_code.bad_request},
                        status=Status_code.bad_request)

            if 'expiration_time' in data.keys():
                return Response(data={
                    'message': "expiration_time can not be updated.",
                    'status': Status_code.bad_request},
                    status=Status_code.bad_request)

            # if the request doesn't have start_time or end_time, it means it isn't a correct request. so the given
            # times and date are neglected and we use the instance's original times and date and only apply the update
            # the rest of the given fields like payment_status
            if 'start_time' not in data.keys() or 'end_time' not in data.keys():
                data['start_time'] = instance.start_time
                data['end_time'] = instance.end_time
                data['date'] = instance.date
                return Response(data={"message": "Booking was updated successfully.",
                                      'status': Status_code.updated},
                                status=Status_code.updated)

            # else if the request contains both start_time and end_time we have to check for the availability
            # of the given times, if there's a booking already exists
            else:
                is_booking_available, availabe_hours = BookingAppValidations.validate_booking_time(
                    self, data)

                if is_booking_available:
                    return Response(data={"message": "Booking was updated successfully.",
                                          'status': Status_code.updated},
                                    status=Status_code.updated)
                else:
                    return Response(data={'message': "Playground is already booked for the time slot " +
                                                     str(data['start_time']) + " : " + str(data['end_time']),
                                          'status': Status_code.bad_request,
                                          "available_hours_to_be_booked": availabe_hours, },
                                    status=Status_code.bad_request)

        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)

    # booking here is represented in request.data
    def validate_booking_time(self, booking):
        FMT = '%H:%M:%S'
        playground = Playground.objects.get(id=booking['playground_id'])  # get playground instance by id

        playground_open_hours = PlaygroundSerializerHelper.get_all_available_hours(
            playground)  # get playground's all available hours

        availabe_hours = BookingAppHelper.get_playground_available_booking_hours(
            booking['playground_id'],  # get playground's available hours to be booked
            booking['date'],
            playground_open_hours
        )
        playground_booked_hours = Booking.objects.filter(  # return all the bookings for specific playground
            playground_id=booking['playground_id'],  # on a specific date
            date=booking['date'])

        if playground_booked_hours.exists():  # checks if there are any bookings for the
            start_time = TimeOperationsHelper.convert_str_time_format(  # playground on that date, if not
                booking['start_time'])  # return all the playground's availabe_hours
            end_time = TimeOperationsHelper.convert_str_time_format(  # if there are any bookings, then
                booking['end_time'])

            # get all the bookings as hours ex: if booking from 10:00:00 to 11:00:00, then to_be_booked_hours
            # will save hour datetime.time(10, 0). therefore the list will contain all the bookings in hours
            # [d.time(10, 0),d.time(11, 0),...etc]
            to_be_booked_hours = BookingAppHelper.get_hours_to_be_booked(start_time, end_time)

            for i in range(len(to_be_booked_hours)):  # for every to_be_booked_hours check for
                for j in range(len(playground_booked_hours)):  # for every playground_booked_hours
                    already_booked_start_time = TimeOperationsHelper.convert_str_time_format(
                        playground_booked_hours[j].start_time)
                    already_booked_end_time = TimeOperationsHelper.convert_str_time_format(
                        playground_booked_hours[j].end_time)
                    # get booked hours for every booking, for ex if that date has 3 bookings, then each booking
                    # will be represented as a list of hours
                    already_booked_hours = BookingAppHelper.get_hours_to_be_booked(
                        already_booked_start_time, already_booked_end_time)

                    # for every booking's list of hours check if it contains the hour that we wish to book
                    # that ensures that even if the already booked was from [10 to 12] it will be represented as
                    # [(10),(11)], so if the user tried to book from [11 to 12] it will be represented as [(11)]
                    # therefore it will return a validation error, so no in between booking can be accepted.
                    # <--------b.st 10-------------11---------------b.et 12--------------13-------------14----->
                    if to_be_booked_hours[i] in already_booked_hours:

                        return False, PlaygroundSerializerHelper.calc_paired_hours(availabe_hours)

                    else:  # in the frontend side the user will only be able to select from
                        pass  # the availabe_hours and can't send a request that contains already
                        # booked hours, but this validation is necessary to avoid any potential
                        # attempt to miss use the request
            return True, PlaygroundSerializerHelper.calc_paired_hours(availabe_hours)

        else:
            return True, availabe_hours
