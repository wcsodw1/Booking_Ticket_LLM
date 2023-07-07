
# python Choose_Best_TicketPrice.py

# A.Import neccessary package and OpenAI API Tool
import pandas 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_extraction_chain

OPENAI_API_KEY = "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"
OPENAI_LLM = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key = OPENAI_API_KEY)
Ticket_Website = "https://www.expedia.com.tw/Flights-Search?leg1=from%3A%E5%8F%B0%E5%8C%97%20%28TPE-%E6%A1%83%E5%9C%92%E5%9C%8B%E9%9A%9B%E6%A9%9F%E5%A0%B4%29%2Cto%3A%E6%9B%BC%E8%B0%B7%20%28BKK%20-%20%E7%B4%A0%E8%90%AC%E9%82%A3%E6%99%AE%E5%9C%8B%E9%9A%9B%E6%A9%9F%E5%A0%B4%29%2Cdeparture%3A2023%2F7%2F12TANYT&leg2=from%3A%E6%9B%BC%E8%B0%B7%20%28BKK%20-%20%E7%B4%A0%E8%90%AC%E9%82%A3%E6%99%AE%E5%9C%8B%E9%9A%9B%E6%A9%9F%E5%A0%B4%29%2Cto%3A%E5%8F%B0%E5%8C%97%20%28TPE-%E6%A1%83%E5%9C%92%E5%9C%8B%E9%9A%9B%E6%A9%9F%E5%A0%B4%29%2Cdeparture%3A2023%2F7%2F13TANYT&mode=search&options=carrier%3A%2A%2Ccabinclass%3A%2Cmaxhops%3A1%2Cnopenalty%3AN&pageId=0&passengers=adults%3A1%2Cchildren%3A0%2Cinfantinlap%3AN&trip=roundtrip"


# B.crawler_flightdataby_LLM
def crawler_flightdataby_LLM(OPENAI_API_KEY,OPENAI_LLM):
    
    # 1.Craw data from website and using beautiful soup filter data
    s = Service('./chromedriver')
    driver = webdriver.Chrome(service = s)
    driver.get(Ticket_Website)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # soup.text
    
    #2.Design Agent(Langchain) mission(Dictionary) by setting the customize schema 
    schema = {
        "properties": {
            "flight": {"type": "string"},
            "departure_time": {"type": "string"},
            "departure_terminal": {"type": "string"},
            "flight_hour": {"type": "string"},
            "flight_type": {"type": "string"},
            "arrival_time": {"type": "string"},
            "arrival_terminal": {"type": "string"},
            "price": {"type": "string"},
            "flight_type": {"type": "string"},
        }
    }

    # 3.Extract data using OPENAI API and show data by df 
    chain = create_extraction_chain(schema, OPENAI_LLM)
    flight_data = chain.run(soup.text)
    df = pandas.DataFrame(flight_data)
    df.to_csv('ticket_out.csv', index=False)
    print(df)
    
crawler_flightdataby_LLM(OPENAI_API_KEY,OPENAI_LLM)
