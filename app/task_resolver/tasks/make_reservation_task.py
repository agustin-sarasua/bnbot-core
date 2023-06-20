from ...system import Task, Step
from ...task_resolver import GatherBookingInfoResolver, HouseSelectionResolver, GatherUserInfoResolver, BookingConfirmationResolver

def create_make_reservation_task():
    gather_booking_info_step = Step("GATHER_BOOKING_INFO", GatherBookingInfoResolver(), reply_when_done=False)
    house_selection_step = Step("HOUSE_SELECTION", HouseSelectionResolver())
    gather_user_info_step = Step("GATHER_USER_INFO", GatherUserInfoResolver(), reply_when_done=False)
    booking_confirmation_step = Step("BOOKING_CONFIRMATION", BookingConfirmationResolver())
    reservation_task = Task("RESERVATION_TASK", [gather_booking_info_step, house_selection_step, gather_user_info_step, booking_confirmation_step])

    return reservation_task