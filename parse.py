import requests
from tokens import token_buff


token = token_buff
version = 5.131

def get_count_posts(domainP):
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token':token,
                                'v': version,
                                'domain': domainP,
                                'count':100,
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
                                'count':100,
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
                            'count':100,
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
                                'count':100
                            }
                            )
    # Текущий объект
    source_data = response.json()
    main_counter = 0
    for i in range(get_count_posts(domainP)):
        try:
            main_counter += source_data['response']['items'][i]['comments']['count']
        except Exception:
            main_counter = 1
    return main_counter
#Дата между постами
# date1 = source_data['response']['items'][0]['date']
# date2 = source_data['response']['items'][-1]
# count_days_between = days_between(date1,date2)

def naebalovo(koefs):
    low = []
    med = []
    hig = []

    sum = 0
    for i in koefs:
        sum+=i
    try:
        avg = sum/len(koefs)
    except Exception:
        avg = 0
    for i in koefs:
        if i < avg:
            low.append(i)
            koefs.remove(i)
    sum = 0
    for i in koefs:
        sum+=i
    try:
        avg2 = sum/len(koefs)
    except Exception:
        avg2 = 0
    for i in koefs:
        if i < avg2:
            med.append(i)
            koefs.remove(i)
        else:
            hig.append(i) 
    return [low,med,hig]

# domain_list = ['hurmyatina','a4']
def potential(domain_list):
    links = domain_list
    c_owner = []
    c_posts = []
    c_comments = []
    koefs = []
    for i in domain_list:
    
        count_owner_comments = get_count_owner_posts(i)
        print(f"Количество ответов от владельца под своим постом - {count_owner_comments}")
        c_owner.append(count_owner_comments)

        count_posts = get_count_posts(i)
        print(f"Количество постов - {count_posts}")
        c_posts.append(count_posts)

        count_comments = get_count_comments(i) 
        print(f"Количество комментов - {count_comments}")
        c_comments.append(count_comments)

        sum_koef = count_posts+count_comments*0.5+count_comments*0.25
        print(f"Числитель - {sum_koef}")
        koefs.append(sum_koef)
        
        # znamenatel = count_comments+count_owner_comments+count_posts
        # print(f"Знаменатель - {znamenatel}")

        print(f"Потенциал источника - {sum_koef}")
    low = naebalovo(koefs)
    med = naebalovo(koefs)
    hig = naebalovo(koefs)
    print(f"Итого:\n Слабый потенциал: {low};\n Средний потенциал: {med};\n Высокий потенциал: {hig}.")
    print(f"Ответы - {c_owner};\n Посты - {c_posts};\n Комменты - {c_comments}.")
    return [links,c_owner,c_posts,c_comments,low,med,hig]


# print(potential(domain_list))