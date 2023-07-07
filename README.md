# BNBOT

# Project Documentation

This documentation is for the project **BNBOT Project**. This project is aimed to do *something awesome*.

# The Engine (Framework for the chatbot)

It uses LangChain in some cases, it uses directly chatgpt in other, the idea of the framework is to orchestrate LLM calls, step by step and have the full controll to put code everyware and customize it.

Here is the engine model.

![Engine Model](doc/engine_model.png)

- The engine execute TASKS
- Each TASK is a series of STEPS
- Each STEP has a status (DONE or not DONE)
- Each STEP has a run() method to execute the Step and once the step is executed, the task execute the is_done() method of the Step to determine wether is done or not. 
- Each STEP stores information about the execution of the step in memory usind a "data" dictonary.
- Each STEP has a STEP_RESOLVER which holds the logic for executing the STEP.
- Eeach STEP_RESOLVER can use any TOOLS.

All the code for the enginse is under:
- app/task_resolver/tasks: Tasks definitions
- app/task_resolver/engine: Generic code for executing the Tasks, it also has the engine model definition.
- app/task_resolver/step_resolvers
- app/tools

## Implementation of BNBOT using the engine

![Engine BnBot](doc/engine_bnbot.png)


# Backend

El backend es una API using FastAPI. 
- It uses Clean Architecture Pattern, basically is:
- Presentation (routers) -> UseCases -> Repository -> (DB). For example, to create a reservation you have: reservation_router -> create_reservation_use_case -> reservation_respotiory -> Posgres DB

## System components

![System Components](doc/components.png)

## Class model for the BNBOT backend

![Business Model](doc/business_model.png)

## Flow Diagram

![Flow Diagram](doc/flow_diagram.png)

