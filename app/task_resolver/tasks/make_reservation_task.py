from app.task_resolver.engine import Task, Step
from app.task_resolver.step_resolvers import GatherBookingInfoResolver, HouseSelectionResolver, GatherUserInfoResolver, BookingConfirmationResolver, ExitTaskResolver, PostProcessRouterResolver

from typing import List, Optional
from app.task_resolver.engine import Task, Step
from app.task_resolver.engine.task_model import Step

class MakeReservationTask(Task):

    def __init__(self):

        gather_booking_info_step = Step(
            name="GATHER_BOOKING_INFO", 
            resolver=GatherBookingInfoResolver(), 
            reply_when_done=False)
        
        house_selection_step = Step(
            name="HOUSE_SELECTION", 
            resolver=HouseSelectionResolver(), 
            reply_when_done=False)
        
        gather_user_info_step = Step(
            name="GATHER_USER_INFO", 
            resolver=GatherUserInfoResolver(), 
            reply_when_done=False)
        
        booking_confirmation_step = Step(
            name = "BOOKING_CONFIRMATION",
            resolver = BookingConfirmationResolver())

        super().__init__(name="RESERVATION_TASK", 
                         steps=[gather_booking_info_step, house_selection_step, gather_user_info_step, booking_confirmation_step])

    def get_next_task(self) -> Optional[Task]:
        return None


def create_make_reservation_task():
    return MakeReservationTask()

    
