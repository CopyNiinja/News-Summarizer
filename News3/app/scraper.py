import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from .database import SessionLocal
from .crud import create_news
from .schemas import NewsCreate, News



def scrape_single_page_selenium(url: str, db: SessionLocal):
  
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    try:
        driver.get(url)
       
        title = driver.find_element(By.TAG_NAME, 'h1').text
        print("Title: ", title)

        try:
            reporter = driver.find_element(By.CLASS_NAME, 'contributor-name').text
        except:
            reporter = "প্রতিনিধি"
        print("Reporter: ", reporter)

        # reporter_location = driver.find_element(By.CLASS_NAME, 'author-location').text
        # print("Reporter Location: ", reporter_location)

        datetime_element = driver.find_element(By.TAG_NAME, 'time')
        datetime_str = datetime_element.get_attribute('datetime')
        news_datetime = datetime.datetime.fromisoformat(datetime_str)
        print("Datetime attribute: ", news_datetime)

        try:
            category = driver.find_element(By.CLASS_NAME, 'print-entity-section-wrapper').text
        except:
            category = "সাধারণ"
        print("Category: ", category)

        news_body = '\n'.join([p.text for p in driver.find_elements(By.CSS_SELECTOR, 'div.story-element.story-element-text p')])
        print("News Body: ", news_body)

        img_tags = driver.find_elements(By.CSS_SELECTOR, 'picture.qt-image:not(.default) img')
        print("Number of images: ", len(img_tags))
        images = [img.get_attribute('src') for img in img_tags if img.get_attribute('src')]
        print("Images: ", images)

        publisher_website = driver.current_url.split('/')[2]
        publisher = publisher_website.split('.')[-2]
        print("Publisher: ", publisher)
        db = SessionLocal()
        news_data = NewsCreate(
            publisher_website=publisher_website,
            news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=news_body,
            images=images,
        )
        print(news_data)
        
        inserted_news = ""
        if news_data:
            inserted_news = create_news(db=db, news=news_data)
        db.close()

        return inserted_news
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def scrape_homepage_selenium(homepage_url: str):
 
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    news_links = []
    try:
        driver.get(homepage_url)
        news_elements = driver.find_elements(By.CSS_SELECTOR, 'a.title-link')
        for element in news_elements:
            title = element.text
            link = element.get_attribute('href')
            news_links.append((title, link))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    return news_links

def scrape_and_store_homepage_news(homepage_url: str, db: SessionLocal):
  
    all_news = []
    news_links = scrape_homepage_selenium(homepage_url)
    print(f"Found {len(news_links)} news links.")

    for title, link in news_links:
        print(f"\nScraping news page: {title}")
        x=scrape_single_page_selenium(link, db)
        all_news.append(x)
    return all_news