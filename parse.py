import requests
from tokens import token_buff


token = token_buff
version = 5.131
count = 30

import requests

def get_count_posts(domainP):
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token':token,
                                'v': version,
                                'domain': domainP,
                                'count': count,
                                # 'post_id':post_id,
                                # 'owner_id':owner_id,
                                # 'need_likes':1,
                            }
                            )
    # Текущий объект
    source_data = response.json()
    # Количество постов
    try:
        count_post = len(source_data['response']['items'])
    except Exception:
        count_post = 1
    return count_post

def get_all_posts_id(domainP):
    response_prepare = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token':token,
                                'v': version,
                                'domain': domainP,
                                'count':count,
                                # 'post_id':post_idP,
                                # 'owner_id':ownerP,
                            }
                            )
    id_list = []
    owner_id_list = []
    for i in range(get_count_posts(domainP)):
        try:
            id_list.append(response_prepare.json()['response']['items'][i]['id'])
            owner_id_list.append(response_prepare.json()['response']['items'][i]['owner_id'])
        except Exception:
            id_list = []
            owner_id_list = []
    return [id_list,owner_id_list]

def days_between(date1,date2):
    import datetime
    unix_date1 = 1677626433
    unix_date2 = 1639685759
    # Преобразование UNIX-даты в объект datetime
    date1 = datetime.datetime.fromtimestamp(unix_date1)
    date2 = datetime.datetime.fromtimestamp(unix_date2)
    # Вычисление разницы между датами
    difference = date1 - date2
    # Извлечение количества дней из разницы
    days_difference = difference.days
    print("Разница в днях:", days_difference)
    return days_difference
    
def get_count_owner_posts(domainP):
    print(domainP)
    post_id_list = get_all_posts_id(domainP)[0]
    print(post_id_list)
    l = get_all_posts_id(domainP)[1]
    try:
        owner_id_list = max(set(l), key=l.count) # Это ебаный костыль!
    except Exception:
        owner_id_list = 0
    print(owner_id_list)
    k = 0
    for i in post_id_list:
        print('post_id '+str(i))
        response = requests.get('https://api.vk.com/method/wall.getComments',
                        params={
                            'access_token':token,
                            'v': version,
                            'domain': domainP,
                            'count':count,
                            'post_id':i,
                            # 'post_id':post_id,
                            # 'owner_id':owner_id
                            'owner_id':owner_id_list
                        }
                        )
        data = response.json()
        if 'response' in data:
            try:
                comments = data['response']['items']
            except Exception:
                comment = {}
            # user_id = owner_id_list  # Идентификатор пользователя, чей комментарий нужно проверить
            user_id = owner_id_list  
            for comment in comments:
                if comment['from_id'] == int(user_id):
                    k = k+1
                    print('Коммент  ' + str(k))
    return k

def get_count_comments(domainP):
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token':token,
                                'v': version,
                                'domain': domainP,
                                'count':count
                            }
                            )
    # Текущий объект
    source_data = response.json()
    main_counter = 0
    for i in range(get_count_posts(domainP)):
        # try:
        main_counter += source_data['response']['items'][i]['comments']['count']
        # if source_data['response']['items'][i]['comments']['text'] != '':
            # main_counter+=1
        # except Exception:
        #     print('Komm ?')
        #     main_counter = 1
    return main_counter

def find_bad_words(domainP):
    print(domainP)
    res_dict = {}
    post_id_list = get_all_posts_id(domainP)[0]
    print(post_id_list)
    l = get_all_posts_id(domainP)[1]
    try:
        owner_id_list = max(set(l), key=l.count) # Это ебаный костыль!
    except Exception:
        owner_id_list = 0
    print(owner_id_list)
    k = 0
    indicator = 0
    bad_word_id_list = []
    for i in post_id_list:
        print('post_id '+str(i))
        response = requests.get('https://api.vk.com/method/wall.get',
                        params={
                            'access_token':token,
                            'v': version,
                            'domain': domainP,
                            'count':count,
                            'post_id':i,
                            # 'post_id':post_id,
                            # 'owner_id':owner_id
                            'owner_id':owner_id_list
                        }
                        )
        data = response.json()
        from dict import bad_word
        text = data['response']['items'][indicator]['text']
        print(text)
        for j in bad_word:
            if j in text:
                print(f"bad word FINDED - {j} in {i}")
                bad_word_id_list.append(i)
        indicator+=1
        # print(indicator)
    res_dict[f'{domainP}'] = bad_word_id_list
    return res_dict
