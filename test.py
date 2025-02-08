from openai import OpenAI
import pandas as pd
import random

random.seed(42)
API_KEY = 'sk-4da11687a4f84c3b96405cc4b136ce67'


def data_load():
    test_df = pd.read_csv('data/test.csv')
    submission_df = pd.read_csv('data/sample_submission.csv')
    test_topic = []
    submission_topic = []
    for id, topic in test_df.values:
        test_topic.append({
            'id': id,
            'topic': topic
        })
    for id, topic in submission_df.values:
        submission_topic.append({
            'id': id,
            'topic': topic
        })
    return test_topic, submission_topic


def response_question(prompt):
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"{prompt}"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)


def prompt_produce(topics):
    for t in topics:
        id = t["id"]
        topic = t["topic"]

        prompt = f"{topic}"
        answer = response_question(prompt)


if __name__ == '__main__':
    test_topic, submission_topic = data_load()
