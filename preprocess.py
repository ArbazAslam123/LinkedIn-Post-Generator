from itertools import chain
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm


def process_posts(raw_file_path, linkedin_file_path, processed_file_path="data/processed_post.json"):
    enriched=[]
    with open(raw_file_path, encoding ="utf-8") as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata= post | metadata
            enriched.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched)

    for post in enriched:
        current_tags = post['tags']
        new_tags= {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding="utf-8", mode="w") as file:
        json.dump(enriched, file, ensure_ascii=False, indent=4)

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])   

    unique_tags_list = ', '.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list.
        Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search".
        Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation".
        Example 3: "Personal Growth", "personal Development", "Self Improvement can be mapper to "Personal Development".
        Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "scams"
    2. Output should be a JSON object,No premable
    3. Each tag should be follow title case convention, i.e. : "Motivation", "Job Search"
    4. Output should have mapping of original tag and the unified tag.
        For Example: {{"jobseekers": "Job Search", "Job Hunting": "Job Search", "Motivation": "Motivation"}}

    Here is the list of tags:
    {tags}    
    '''     

    pt = ChatPromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"tags": str(unique_tags_list)})

    json_parser = JsonOutputParser()
    content = response.content
    if not isinstance(content, str):
        content = json.dumps(content)

    res = json_parser.parse(content)
    
    return res  

def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, Language of the post andatags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, langauge and tags.
    3. tags is an array of text tags, Extract minimum two tags.
    4. Langauge should be in English or Urdu (Should be Roman Urdu) 
    
    here is the actual post on which you need to perform this task:
    {post}
    '''

    pt = ChatPromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"post": post})

    json_parser = JsonOutputParser()
    content = response.content
    if not isinstance(content, str):
        content = json.dumps(content)

    res = json_parser.parse(content)
    
    return res  
    

if __name__ == "__main__":
    process_posts("D:\\NextGen Internship Task\\AI ML Learning\\LinkedIn Post Generator\\data\\linkedin_feed_data.json", "D:\\NextGen Internship Task\\AI ML Learning\\LinkedIn Post Generator\\data\\processed_post.json")
    


