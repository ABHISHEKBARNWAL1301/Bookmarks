from models import Article, User
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from connection import get_db
from .search import Search
import asyncio
from auth import get_current_user



search = Search()


CrudRoute = APIRouter(tags=["CRUD Operations"])


# Step 1: Searching Wikipedia
@CrudRoute.get("/search/{keyword}")
async def search_wikipedia(
    keyword: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    # Check if articles for this keyword already exist for the current user
    existing_articles = db.query(Article).filter(Article.keyword == keyword, Article.user_id == current_user.userid).all()
    
    article_data = []
    tag_tasks = []

    if existing_articles:
        for article in existing_articles:
            article_dict = article.__dict__.copy()
            article_dict.pop("user_id", None)
            article_dict["tags"] = article_dict["tags"].split(", ")
            article_data.append(article_dict)
        return article_data

    article = await search.get_article_from_wikipedia(keyword)
    
    for page_id, page_data in article['query']['pages'].items():
        title = page_data.get('title')
        extract = page_data.get('extract')

        # Prepare the task for concurrent execution
        tag_tasks.append(search.generate_tages(title, extract))
        
        # Append other data to results immediately (tags will be added later)
        article_data.append({
            'articleid': page_id,
            'title': title,
            'extract': extract,
            'keyword': keyword,
            # 'tags' will be added after asyncio.gather resolves
        })
    
    # Run all generate_tags calls concurrently
    tags_list: List[List[str]] = await asyncio.gather(*tag_tasks)
    
    # Insert generated tags into the article_data
    for i, tags in enumerate(tags_list):
        article_data[i]['tags'] = tags
    
    
    user = db.query(User).filter(User.username == current_user.username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    # Save the article data in the background task
    for data in article_data:
        background_tasks.add_task(search.save_articles, user.userid, data, db)
    
  
    return article_data




# Step 2: List all articles for a user
@CrudRoute.get("/list_articles")
async def list_articles_for_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Retrieve all articles for the user
    articles = db.query(Article).filter(Article.user_id == current_user.userid).all()
    # breakpoint()

    article_data = []
    for article in articles:
        article_dict = article.__dict__.copy()  # Get dictionary representation
        article_dict.pop("user_id", None)       # Remove 'user_id'
        article_dict["tags"] = article_dict["tags"].split(", ")
        article_dict["articleid"] = str(article_dict["articleid"])
    
        article_data.append(article_dict)
    
    return article_data




# Step 3: Edit tags for an article for a user
@CrudRoute.put("/edit_tags/{articleid}")
async def edit_tags_for_article(
    articleid: int, 
    new_tags: List[str], 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = db.query(Article).filter(Article.articleid == articleid, Article.user_id == current_user.userid).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article.tags = ', '.join(new_tags)  # Store tags as a comma-separated string
    db.commit()

    return {"status": "success", "message": "Tags updated successfully"}
