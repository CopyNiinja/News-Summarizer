from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas, dependencies, scraper

router = APIRouter(
    prefix="/news",
    tags=["news"],
)

@router.get("/", response_model=List[schemas.News])
def read_news_list(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    """
    Return all news from the database.
    """

    news_list = crud.get_news_list(db=db, skip=skip, limit=limit)
    if news_list is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news_list
    


@router.get("/{news_id}", response_model=schemas.News)
def read_news(news_id: int, db: Session = Depends(dependencies.get_db)):
    news = crud.get_news(db, news_id=news_id)

    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.post("/scrape/")
def scrape_news(homepage_url: str, db: Session = Depends(dependencies.get_db)):
    return scraper.scrape_and_store_homepage_news(homepage_url, db)
     
