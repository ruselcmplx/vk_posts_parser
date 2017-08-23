import urllib.request as Request
import json
import time
import os.path


START_TIME = time.time()
ACCESS_TOKEN = '88af5ea888af5ea888af5ea82a88f2a4d4888af88af5ea8d1322cecc0b538ff68c8b593'
OWNER_ID = '91709075'
POSTS_HUNDREDS_COUNT = 106
URL_TEMPLATE = 'https://api.vk.com/method/wall.get?owner_id=-{owner_id}&offset={offset}&count=100&access_token={access_token}&v=V'

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
    filepath = os.path.join('c:/filthy_pics', str(post.get_id()) + '.jpg')
    with open(filepath, 'wb') as file:
        file.write(file_b)
        file.close()


def parse_result(res):
    parsed_obj = json.loads(res)['response']
    return parsed_obj[1:]


def get_result(offset=0):
    url = URL_TEMPLATE.format(owner_id=OWNER_ID, offset=offset, access_token=ACCESS_TOKEN)
    res = Request.urlopen(url).read()
    res = parse_result(res.decode('utf-8'))
    return res


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
                pic_src = pic_src.get('src_xbig', None)
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


def statistics(count):
    p = get_posts(count)
    dt = time.time() - START_TIME
    print("%f seconds" % (dt))
    print(str(len(p)) + ' posts parsed')
    print('speed: ' + str(round(len(p)/dt, 2)) + 'post/sec')


#statistics(1)
p = get_posts(1)
download_pic(next(iter(p.values())))
