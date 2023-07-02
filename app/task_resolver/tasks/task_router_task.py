from app.task_resolver.engine import Task, Step, StepData
from app.task_resolver.step_resolvers import TaskIdentifierResolver, PromptInjectionResolver, ExitTaskResolver

def create_task_router_task() -> Task:
    detect_prompt_injection_step = Step("PROMPT_INJECTION_STEP", PromptInjectionResolver(), reply_when_done=False)
    # exit_task_step = Step("EXIT_TASK_STEP", ExitTaskResolver(), reply_when_done=False)
    task_identifier_step = Step("TASK_IDENTIFIER_STEP", TaskIdentifierResolver())
    
    task_router_task = Task("TASK_ROUTER_TASK", [detect_prompt_injection_step, task_identifier_step])

    return task_router_task

# class TaskRouterTask(Task):

#     def post_processing(self):
#         last_step_data: StepData = self.steps[:-1].data
#         if "booking_confirmed" in last_step_data.data and last_step_data.data["booking_confirmed"] == "True":
#             pass
#         else:
#             pass