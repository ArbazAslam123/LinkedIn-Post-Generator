from llm_helper import llm
from few_shot import fewShotPosts


few_shot = fewShotPosts()
def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "6 to 10 lines"
    elif length == "Long":
        return "11 to 15 lines"

def get_prompt(length, language, tag):
    length_str = get_length_str(length)
    prompt = f'''
    Generate a LinkedIn post about the using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If the Language is Urdu, then write the post in Roman Urdu.
    The script for the generated post should always be English.
    '''
    length_lower = length.lower()
    example = few_shot.get_filtered_posts(length=length_lower, language=language, tag=tag)
    if len(example) > 0:
        prompt += "4) Use the writing style as per the folowing examples."
        for  i, post in enumerate(example):
            post_test= post['text']
            prompt += f"\n\nExample {i + 1}:\n{post_test}"

            if i == 1:  # Limit to 3 examples
                break
    return prompt


def generate_post(tag, length, language):
    prompt = get_prompt(length, language, tag)

    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    post = generate_post(tag="Automation", length="medium", language="English")
    print(post)