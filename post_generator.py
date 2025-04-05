from llm_helper import llm
from few_shot import FewShotPosts
import random
import spacy  # Import spaCy

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

few_shot = FewShotPosts()

# Define emojis based on tags
EMOJI_MAP = {
    "mental health": ["🧠", "💙", "🌿", "🧘", "💆‍♂️"],
    "stress": ["😓", "💆‍♂️", "🕊️", "😩", "🤯"],
    "yoga": ["🧘", "☯️", "🕉️", "💪", "🌞"],
    "motivation": ["🔥", "🚀", "💪", "🌟", "💡"],
    "success": ["🏆", "🎯", "🌟", "💰", "📈"],
    "job search": ["📄", "💼", "🔍", "💪", "🤞"],
    "linkedin": ["💼", "📢", "📱", "👥", "🌐"],
    "influencer": ["🎤", "💡", "📱", "🔝", "📢"],
    "online dating": ["💘", "💔", "💬", "😅", "😂"],
    "scams": ["⚠️", "🚨", "💸", "😡", "🤦‍♂️"],
    "self improvement": ["📚", "💡", "🎯", "✨", "🚀"],
    "career advice": ["💼", "📈", "📊", "📝", "🤝"],
    "rejection": ["😔", "💔", "🔄", "💪", "🌱"],
    "toxic work environment": ["💀", "⚠️", "😡", "🚪", "🛑"]
}

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def add_emojis_to_post(text, tags):
    """Add relevant emojis based on tags."""
    emojis = []
    for tag in tags:
        if tag.lower() in EMOJI_MAP:
            emojis.extend(EMOJI_MAP[tag.lower()])  # Collect emojis for all matching tags
    if emojis:
        text += " " + " ".join(random.sample(emojis, min(2, len(emojis))))  # Add 2 random emojis
    return text

def extract_keywords_and_hashtags(text, length):
    """Extracts key topics from a given text using spaCy and generates relevant hashtags based on post length."""
    doc = nlp(text)

    # Extract named entities (Organizations, Locations, Technologies, etc.)
    keywords = {ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE", "EVENT", "WORK_OF_ART"]}

    # Extract important nouns (avoid very short words)
    keywords.update({token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 3})

    # Convert keywords to hashtags, removing duplicates
    hashtags = {f"#{word.replace(' ', '')}" for word in keywords}

    # Define hashtag limits based on post length
    length_hashtag_map = {
        "Short": 3,   # 2-3 hashtags
        "Medium": 7,  # 6-8 hashtags
        "Long": 12    # 10-14 hashtags
    }

    max_hashtags = length_hashtag_map.get(length, 5)  # Default to 5 if length is unknown

    return list(hashtags)[:max_hashtags]  # Limit hashtags based on length

def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    post_text = response.content.strip()  # Ensure no trailing spaces or extra lines

    # Add emojis to the generated post
    post_text = add_emojis_to_post(post_text, [tag])

    # Generate relevant hashtags based on post length
    hashtags = extract_keywords_and_hashtags(post_text, length)

    # Avoid duplicate hashtags by checking if they already exist in post_text
    existing_hashtags = set(word for word in post_text.split() if word.startswith("#"))
    new_hashtags = [tag for tag in hashtags if tag not in existing_hashtags]

    if new_hashtags:
        post_text += "\n\n" + " ".join(new_hashtags)  # Append only unique hashtags

    return post_text

def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1:  # Use max two samples
            break

    return prompt

if __name__ == "__main__":
    print(generate_post("Short", "English", "Job Search"))
