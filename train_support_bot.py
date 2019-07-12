import os
import argparse
import requests
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv

load_dotenv()

DIALOGFLOW_PROJECT_ID = os.getenv('PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = 'ru-RU'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GA-KEY-ADMIN')


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    print('Intent created: {}'.format(response))


if __name__ == "__main__":

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-u', '--url', action='store', type=str, help='link to file for study', required=True)

    args = args_parser.parse_args()

    url = args.url

    response = requests.get(url)

    if response.ok:

        response_json = response.json()

        for key, item in response_json.items():
            display_name = key
            training_phrases_parts = item['questions']
            message_texts = [item['answer']]

            create_intent(
                project_id=DIALOGFLOW_PROJECT_ID,
                display_name=display_name,
                training_phrases_parts=training_phrases_parts,
                message_texts=message_texts
            )
    else:
        print(f'Request error {response.status_code}')
