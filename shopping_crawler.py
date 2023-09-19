import os
import urllib
import h5py
import numpy as np
import json
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from feature_extractor import FeatureExtractor
import threading

load_dotenv()
CLIENT_ID = os.environ.get('NAVER_ID')
CLIENT_SECRET = os.environ.get('NAVER_PW')
<<<<<<< HEAD
=======

# with open('furniture.json', 'r') as file1:
#     furniture = json.load(file1)
# with open('appliances.json', 'r') as file2:
#     appliances = json.load(file2)
# queries = {**furniture, **appliances}

# queries = {"sofa":"소파", "desk":"책상", "drawer":"서랍장"}
furniture_queries = {
    "sofa":"소파",
    "desk":"책상",
    "drawer":"서랍장",
    "bed":"침대",
    "dressing_table":"화장대",
    "table":"식탁",
    "cabinet":"장식장",
    "wardrobe":"장롱",
    "chair":"의자"
}

appliance_queries = {
    "refrigerator": "냉장고",
    "dryer":"건조기",
    "air_cleaner":"공기청정기",
    "rice_cooker":"밥솥",
    "microwave":"전자레인지",
    "air_conditioner":"에어컨",
    "styler":"스타일러",
    "fan":"선풍기",
    "washing_machine":"세탁기",
    "robot_vacuum_cleaner":"로봇청소기",
    "vacuum_cleaner":"청소기",
    "air_fryer":"에어프라이어"
}

queries = [furniture_queries, appliance_queries]

#총 1000개 상품 크롤링
# START = 1
# COUNT = 10
# DISPLAY = 100
>>>>>>> feature/flask
START = 1
COUNT = 10
DISPLAY = 100
FE = FeatureExtractor()

def get_shopping_data(client_id, client_secret, query, display, sort, start, count):
    url = "https://openapi.naver.com/v1/search/shop.json?query={}&display={}&sort={}&start={}".format(query, display, sort, start + count*display)
    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)
    response = urllib.request.urlopen(request)
    dic = response.read().decode('utf-8')
    return eval(dic)['items']

<<<<<<< HEAD
def data_parser(query):
    query = urllib.parse.quote(query)
    result = []
    for cnt in range(COUNT):
        result += get_shopping_data(CLIENT_ID, CLIENT_SECRET, query, DISPLAY, 'sim', START, cnt)
    features = []
    for idx, product in enumerate(result):
        img = result[idx]['image'] = ''.join(product['image'].split('\\'))
        result[idx]['link']        = ''.join(product['link'].split('\\'))
        result[idx]['category1']   = ''.join(product['category1'].split('\\'))
        result[idx]['category2']   = ''.join(product['category2'].split('\\'))
        result[idx]['category3']   = ''.join(product['category3'].split('\\'))
        result[idx]['category4']   = ''.join(product['category4'].split('\\'))
        result[idx]['title'] = product['title'].split("<b>")[0]
        result[idx].pop('hprice')
        result[idx].pop('productId')
        result[idx].pop('mallName')
        result[idx].pop('productType')
        result[idx].pop('maker')
        try:
            res = urllib.request.urlopen(img).read()
            pic = Image.open(BytesIO(res))
            '''
            배경제거 코드 들어감
            '''
            feature = FE.extract(img=pic)
            features.append(feature)
        except:
            pass
    return result, features

def process_category(category, queries): 
    for subcategory, query in queries.items():
        json_data, features = data_parser(query)
        np.save('./static/feature/'+category+subcategory+'.npy', features)
        with open('./static/json/'+category+subcategory+'.json', 'w') as f:
            json.dump(json_data, f)
        f.flush()

