
import os
import requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
import pandas as pd
import pickle
import threading
import time
from movie_linking import split_title_and_year, linking

# In[全域變數與函數]:

main_page = 'https://www.imdb.com/title/' # IMDB網域名稱/title/
header_example = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
default_poster = 'https://m.media-amazon.com/images/G/01/imdb/images/social/imdb_logo.png'

def RW_ClassObj(obj=None, write=True, dir_name='temp/', name='var', date='', batch = ''):
    if date:
        dir_name += date+'/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if batch:
        name += '_'+str(batch)
    if write:
        with open(dir_name+name, 'wb') as file:
            pickle.dump(obj, file)
    else:
        with open(dir_name+name, 'rb') as file:
            obj = pickle.load(file)
        return obj

# In[IMDb_crawler類別]:

class IMDb_crawler:
    def __init__(self, idlist):
        self.imdbId_list = idlist
        self.n = len(self.imdbId_list)
        self.name_zhtw = ['']*self.n
        self.years = ['']*self.n
        self.genres = ['']*self.n
        self.grades = ['']*self.n
        self.posters = ['']*self.n # 部分電影可能共用預覽圖(非default_poster), 這是IMDb網站的問題, 與爬蟲程式無關

    def reload_var(self, num):
        self.name_zhtw = RW_ClassObj(write=False, name='name_zhtw', batch=num)
        self.genres = RW_ClassObj(write=False, name='grades', batch=num)
        self.grades = RW_ClassObj(write=False, name='grades', batch=num)
        self.posters = RW_ClassObj(write=False, name='posters', batch=num)

    def save_var(self, num):
        RW_ClassObj(obj=self.name_zhtw, write=True, name='name_zhtw', batch=num)
        RW_ClassObj(obj=self.genres, write=True, name='genres', batch=num)
        RW_ClassObj(obj=self.grades, write=True, name='grades', batch=num)
        RW_ClassObj(obj=self.posters, write=True, name='posters', batch=num)

    def isfloat(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def idx_of_last_left_parenthesis(self, s):
        for i in range(len(s)-1, -1, -1):
            if s[i] == '(':
                return i
        return -1

    def crawl_IMDb(self, i, show_text=False): # 子執行緒的工作函數, 注意無法return
        url = main_page+self.imdbId_list[i]
        request = requests.get(url, headers=header_example, timeout=10)
        html = BeautifulSoup(request.text, 'html.parser')
        links = html.find_all('meta')
        text, img = '', ''
        for link in links:
            if 'property' in link.attrs:
                if link.attrs['property'] == 'og:title':
                    text = link.attrs['content']
                if link.attrs['property'] == 'og:image':
                    img = link.attrs['content']
        if len(text) == 0:
            return
        if show_text:
            print(i+1, '-th catched', sep='')
        parts = text.split('|')
        self.name_zhtw[i], self.years[i] = split_title_and_year(parts[0])
        tail = -2 if parts[0][-1] == ' ' else -1
        if self.isfloat(parts[0].split(' ')[tail]):
            self.grades[i] = parts[0].split(' ')[tail]
        else:
            self.grades[i] = '0'
        if len(parts) > 1:
            self.genres[i] = parts[1].replace(' ', '').replace(',', '|')
        else:
            self.genres[i] = '(no genres listed)'
        self.posters[i] = img
        if show_text:
            print('  ', self.name_zhtw[i], self.years[i], self.grades[i], self.genres[i], self.posters[i] != default_poster)

    def threading_crawler(self, idxlist, show_text=False):
        for i in idxlist:
            self.crawl_IMDb(i, show_text)
            time.sleep(1)

    def crawl_threads(self, begin, batch_size, thread_count, target_idx=[], show_text=False):
        threads = []
        if not target_idx:
            target_idx = list(range(self.n))
        start_t = time.time()
        for i in range(thread_count): # 建立15個子執行緒
            start = begin+i*batch_size
            end = start+batch_size
            threads.append(threading.Thread(target=self.threading_crawler, args=(target_idx[start:end], show_text)))
            threads[i].start()
        for j in range(thread_count): # 等待所有子執行緒結束
            threads[j].join()
        end_t = time.time()
        print('Done, duration =', end_t-start_t, 'sec.')

    def check_missing(self): # 檢查遺漏項
        return [i for i in range(self.n) if not self.name_zhtw[i] or not self.posters[i]]

    def get_result(self):
        return self.name_zhtw, self.years, self.genres, self.grades, self.posters

# In[main]:

if __name__ == "__main__":
    linking() # 合併movies.csv, links.csv
    movies = pd.read_csv('movies_linked.csv', sep = ',') # 62423部電影
    imdbId_list = list(movies['imdbId'])
    crawler = IMDb_crawler(imdbId_list)
    crawler.crawl_threads(begin = 0, batch_size = 41, thread_count = 10, show_text = True)
    name_zhtw, years, genres, grades, posters = crawler.get_result()

# In[]:

#   movies['name_zhtw'] = name_zhtw
    movies['year'] = years
    movies['genres'] = genres
    movies['grade'] = grades
    movies['picture'] = posters
    """
    未上映
      tt7335008 (2024)
    """
    movies[movies['imdbId'] == 'tt7335008']['year'] = '2024'
    movies.to_csv('movies_extended.csv', index = False, header = True)

