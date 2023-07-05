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

## System components

![System Components](doc/components.png)

## Class model for the BNBOT backend

![Business Model](doc/business_model.png)

## Flow Diagram

![Flow Diagram](doc/flow_diagram.png)


# This is just for me, do worry about this.

terraform apply -var 'env_name=dev' -var 'open_ai_token=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' -var 'whatsapp_url=https://graph.facebook.com/v17.0/102195312913032/messages' -var 'whatsapp_token=EAAJASfMaTY4BACxRQBJM7qlYmm8SwvEgTZCABrSfLn7bLcbUJQdxXlWH2AEwAZAGiFQsXysXzJj0IsMo4ukERahQDwpwBTymInMTLAaxjkdOuTZCvihIVsg5skN4oXwYohHJN3GwWV7zTF2HtG2uyZAiVPNbrleUpOJp19zg7oQZBzdPBgAzohm4Ya14K5ILVkCpjZBobyPgZDZD'


aws dynamodb create-table \
    --table-name businesses \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url http://localhost:8000