# {'a4': [187863, 11554338, 4588]}
def get_likes_reposts_views(domainP):
    
    # domain = domainP
    token = token_buff
    v = version
    # posts_ids = get_all_posts_id(i)
    res_list = []
    sum_likes = 0
    sum_views = 0
    sum_reposts = 0

    # for i in domain:
    posts_ids = get_all_posts_id(domainP)[0]
    owner_ids = get_all_posts_id(domainP)[1]
    # Формирование URL запроса к API ВКонтакте
    for j,k in zip(posts_ids,owner_ids):
        url = f'https://api.vk.com/method/wall.getById?domain={domainP}&posts={k}_{j}&access_token={token}&v={v}'
        print(url)

        # Отправка запроса и получение данных
        response = requests.get(url)
        data = response.json()

        # Обработка полученных данных
        if 'response' in data and data['response']:
            post = data['response'][0]

            likes = post['likes']['count']
            views = post['views']['count']
            reposts = post['reposts']['count']

            sum_likes+=likes
            sum_views+=views
            sum_reposts+=reposts

            print(f'Лайки: {likes}')
            print(f'Просмотры: {views}')
            print(f'Репосты: {reposts}')
        else:
            print('Не удалось получить информацию о посте.')
        res_list = [sum_likes,sum_views,sum_reposts]
    return res_list
# print(get_likes_reposts_views('hurmyatina'))


# print(find_bad_words(['hurmyatina']))
#{"['hurmyatina']": [417, 394, 370]}

# print(source_data['response']['items'][0]['text'])

#Дата между постами
# date1 = source_data['response']['items'][0]['date']
# date2 = source_data['response']['items'][-1]
# count_days_between = days_between(date1,date2)
# get_count_comments(['a4','hurmyatina'])
# a = {'hurmyatina': [0, 30, 25, 81.064, 448, 11840, 47], 'kisszaya': [1, 4, 23, 16.4601, 1, 1, 1]}

def naebalovo(gdict):
    k = gdict.keys()
    v = gdict.values()
    low = []
    med = []
    hig = []
    res = {}
    for i, j in zip(k, v):
        res[f"{i}"] = j[3]

    max_value = max(res.values())
    sum_values = sum(res.values())
    avg = sum_values / len(res)

    keys_to_remove = []
    for i in res:
        if res[f"{i}"] < avg:
            keys_to_remove.append(i)

    for key in keys_to_remove:
        del res[key]

    print(res)

    return [res,gdict]
# {'hurmyatina': 81.064}

# naebalovo(a)
# domain_list = ['hurmyatina','a4']
def potential(domain_list):

    c_owner = []
    c_posts = []
    c_comments = []
    c_likes = []
    c_reposts = []
    c_views = []
    koefs = []
    # glvr = list(get_likes_reposts_views(domain_list).values())
    main_result = {}

    for i in domain_list:
        
        try:
            count_likes = get_likes_reposts_views(i)[0]
            print(f"Количество лайков - {count_likes}")
        except Exception:
            count_likes = 1
        # c_likes.append(count_likes)

        try:
            count_views = get_likes_reposts_views(i)[1]
            print(f"Количество просмотров - {count_views}")
        except Exception:
            count_views = 1
        # c_views.append(count_views)
        try:
            count_reposts = get_likes_reposts_views(i)[2]
            print(f"Количество репостов - {count_reposts}")
        # c_reposts.append(count_reposts)
        except Exception:
            count_reposts = 1
        try:
            count_owner_comments = get_count_owner_posts(i)
            print(f"Количество ответов от владельца под своим постом - {count_owner_comments}")
        # c_owner.append(count_owner_comments)
        except Exception:
            count_owner_comments = 1
        try:
            count_posts = get_count_posts(i)
            print(f"Количество постов - {count_posts}")
        except Exception:
            count_posts = 1
        # c_posts.append(count_posts)
        try:
            count_comments = get_count_comments(i) 
            print(f"Количество комментов - {count_comments}")
        except Exception:
            count_comments = 1
        # c_comments.append(count_comments)
        sum_koef = count_posts+count_comments*0.5+count_owner_comments*0.25+count_likes*0.01+count_reposts*0.7+count_views*0.0001
        print(f"Числитель - {sum_koef}")
        # koefs.append(sum_koef)
        
        # znamenatel = count_comments+count_owner_comments+count_posts
        # print(f"Знаменатель - {znamenatel}")

        print(f"Потенциал источника - {sum_koef}")
        main_result[f'{i}'] = [count_owner_comments,count_posts,count_comments,sum_koef,count_likes,count_views,count_reposts]

    print(f" Ответы - {c_owner};\n Посты - {c_posts};\n Комменты - {c_comments}; Лайки - {c_likes};\n Просмотров - {c_views};\n Репостов - {c_reposts}.")
    return main_result


# print(potential(['hurmyatina','kisszaya']))

# print(potential(domain_list))