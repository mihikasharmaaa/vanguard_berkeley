from newspaper import Article

url = 'https://web.archive.org/web/20220122072147/https://www.sfchronicle.com/health/article/UCSF-scientists-detect-fluid-anomolies-in-people-16784623.php'
article = Article(url)
article.download()
article.parse()
print(article.text)

