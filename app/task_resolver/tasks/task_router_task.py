from system import Task, Step
from task_resolver import TaskIdentifierResolver, PromptInjectionResolver, ExitTaskResolver

def create_task_router_task():
    detect_prompt_injection_step = Step("PROMPT_INJECTION_STEP", PromptInjectionResolver(), reply_when_done=False)
    exit_task_step = Step("EXIT_TASK_STEP", ExitTaskResolver(), reply_when_done=False)
    task_identifier_step = Step("TASK_IDENTIFIER_STEP", TaskIdentifierResolver(), reply_when_done=False)
    
    task_router_task = Task("TASK_ROUTER_TASK", [detect_prompt_injection_step, exit_task_step, task_identifier_step])

    return task_router_task