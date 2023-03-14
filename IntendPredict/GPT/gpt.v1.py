import openai

OPENAI_KEY = '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'

openai.api_key = OPENAI_KEY


def ChatGPTCompletionRaw(prompt, model="gpt-3.5-turbo"):

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    ret = completion.choices[0].message.content.strip()

    print(ret)

    return ret


