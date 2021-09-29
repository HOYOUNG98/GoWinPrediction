# WinRatePredictionGoGames

This is my mini project on building a ML model for Go Games win predictor. Nowadays, win predictor using AI is ubiquitous. Sports like baseball, soccer, has many projects involved with ML. However, Go does not have many updates after advent of AI. AlphaGo could be considered possibly the first and last AI product that has impacted Go industry. I wanted to apply my ML knowledge on Go industry, which is why I decided to build this project.

### Project Workflow

I have scraped info from http://m.baduk.or.kr an official Korean Go website. In crawl directory, my work on scraping can be found. I used Selenium to crawl and used DataFrame from Pandas to store my data into csv files. After data acquisition, I have proecessed data and you can see my proecces in dataProcessing.ipynb. I created my own features, considering what would be really needed. Lastly, after processing all data, I have applied it to 3 models to see the best fit.
