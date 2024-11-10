from langchain_core.prompts import PromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session
from connection import get_db
from models import Article
from settings import settings

class Search:
    def __init__(self):
        self.db = get_db()

    async def save_articles(
        self,
        user_id: int, 
        article_data: dict,
        db: Session  # Pass db as a parameter
    ):
        # Insert the article in the database in the background
        article = Article(
            title=article_data['title'],
            extract=article_data['extract'],
            keyword=article_data['keyword'],
            tags=', '.join(article_data['tags']),
            user_id=user_id
        )

        db.add(article)
        db.commit()

    async def get_article_from_wikipedia(self, keyword):
        url = settings.wikipedia_api_url
            
        # Step 1: Search for page IDs
        search_params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'utf8': 1,
            'srsearch': keyword,
            'srlimit': 1 # Adjust to number of results you want
        }
        search_response = requests.get(url, params=search_params)
        search_data = search_response.json()
        
        if "query" not in search_data:
            raise HTTPException(status_code=404, detail="No articles found")
        
        # Extract page IDs from the search results
        page_ids = [str(result['pageid']) for result in search_data['query']['search']]
        page_ids_str = "|".join(page_ids)  # Concatenate page IDs with '|'

        # Step 2: Fetch extracts based on page IDs
        extract_params = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'pageids': page_ids_str,
            'exintro': True,  # Only get the introduction section
            'explaintext': True  # Return plain text, no HTML
        }
        extract_response = requests.get(url, params=extract_params)
        extract_data = extract_response.json()

        return extract_data

        


    async def generate_tages(self, title, extract):

        prompt = PromptTemplate(template="Analyze the following Wikipedia article excerpt and generate the five most relevant tags or keywords that summarize its main topics, themes, and concepts. Provide the tags in a single comma-separated list without additional formatting: {input}")
        formatted_prompt = prompt.format(input=extract) 

        # Initialize the model and output parser
        llm = ChatGoogleGenerativeAI(model=settings.llm_model, api_key=settings.llm_api_key)
        parser = StrOutputParser()

        # Invoke the model with the formatted prompt string
        result = llm.invoke(formatted_prompt)
        parsed_result = parser.parse(result) 
        tags = parsed_result.content

        # Clean and split tags
        clean_tags = [tag.strip().title() for tag in tags.split(",") if tag.strip()]  # Strip whitespace, title case, and remove empty entries

        return clean_tags

