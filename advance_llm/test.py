from openai import OpenAI
client = OpenAI(api_key="sk-")

with open('q1.doc', 'r', encoding='utf-8') as file:
    content = file.read()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": content
        }
      ]
    },
    
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)