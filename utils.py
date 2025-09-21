import re

def clean_text(text):
   
    text = re.sub(r'<[^>]*?>', '', text)

    text = re.sub(r'http[s]?://\S+', '', text)

    text = re.sub(r'[^a-zA-Z0-9.,;:\-()\n ]', '', text)
    
    text = re.sub(r'[ ]{2,}', ' ', text)

    text = re.sub(r'\n{2,}', '\n', text)
    
    text = text.strip()
    
    return text
