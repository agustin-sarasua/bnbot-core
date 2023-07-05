from app.task_resolver.engine import Task, Step, StepData
from app.task_resolver.step_resolvers import TaskIdentifierResolver, PromptInjectionResolver, ExitTaskResolver

from app.task_resolver.engine import Task, Step

from typing import List, Optional
from app.task_resolver.engine import Task, Step
from app.task_resolver.engine.task_model import Step
from .select_business_task import create_select_business_task

class TaskRouterTask(Task):

    def __init__(self):
        
        detect_prompt_injection_step = Step(
            name="PROMPT_INJECTION_STEP", 
            resolver=PromptInjectionResolver(), 
            reply_when_done=False)
        
        task_identifier_step = Step(
            name="TASK_IDENTIFIER_STEP", 
            resolver=TaskIdentifierResolver(),
            reply_when_done=False)

        super().__init__(name="TASK_ROUTER_TASK", 
                         steps=[detect_prompt_injection_step, task_identifier_step])

    def get_next_task(self) -> Optional[Task]:
        if self.is_done():
            task_name = self.steps[-1].data.resolver_data["task_info"]["task_id"]
            if task_name is not None and task_name != "":
                if task_name == "MAKE_RESERVATION_TASK":
                    return create_select_business_task()
                else: 
                    return create_task_router_task()
        return None
    

def create_task_router_task():
    return TaskRouterTask()
