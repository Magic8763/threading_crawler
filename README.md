# Threading Crawler
![](https://img.shields.io/github/stars/magic8763/threading_crawler)
![](https://img.shields.io/github/watchers/magic8763/threading_crawler)
![](https://img.shields.io/github/forks/magic8763/threading_crawler)

採用多執行緒加速網頁爬蟲，以 IMDb 網站為例。

## Prerequisites
- Python3, Requests, Beautifulsoup4, Pandas

## Description
- `movie_linking.py`: 整合電影特徵資料集與 IMDb 主頁索引
- `IMDb_crawler.py`: 基於每部電影的主頁索引，以 Python Threading 模組同時爬取複數網頁內容

## Dataset
- [MovieLens 25M](https://grouplens.org/datasets/movielens/25m) 其中的 `movies.csv` 和 `links.csv` 兩個電影特徵資料集
  - `movies.csv`: 包含 62423 部相異電影，每部電影具有 movieId, title, genres 等特徵（部分有誤或缺漏）
  - `links.csv`: 每部電影分別對應的 IMDb 主頁索引

## Output
- `movies_extended.csv`: 保留 `movies.csv` 和 `links.csv` 的原始特徵，再追加 year, genres, grade, picture 等新特徵

## Authors
* **[Magic8763](https://github.com/Magic8763)**

## License
This project is licensed under the [MIT License](https://github.com/Magic8763/threading_crawler/blob/main/LICENSE)
