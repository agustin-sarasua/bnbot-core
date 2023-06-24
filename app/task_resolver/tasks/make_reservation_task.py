from app.system import Task, Step
from app.task_resolver import GatherBookingInfoResolver, HouseSelectionResolver, GatherUserInfoResolver, BookingConfirmationResolver, ExitTaskResolver

def create_make_reservation_task():
    exit_task_step = Step("EXIT_TASK_STEP", ExitTaskResolver(), force_execution=True, reply_when_done=False)
    gather_booking_info_step = Step("GATHER_BOOKING_INFO", GatherBookingInfoResolver(), reply_when_done=False)
    house_selection_step = Step("HOUSE_SELECTION", HouseSelectionResolver())
    gather_user_info_step = Step("GATHER_USER_INFO", GatherUserInfoResolver(), reply_when_done=False)
    booking_confirmation_step = Step("BOOKING_CONFIRMATION", BookingConfirmationResolver())
    
    reservation_task = MakeReservationTask("RESERVATION_TASK", [exit_task_step, gather_booking_info_step, house_selection_step, gather_user_info_step, booking_confirmation_step])

    return reservation_task

class MakeReservationTask(Task):

    def post_processing(self):
        last_step_data = self.steps[:-1].data
        if "booking_confirmed" in last_step_data and last_step_data["booking_confirmed"] == "True":
            pass
        else:
            pass