import pandas as pd
from groq import Groq

client = Groq(
    api_key="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",
)

testData = pd.read_csv('testData.csv')
categorizedKeywords = pd.read_csv('categorized_keywords.csv')
keywords = testData['Keyword']
categories = testData['Categories']

with open('keywords_filtering.txt', 'r') as file:
    google_policies = file.read()

# Removing NaN values from array
categories = [x for x in categories if x == x]


def categorize_keyword(keyword):
    # Create AI request
    prompt = f"Assign the following keyword to one of these categories: {', '.join(categories)}.\nKeyword: {keyword}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system",
             "content": "You are a management assistant, skilled in categorizing keywords. You answer with category type only."},
            {"role": "user", "content": prompt}
        ]
    )
    category = response.choices[0].message.content
    print(keyword, category)
    return category


def categorize_all_keywords():
    # Categorize each keyword
    testData['Categories'] = keywords.apply(categorize_keyword)

    # Save to a new CSV file or Google Sheet
    testData.to_csv('categorized_keywords.csv', index=False)


# categorize_all_keywords()


def get_commercial_potential():
    for index, row in testData.iterrows():
        categorizedKeywords.loc[index, 'Commercial Potential'] = (
                int(row['Search Volume (US)']) *
                float(row['CPC (US)'][1:])
        )

    categorizedKeywords.to_csv('categorized_keywords.csv', index=False)


# get_commercial_potential()


def sort_by_commercial_potential():
    sorted_keywords = categorizedKeywords.sort_values(by='Commercial Potential', ascending=False)
    sorted_keywords.to_csv('categorized_keywords.csv', index=False)


# sort_by_commercial_potential()


def filter_keyword(keyword):
    filter_keyword.counter += 1
    # Create AI request
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system",
             "content": "You are a skilled assistant, skilled in filtering keywords according to rules.\n"
                        "You need to find keywords that are:\n"
                        "Related to ecommerce and likely to return searches on our sites (alwaysreview.shop, dealday.today etc).\n"
                        "Non-branded (for now)\n"
                        "Not in violation of any of google’s policies:\n"
                        f"{google_policies}"
             },
            {"role": "user", "content": f"Filter the following keyword - '{keyword}'\n Answer only PASSED or FAILED"}
        ],
        temperature=0
    )
    filter_status = response.choices[0].message.content
    print(filter_keyword.counter, keyword, '-', filter_status)
    return filter_status


filter_keyword.counter = 0


def filter_all_keywords():
    categorizedKeywords['Filtering'] = categorizedKeywords['Keyword'].apply(filter_keyword)

    categorizedKeywords.to_csv('categorized_keywords.csv', index=False)


# filter_all_keywords()
