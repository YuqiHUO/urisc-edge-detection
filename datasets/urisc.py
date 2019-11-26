import torch.utils.data as data
import os

class UriscEdgeDetection(data.Dataset):
    def __init__(self, args, log, mode):
        self.args = args
        self.mode = mode
        self.log = log
        self.data_list = self.args[mode.lower()].data_list
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
        _image = self.image_list[index]
        input = _image['input']
        target = _image['target'] if 'target' in _image else None
        self.log.logger.info(input)
        self.log.logger.info(target)
        
        input = os.path.join(self.args.datadir, input)
        target = os.path.join(self.args.datadir, target) if target else None

        self.log.logger.info(input)
        self.log.logger.info(target)
        return input, target
    
    def __len__(self):
        return len(self.image_list)