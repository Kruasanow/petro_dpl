import requests

token = '94aa5d6594aa5d6594aa5d65a497be1e27994aa94aa5d65f0d97ee5dc95e8f4035d1c7d'
version = 5.131
domain = 'hurmyatina'
# owner_id = -127321253
# post_id = 337

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
    count_post = len(source_data['response']['items'])
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
        id_list.append(response_prepare.json()['response']['items'][i]['id'])
        owner_id_list.append(response_prepare.json()['response']['items'][i]['owner_id'])
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
    owner_id_list = get_all_posts_id(domainP)[1][-1] # Это ебаный костыль!
    print(owner_id_list)
    k = 0
    main_k = 0

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
            comments = data['response']['items']
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
        main_counter += source_data['response']['items'][i]['comments']['count']
    return main_counter

#Дата между постами
# date1 = source_data['response']['items'][0]['date']
# date2 = source_data['response']['items'][-1]
# count_days_between = days_between(date1,date2)

def potential(domain_list):
    for i in domain_list:
        count_owner_comments = get_count_owner_posts(i)
        print(f"Количество ответов от владельца под своим постом - {count_owner_comments}")

        count_posts = get_count_posts(i)
        print(f"Количество постов - {count_posts}")

        count_comments = get_count_comments(i) 
        print(f"Количество комментов - {count_comments}")

        sum_koef = count_posts+count_comments*0.5+count_comments*0.25
        print(f"Числитель - {sum_koef}")

        znamenatel = count_comments+count_owner_comments+count_posts
        print(f"Знаменатель - {znamenatel}")
        res = sum_koef/znamenatel
        print(f"Потенциал источника - {res}")

domains = ['hurmyatina','a4']
potential(domains)
print(1)
