import os

import requests
import dialogflow_v2 as dialogflow

DIALOGFLOW_PROJECT_ID = os.getenv('project_id')
DIALOGFLOW_LANGUAGE_CODE = 'ru-RU'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('ga-key-admin')


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

    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    response = requests.get(url).json()

    for key, item in response.items():
        display_name = key
        training_phrases_parts = item['questions']
        message_texts = [item['answer']]

        create_intent(
            project_id=DIALOGFLOW_PROJECT_ID,
            display_name=display_name,
            training_phrases_parts=training_phrases_parts,
            message_texts=message_texts
        )
