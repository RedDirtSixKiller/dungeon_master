from openai import OpenAI
import config
client = OpenAI(api_key=config.openai_key)



# the main workhorse
def get_completion(prompt, model='gpt-3.5-turbo'):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature=0)
    return response.choices[0].message.content


# chars should come from the character class
# need to write a class for the action - probably with a sub action for attacks?
char1 = 'Daisy the drow elf'
char2 = 'Hokar the half-orc'
act = 'uses a bow to shoot'

prompt = f"""
Your task is to act as a dungeon master describing a combat action in dungeons and dragons.\
 Write a narrative where the characters' information is delimited by <char></char>\
 and the action is delimited by <act></act>

 Action: <char>{char1}</char> <act>{act}</act> <char>{char2}</char>
"""

# uncommenting here will cost money, not much but it isn't free
# response = get_completion(prompt)
# print(response)