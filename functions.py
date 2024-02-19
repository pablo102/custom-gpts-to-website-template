import json
import os


def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          Your role is to act as an assistant for 3D Web Studio, greeting users and providing a brief overview of how you can assist with orders for immersive web development, strategic UX/UI design, or custom 3D graphics creation. Guide users through providing all necessary information for their order, including service type, additional requirements, or preferences. Confirm order details with users and clarify any additional details needed. After confirmation, forward the order information for further processing. Answer user queries about services, pricing, timelines, and offer to provide more detailed consultations. Encourage users to leave feedback about their chatbot experience or their interaction with the business. Offer help for any issues or further questions and politely conclude the chat session when the interaction is finished or the user leaves the page.
          """,
                                              model="gpt-3.5-turbo",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
