from playwright.sync_api import (
  sync_playwright, BrowserContext,
  Page, Browser,
)
from faker import Faker


class CookiesLoader:
  def __init__(self, url: str, user_agent: str = None, headless: bool = True) -> None:
    self.url = url
    self.user_agent = user_agent
    self.headless = headless
    self.cookies = []
    
    if not user_agent:
      self.user_agent = Faker().user_agent()

  def load(self) -> None:
    with sync_playwright() as playwright:
      browser: Browser = playwright.webkit.launch(headless=self.headless)
      context: BrowserContext = browser.new_context(user_agent=self.user_agent)
      page: Page = context.new_page()
      page.goto(self.url)
      page.wait_for_load_state('networkidle')
      self.cookies = context.cookies()

      cookie: dict
      for cookie in self.cookies:
        if cookie.get('name') == '__cf_bm':
          break
      else:
        raise Exception('__cf_bm cookie not found')


loader = CookiesLoader('https://platform.nexo.io/')
loader.load()

cookie: dict
for cookie in loader.cookies:
  print(cookie.get('name'), cookie.get('value'))
