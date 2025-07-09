from keybert import KeyBERT
import asyncio

kw_model = KeyBERT(model="all-MiniLM-L6-v2")

async def fetch_keywords(user_query: str):
    keywords = kw_model.extract_keywords(user_query, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
    return [i[0] for i in keywords]
    

# Example usage
if __name__ == "__main__":
    result = asyncio.run(fetch_keywords("aRTIFICIAL INTELLIGENCE"))
    #t = list(result.split(" "))
    print("Extracted keywords:", result)