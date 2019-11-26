import os
from PIL import Image
import datetime
import numpy as np
#path = '/home/yuqi_huo/data/urisc/'
from tqdm import tqdm
def get_datalist():
    ftr = open('urisc_train_list.txt', 'w')
    fte = open('urisc_test_list.txt', 'w')

    for roots, dirs, files in os.walk('/home/yuqi_huo/data/urisc/'):
        for name in files:
            path = os.path.join(roots, name)
            tmp_path = '/'.join(path.split('/')[4:])
            if 'complex_crop' in path:
                if 'val' in path:
                    print(tmp_path, file=fte)
                if 'train' in path and 'label' not in path:
                    tmp_path_l = tmp_path.replace('train', 'complex_train_label')
                    print(tmp_path, tmp_path_l, file=ftr)
            if 'simple' in path and 'train' in path and 'label' not in path:
                tmp_path_l = tmp_path.replace('train', 'labels')
                print(tmp_path, tmp_path_l, file=ftr)
            
        


def generate_data():
    f = open('filelist.txt')
    path = '/home/yuqi_huo/data/urisc/'
    for i in tqdm(f.readlines()):
        img_file = os.path.join(path, i.strip())
        print(img_file)
        
        houzhui = img_file.split('.')[-1]
        qianzhui = img_file.split('.')[0]
        img_name = qianzhui.split('/')[-1]
        qianzhui = '/'.join(qianzhui.split('/')[:-1])

        print(qianzhui)

        start = datetime.datetime.now()
        img = Image.open(img_file)
        end = datetime.datetime.now()
        print("程序运行时间："+str((end-start))+"秒")
        tmp = np.array(img)

        if 'complex' in img_file:
            qianzhui = os.path.join('/'.join(qianzhui.split('/')[:5]), 'complex_crop', qianzhui.split('/')[-1], img_name)
            print(qianzhui)
            if not os.path.exists(qianzhui):
                os.makedirs(qianzhui)
            step = 500
            size = 2048
            num = int((9958 - size) / step + 2)
            for x in range(num):
                for y in range(num):
                    if x != num-1:
                        if y!= num-1:
                            img_tmp = tmp[x*step : x*step+size, y*step : y*step+size]
                        else:
                            img_tmp = tmp[x*step : x*step+size, -size:]
                    else:
                        if y != num-1:
                            img_tmp = tmp[-size:, y*step : y*step+size]
                        else:
                            img_tmp = tmp[-size:, -size:]
                    assert img_tmp.shape[:2] == (2048, 2048)
                    Image.fromarray(img_tmp).save(qianzhui + '/' + img_name + '_' + str(x*num+y) + '.' + houzhui)
        else:
            assert img_tmp.shape[:2] == (1024, 1024)
            continue
        #_ = input('')

generate_data()