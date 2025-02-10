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


def response_question(system_prompt, user_prompt):
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_prompt}"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content


def prompt_produce(topic):
    topic_word = topic["topic"]
    system_prompt = "You are a professor writer with expertise in producing essays"
    user_prompt = \
        (f"Now, you should produce an essay about the topic: {topic_word} "
         f"Your writing should demonstrate critical thinking, logical structure, and academic rigor."
         f"Please create a series of essays on the topics provided, ensuring clarity, depth, and precision in your arguments. "
         f"The essay should be approximately 100 words, include an introduction, body paragraphs, and a conclusion. ")
    return system_prompt, user_prompt


if __name__ == '__main__':
    test_topic, submission_topic = data_load()
    for topic in test_topic:
        id = topic['id']
        system_prompt, user_prompt = prompt_produce(topic)
        result = response_question(system_prompt, user_prompt)
        topic['result'] = result
    print(test_topic)
