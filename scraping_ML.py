import json
import pandas as pd
from collections import defaultdict
import spacy

nlp = spacy.load("es_core_news_sm")

with open('dataset_fbgroups111.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
truck_type_keywords = ['camioneta', 'trailer', 'caja seca', 'plataforma', 'camión', 'remolque', 'furgón', 'volquete', 'cisterna']

def extract_routes_and_truck_types(text):
    doc = nlp(text.lower())
    cities = [ent.text for ent in doc.ents if ent.label_ == "LOC"]
    truck_types = [token.text for token in doc if token.text.lower() in truck_type_keywords]
    
    routes = []
    if len(cities) >= 2:
        for i in range(len(cities) - 1):
            routes.append(f"{cities[i]} to {cities[i + 1]}")
    
    return routes, truck_types

def extract_text_data(data):
    posts = []
    users = []
    for entry in data:
        post_text = entry.get('text', '')
        user_name = entry['user'].get('name', '')
        
        if post_text:
            posts.append(post_text)
            users.append(user_name)
        
        for comment in entry.get('topComments', []):
            comment_text = comment.get('text', '')
            if comment_text:
                posts.append(comment_text)
                users.append(comment.get('name', ''))

    return posts, users

texts, users = extract_text_data(data)

user_data = defaultdict(list)

for text, user in zip(texts, users):
    routes, truck_types = extract_routes_and_truck_types(text)
    if routes:
        for route in routes:
            user_data[user].append({'Route': route, 'Truck Types': ', '.join(truck_types)})

final_data = []

for user, entries in user_data.items():
    for entry in entries:
        final_data.append({'User': user, 'Route': entry['Route'], 'Truck Types': entry['Truck Types']})

df = pd.DataFrame(final_data)
df.to_excel('user_routes_analysis222.xlsx', index=False)
print("Analysis complete. Results saved to 'user_routes_analysis.xlsx'")