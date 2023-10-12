# Threading Crawler
採用多執行緒加速網頁爬蟲，以IMDb網站為例

## Prerequisites
- Python3, Requests, Beautifulsoup4, Pandas, Pickle

## Description

下載 [MovieLens 25M](https://grouplens.org/datasets/movielens/25m) 其中的 movies.csv 和 links.csv。
- movies.csv: 62423 部電影的特徵資料集，每部電影包含 movieId, title, genres 等特徵（部分有誤或缺漏）
- links.csv: 62423 部電影對應的 IMDb 主頁索引

**Program**
- movie_linking.py: 合併 movies.csv, links.csv 兩資料集
- IMDb_crawler.py: 基於每部電影的 IMDb 主頁索引爬取 year, genres, grade, poster 等新特徵

## Authors
* **Chih-Chien Cheng** - (categoryv@cycu.org.tw)
