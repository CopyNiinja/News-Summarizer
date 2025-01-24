from fastapi import FastAPI
import uvicorn

from app.routers import news, summary



app = FastAPI(
    title="ProthomAlo News Summary API",
    version="0.1",
    description="This is the API documentation for News Summary generating by AI . It uses Selenium to scrape news from ProthomAlo and stores them in a database. It also provides endpoints to retrieve the news and summaries.",
    redoc_url="/documentation",
    docs_url="/test",
)

app.include_router(news.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prothom Alo Summary API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8011, reload=True)