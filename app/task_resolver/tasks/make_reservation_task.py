from app.task_resolver.engine import Task, Step
from app.task_resolver.step_resolvers import GatherBookingInfoResolver, HouseSelectionResolver, GatherUserInfoResolver, BookingConfirmationResolver, ExitTaskResolver, PostProcessRouterResolver

def create_make_reservation_task():
    # exit_task_step = Step("EXIT_TASK_STEP", ExitTaskResolver(), force_execution=True, reply_when_done=False)
    gather_booking_info_step = Step("GATHER_BOOKING_INFO", GatherBookingInfoResolver(), reply_when_done=False)
    
    house_selection_step = Step(
        name="HOUSE_SELECTION", 
        resolver=HouseSelectionResolver(), 
        post_process_router_resolver=PostProcessRouterResolver([
            {"name":"GATHER_BOOKING_INFO", "description":"When the user wants to look for properties in different dates."},
            {"name":"CONTINUE", "description":"When none of the other options fit."},
        ]),
        reply_when_done=False)
    
    gather_user_info_step = Step("GATHER_USER_INFO", GatherUserInfoResolver(), reply_when_done=False)
    
    booking_confirmation_step = Step(
        name = "BOOKING_CONFIRMATION",
        resolver = BookingConfirmationResolver(),
        post_process_router_resolver= PostProcessRouterResolver([
            {"name":"GATHER_BOOKING_INFO", "description":"When the user wants to change the check-in, check-out or number of guests."},
            {"name":"HOUSE_SELECTION", "description":"When the user wants to select a different property."},
            {"name":"GATHER_USER_INFO", "description":"When the user does not want confirm the booking because there is an error or wants to change the email or the name for the reservation."},
            {"name":"CONTINUE", "description":"When none of the other options fit."},
        ]))

    reservation_task = Task(
        "RESERVATION_TASK", 
        [gather_booking_info_step, house_selection_step, gather_user_info_step, booking_confirmation_step])

    return reservation_task