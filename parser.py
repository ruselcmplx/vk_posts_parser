import urllib.request as Request
import json
import time
import os.path


START_TIME = time.time()
ACCESS_TOKEN = '88af5ea888af5ea888af5ea82a88f2a4d4888af88af5ea8d1322cecc0b538ff68c8b593'
OWNER_ID = '91709075'
POSTS_HUNDREDS_COUNT = 106
URL_TEMPLATE = 'https://api.vk.com/method/wall.get?owner_id=-{owner_id}&offset={offset}&count=100&access_token={access_token}&v=V'
DESTINATION_FOLDER = 'c:/filthy_pics'

post_objs = {}

class Post():
    def __init__(self, post_id, img_url, likes_count):
        self.post_id = post_id
        self.img_url = img_url
        self.likes_count = likes_count

    def get_id(self):
        return self.post_id

    def get_url(self):
        return self.img_url

    def get_likes_count(self):
        return self.likes_count


def download_pic(post):
    file_b = Request.urlopen(post.get_url()).read()
    filepath = os.path.join(DESTINATION_FOLDER, str(post.get_id()) + '.jpg')
    with open(filepath, 'wb') as file:
        file.write(file_b)
        file.close()


def download_pic_sorted(post):
    file_b = Request.urlopen(post.get_url()).read()
    count = post.get_likes_count()
    if count < 2:
        dest = DESTINATION_FOLDER + '/bad'
    elif count < 6:
        dest = DESTINATION_FOLDER + '/lame'
    elif count < 16:
       dest = DESTINATION_FOLDER + '/soso'
    elif count < 32:
       dest = DESTINATION_FOLDER + '/nice'
    elif count < 256:
       dest = DESTINATION_FOLDER + '/good'
    filepath = os.path.join(dest, str(post.get_id()) + '.jpg')
    with open(filepath, 'wb') as file:
        file.write(file_b)
        file.close()


def get_result(offset=0):
    url = URL_TEMPLATE.format(owner_id=OWNER_ID, offset=offset, access_token=ACCESS_TOKEN)
    res = Request.urlopen(url).read()
    parsed_obj = json.loads(res.decode('utf-8'))['response']
    return parsed_obj[1:]


def create_post_objs(arr):
    for post in arr:
        post_type = post.get('post_type', None)

        if post_type != 'post':
            continue

        att = post.get('attachments', None)
        if not att:
            continue
        elif att[0].get('type', None) != 'photo':
            continue

        id = post.get('id',None)
        pic_src = post.get('attachments', None)
        if pic_src:
            pic_src = pic_src[0].get('photo', None)
            if pic_src:
                pic_src = pic_src.get('src_big', None)
        likes_count = post['likes']['count']
        post_obj = Post(id, pic_src, likes_count)
        post_objs[post['id']]=post_obj
    return post_objs


def get_posts(hundreds_posts=POSTS_HUNDREDS_COUNT):
    offset = 0
    posts = []
    for i in range(0, hundreds_posts):
        res = get_result(offset)
        posts += res
        offset += 100
    res = create_post_objs(posts)
    return res


def speed(count):
    dt = time.time() - START_TIME
    print("%f seconds" % (dt))
    #print(str(len(p)) + ' posts parsed')
    print('speed: ' + str(round(count/dt, 2)) + 'post/sec')


def statistics(posts):
    maxlike = 0
    top_post = []
    minlike = 1
    lame_post = []
    k = 0
    categories = {
        0:2,
        1:6,
        2:16,
        3:32,
        4:256
    }
    cat_count = {
        0:0,1:0,2:0,3:0,4:0
    }
    #for p in posts:
    #    if p.get_likes_count() > maxlike:
    #        maxlike = p.get_likes_count()
    #        top_post.append(p.get_id())
    #    if p.get_likes_count() < minlike:
    #        minlike = p.get_likes_count()
    #        lame_post.append(p.get_id())
    #    k+=1
    for p in posts:
        count = p.get_likes_count()
        if count < categories[0]:
            cat_count[0] += 1
            continue
        if count < categories[1]:
            cat_count[1] += 1
            continue
        if count < categories[2]:
            cat_count[2] += 1
            continue
        if count < categories[3]:
            cat_count[3] += 1
            continue
        if count < categories[4]:
            cat_count[4] += 1
            continue

    print('Likes count by cathegory:')
    print('<2: ' + str(cat_count[0]))
    print('<6: ' + str(cat_count[1]))
    print('<8: ' + str(cat_count[2]))
    print('<32: ' + str(cat_count[3]))
    print('<256: ' + str(cat_count[4]))
    #speed(k)
    #print('Posts count: ' + str(k))
    #print('Maximum like value: ' + str(maxlike))
    #print('Top posts:')
    #print(top_post)
    #print('Minimum like value: ' + str(minlike))
    #print('Lame posts:')
    #print(lame_post)


#statistics(1)
print('GETTING POSTS_____________________________')
ps = list(get_posts().values())
speed(len(ps))
#print('CALCULATING LIKES COUNT___________________')
#statistics(ps)
print('DOWNLOADING PICS__________________________')
for p in ps:
    download_pic(p)
print('SUCC ESS__________________________________')

