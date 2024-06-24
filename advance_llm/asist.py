from openai import OpenAI
import os
from typing_extensions import override
from openai import AssistantEventHandler
 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 

client = OpenAI(api_key= "")
file = client.files.create(
  file=open("q1.doc", "rb"),
  purpose='assistants'
)

assistant = client.beta.assistants.create(
  name="Ortool Coder",
  description="You are great at code ortools. You analyze the Description, input, output and examples in .doc files, understand problem and write the code caculate exactly the solution of problem by ortools.linear_solver",
  model="gpt-3.5-turbo",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": [{
          "type": "text",
          "text": "write code to solve problem by ortools.linear_solver."
        },
        {
          "type": "text",
          "text": {"url": "https://example.com/image.png"}
        },],
      "attachments": [
        {
          "file_id": file.id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
)


with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  model="gpt-3.5-turbo",
  instructions="New instructions that override the Assistant instructions",
  tools=[ {"type": "file_search"}],
  event_handler=EventHandler(),
) as stream:
  stream.until_done()