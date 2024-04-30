
import pandas as pd

def fix_the_problem(s):
    parts = s.split('(')
    s = parts[0]
    while s and s[-1] == ' ':
        s = s[:-1]
    if s[-5:] == ', The': # 將'title, The'修正為'The title'
        s = 'The '+s[:-5]
    if len(parts) == 2:
        s += ' ('+parts[1]
    s = s.replace('“', '"') # 統一雙引號
    s = s.replace('”', '"')
    return s

def split_title_and_year(s, fixed = False): # 分割片名與年份
    n = len(s)
    for left in range(n-1, -1, -1):
        if s[left] == '(':
            year = ''
            for c in s[left+1:]:
                if c.isdigit():
                    year += c
                if len(year) == 4 and year[0] in ('1', '2'):
                    s = s[:left]
                    while s and s[-1] == ' ':
                        s = s[:-1]
                    if fixed:
                        s = fix_the_problem(s)
                    return [s, year]
            break
    if fixed:
        s = fix_the_problem(s)
    return [s, 'unknown']

def linking():
    movies = pd.read_csv('ml-25m/movies.csv', sep = ',') # 62423部電影, 原始genres欄位有誤
    movies[['title', 'year']] = movies['title'].apply(lambda x: pd.Series(split_title_and_year(x, True)))
    movies['letters'] = movies['title'].apply(lambda x: x.lower().replace(' ', ''))
    movies = movies[['movieId', 'title', 'letters', 'year']] # 分割後year欄位仍有缺漏

    links = pd.read_csv('ml-25m/links.csv', sep = ',')
    """
    IMDb主頁變動如下
      tt3416042 -> tt3411580
      tt0118114 -> tt2185063
      tt1347439 -> tt2585208
      tt3762944 -> tt12944538
      tt5640954 -> tt28362963
    """
    links[links['imdbId'] == 3416042]['imdbId'] = 3411580
    links[links['imdbId'] == 118114]['imdbId'] = 2185063
    links[links['imdbId'] == 1347439]['imdbId'] = 2585208
    links[links['imdbId'] == 3762944]['imdbId'] = 12944538
    links['imdbId'] = links['imdbId'].apply(lambda x: 'tt'+str(x).zfill(7))
    new_movies = movies.merge(links[['movieId', 'imdbId']], on='movieId', how='left')
    new_movies.to_csv('movies_linked.csv', index = False, header = True)