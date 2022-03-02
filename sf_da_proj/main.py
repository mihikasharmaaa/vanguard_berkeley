from newspaper import Article
 
url = "https://www.bloomberg.com/news/articles/2020-08-01/apple-buys-startup-to-turn-iphones-into-payment-terminals?srnd=premium"
 
# download and parse article
article = Article(url)
article.download()
article.parse()
 
# print article text
print(article.text)