if __name__ == '__main__':
    with open('./query.json', 'r', encoding='utf-8') as file:
        queries = json.load(file)
    # queries = {
    #     "appliances": 
    #     {
    #         # "refrigerator": "냉장고",
    #         # "dryer":"건조기",
    #         # "air_cleaner":"공기청정기",
    #         # "rice_cooker":"밥솥",
    #         # "microwave":"전자레인지",
    #         # "air_conditioner":"에어컨",
    #         # "styler":"스타일러",
    #         "fan":"선풍기", # retry
    #         # "washing_machine":"세탁기",
    #         # "robot_vacuum_cleaner":"로봇청소기",
    #         # "vacuum_cleaner":"청소기",
    #         # "air_fryer":"에어프라이어"
    #     },
    #     "furniture" : 
    #     {
    #         # "sofa":"소파",
    #         # "desk":"책상",
    #         # "drawer":"서랍장",
    #         # "bed":"침대",
    #         # "dressing_table":"화장대",
    #         "table":"식탁", # retry
    #         # "cabinet":"장식장",
    #         # "wardrobe":"장롱",
    #         # "chair":"의자"
    #     }
    # }
    threads = []
    for category, subcategories in queries.items():
        thread = threading.Thread(target=process_category, args=(category, subcategories))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    # for category in queries.keys():
    #     for subcategory, query in queries[category].items():
    #         json_data, features = data_parser(query, fe) 
    #         np.save('./static/feature/'+category+subcategory+'.npy', features)
    #         with open('./static/json/'+category+subcategory+'.json', 'w') as json_file:
    #             json.dump(json_data, json_file)
    with h5py.File('data.h5', 'w') as hdf5_file:
        for category in queries.keys():
            category_group = hdf5_file.create_group(category)
            for subcategory, query in queries[category].items():
                subcategory_group = category_group.create_group(subcategory)
                features = np.load('./static/feature/'+category+subcategory+'.npy')
                with open('./static/json/'+category+subcategory+'.json', 'r') as json_file:
                    json_data = json.load(json_file)
                subcategory_group.create_dataset('json', data=json.dumps(json_data))
                subcategory_group.create_dataset('npy', data=np.array(features))
    # with h5py.File('data.h5', 'w') as hdf5_file:
    #     for category in queries.keys():
    #         category_group = hdf5_file.create_group(category)
    #         for subcategory, query in queries[category].items():
    #             subcategory_group = category_group.create_group(subcategory)
    #             json_data, features = data_parser(query, fe)
    #             subcategory_group.create_dataset('json', data=json.dumps(json_data))
    #             subcategory_group.create_dataset('npy', data=np.array(features))
=======
if __name__ == '__main__':
    fe = FeatureExtractor()
    for i in range(2):
        answer = {}
        for cat, query in queries[i].items():
            result = []
            query = urllib.parse.quote(query)
            for cnt in range(COUNT):
                result += get_shopping_data(CLIENT_ID, CLIENT_SECRET, query, DISPLAY, 'sim', START, cnt)

            features = []
            features_path = Path("./static/feature") / (str(cat) + ".npy")
            for idx, product in enumerate(result):
                link = ''.join(product['link'].split('\\'))
                img = ''.join(product['image'].split('\\'))
                cat1 = ''.join(product['category1'].split('\\'))
                result[idx]['link'] = link
                result[idx]['image'] = img
                result[idx]['category1'] = cat1
                result[idx].pop('hprice')
                result[idx].pop('productId')
                result[idx].pop('mallName')
                result[idx].pop('productType')
                result[idx].pop('maker')
                # res = urllib.request.urlopen(img).read()
                # image_np = np.frombuffer(res, dtype=np.uint8)
                # image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
                # cv2.imwrite('./tmp/' + str(idx) + '.png', image)
                # res = requests.get(img, stream=True)
                res = urllib.request.urlopen(img).read()
                pic = Image.open(BytesIO(res))
                print(type(pic))

                '''
                BGrem 이 부분에서 식별해서 배경 제거할것
                OS.remove(원본파일)
                '''
                # feature = fe.extract(img=Image.open('./tmp/' + str(idx) + '.png'))
                # features.append(feature)
                '''
                OS.remove(배경제거파일)
                '''
            answer[cat] = result
            '''
            hdf5 파일 저장 코드 필요
            json 저장
            '''
            np.save(features_path, np.array(features))
        if not i:
            with open('./furniture.json', 'w', encoding='utf-8') as f:
                json.dump(answer, f, ensure_ascii=False, indent=4)
        if i:
            with open('./appliance.json', 'w', encoding='utf-8') as f:
                json.dump(answer, f, ensure_ascii=False, indent=4)
>>>>>>> feature/flask
