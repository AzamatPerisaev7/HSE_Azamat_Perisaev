import re
import json

def find_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

with open('1000_efrsb_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

emails_dict = {}

for message in data:
    inn = message['publisher_inn']
    text = message['msg_text']
    emails = set(find_emails(text))
    emails_dict.setdefault(inn, set()).update(emails)
    print(emails_dict)

for inn in emails_dict:
    emails_dict[inn] = list(emails_dict[inn])
    
with open('emails.json', 'w', encoding='utf-8') as f:
    json.dump({'emails': emails_dict}, f, indent=2, ensure_ascii=False)