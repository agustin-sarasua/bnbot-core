from app.task_resolver.engine import Task, Step
from app.task_resolver.step_resolvers import GatherBusinessInfoResolver, BusinessSelectionResolver, PostProcessRouterResolver
from app.integrations import OpenAIClient

def create_select_business_task(openai_integration: OpenAIClient = None):
    # exit_task_step = Step("EXIT_TASK_STEP", ExitTaskResolver(), force_execution=True, reply_when_done=False)
    gather_business_info_step = Step("GATHER_BUSINESS_INFO", GatherBusinessInfoResolver(), reply_when_done=False)
    business_selection_step = Step("BUSINESS_SELECTION", BusinessSelectionResolver(backend_url="http://web:8080"), reply_when_done=False)
    
    # house_selection_step = Step(
    #     name="HOUSE_SELECTION", 
    #     resolver=HouseSelectionResolver(), 
    #     post_process_router_resolver=PostProcessRouterResolver([
    #         {"name":"GATHER_BOOKING_INFO", "description":"This step must be taken only when the user wants to choose different check-in and check-out dates from the one he previously chose."},
    #         {"name":"OTHER", "description":"This step must be taken if the user provided the check-in and check-out dates but he has not selected a house yet."},
    #     ]),
    #     reply_when_done=False)
    
    # gather_user_info_step = Step("GATHER_USER_INFO", GatherUserInfoResolver(), reply_when_done=False)
    
    # booking_confirmation_step = Step(
    #     name = "BOOKING_CONFIRMATION",
    #     resolver = BookingConfirmationResolver(),
    #     # post_process_router_resolver= PostProcessRouterResolver([
    #     #     {"name":"GATHER_BOOKING_INFO", "description":"When the user wants to change the check-in, check-out or number of guests."},
    #     #     {"name":"HOUSE_SELECTION", "description":"When the user wants to select a different property."},
    #     #     {"name":"GATHER_USER_INFO", "description":"When the user does not want confirm the booking because there is an error or wants to change the email or the name for the reservation."},
    #     #     {"name":"OTHER", "description":"When none of the other options fit."},
    #     # ])
    # )

    task = Task(
        "SELECT_BUSINESS_TASK", 
        [gather_business_info_step, business_selection_step])

    return task