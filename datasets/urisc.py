import torch.utils.data as data
import os
import random
from PIL import Image
import numpy as np
import torch

class UriscEdgeDetection(data.Dataset):
    def __init__(self, args, log, mode):
        self.args = args
        self.mode = mode
        self.log = log
        self.data_list = self.args[mode.lower()].data_list
        self.crop_size = self.args[mode.lower()].crop_size
        self._input_mean = torch.from_numpy(np.array([0.51430742, 0.51430742, 0.51430742]).reshape((1, 3, 1, 1))).float()
        self._input_std = torch.from_numpy(np.array([0.18548921, 0.18548921, 0.18548921]).reshape((1, 3, 1, 1))).float()
        self._get_data_list()
        self.__getitem__(0)

    def _get_data_list(self):
        self.image_list = []
        f = open(self.data_list)
        for line in f.readlines():
            _input = line.strip().split()[0]
            image_info = {'input': _input}
            if self.mode is not 'test':
                target = line.strip().split()[1]
                image_info['target'] = target
            self.image_list.append(image_info)
        self.log.logger.info('{} file loaded in {} mode.'.format(len(self.image_list), self.mode))

    def __getitem__(self, index):
        _image = random.choice(self.image_list) if self.mode == 'train' else self.image_list[index]
        input_img = _image['input']
        target = _image['target'] if 'target' in _image else None
        self.log.logger.info(input_img)
        self.log.logger.info(target)
        
        input_img = os.path.join(self.args.datadir, input_img)
        target = os.path.join(self.args.datadir, target) if target else None
        input_img = Image.open(input_img)
        target = Image.open(target) if target else None

        assert input_img.size == (1024, 1024) or input_img.size == (2048, 2048)
        if target is not None:
            #target = target[..., np.newaxis]
            assert target.size == (1024, 1024) or target.size == (2048, 2048)
            assert target.size == input_img.size
        
        if target is not None:
            if self.mode == 'train':
                input_img, target = self._train_sync_transform(input_img, target)#img numpy mask tensor
            elif self.mode == 'val':
                input_img, target = self._val_test_sync_transform(input_img, target)#img numpy mask tensor
            target = torch.from_numpy(target).permute(3, 2, 0, 1)#[1/4, C, H, W]
            target = target.float() / 255

        elif self.mode == 'test':
            input_img, target = self._val_test_sync_transform(input_img)#img numpy mask tensor
            
        input_img = torch.from_numpy(input_img).permute(3, 2, 0, 1)#[1/4, C, H, W]
        input_img = input_img.float() / 255
        input_img = (input_img - self._input_mean) / self._input_std
        self.log.logger.info(input_img.shape)
        if target is not None:
            self.log.logger.info(target.shape)
        return input, target
    
    def __len__(self):
        return len(self.image_list)

    def _train_sync_transform(self, img, mask):#train
        #flip
        if random.random() < 0.5:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            mask = mask.transpose(Image.FLIP_LEFT_RIGHT)
        if random.random() < 0.5:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            mask = mask.transpose(Image.FLIP_TOP_BOTTOM)
        #scale
        if img.size == (2048, 2048):
            scale_size = random.randint(int(2048 * self.args.train.scale[0]), int(2048 * self.args.train.scale[0]))
            assert scale_size >= self.crop_size 
            img = img.resize((scale_size, scale_size), Image.BILINEAR)
            mask = mask.resize((scale_size, scale_size), Image.NEAREST)

        img = np.array(img).astype(np.float32)[..., np.newaxis]
        mask = np.array(mask).astype(np.float32)[..., np.newaxis, np.newaxis]
        #crop
        if img.shape[0] > self.crop_size:
            w, h = mask.size
            x1 = random.randint(0, w - self.crop_size)
            y1 = random.randint(0, h - self.crop_size)
            img = img[y1 : y1 + self.crop_size, x1 : x1 + self.crop_size, :]# crop image
            mask = mask[y1 : y1 + self.crop_size, x1 : x1 + self.crop_size]# crop image
        return img, mask

    def _val_test_sync_transform(self, img, mask=None):
        img = np.array(img).astype(np.float32)[..., np.newaxis]
        if mask is not None:
            mask = np.array(mask).astype(np.float32)[..., np.newaxis, np.newaxis]
            if img.shape[0] > self.crop_size:
                mask_0 = mask[:1024, :1024, :]
                mask_1 = mask[:1024, 1024:, :]
                mask_2 = mask[1024:, :1024, :]
                mask_3 = mask[1024:, 1024:, :]
                mask = np.concatenate((mask_0, mask_1, mask_2, mask_3), axis=3)
        if img.shape[0] > self.crop_size:
            img_0 = img[:1024, :1024, :]
            img_1 = img[:1024, 1024:, :]
            img_2 = img[1024:, :1024, :]
            img_3 = img[1024:, 1024:, :]
            img = np.concatenate((img_0, img_1, img_2, img_3), axis=3)
        return img, mask
