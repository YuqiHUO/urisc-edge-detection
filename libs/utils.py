import sys, os
import argparse
import yaml
from easydict import EasyDict as edict
from ast import literal_eval
import pprint

from datetime import datetime
import logging
from logging import handlers

import random
import numpy as np
import torch

class options():
    def __init__(self):
        #first, read the default.yaml or the user specific config file
        #then, modify the yaml with user-added options
        parser = argparse.ArgumentParser(description='Edge detection.', fromfile_prefix_chars='@')
        parser.add_argument('--config_file', '--config', nargs=1, type=str, required=True, help='config .yaml file.')
        parser.add_argument('opts', nargs='*', type=str, help='user specific config.')
        self.parser = parser
    
    def parse(self):
        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(1)
        args = self.parser.parse_args()
        return args

class config():
    def __init__(self, args):
        self.config_file_name = args.config_file[0]
        self.config_file = None
        self.opts = args.opts

    def get_config(self):
        print("Loading config file from {}.".format(self.config_file_name))
        self.config_file = edict(yaml.load(open(self.config_file_name), Loader=yaml.FullLoader))
        
        if len(self.opts) != 0:
            self.get_config_from_list()
        
        print(self.config_file.model)
    
    def get_config_from_list(self):
        print("Loading config file from user specfic.")
        assert len(self.opts) % 2 == 0, "user specfic config should have even args."
        dict_len = len(self.opts) / 2
        for key, value in zip(self.opts[0::2], self.opts[1::2]):
            key_list = key.split('.')
            cfg = self.config_file
            for subkey in key_list[:-1]:
                assert subkey in cfg, 'Config key {} not found'.format(subkey)
                cfg = cfg[subkey]
            subkey = key_list[-1]
            assert subkey in cfg, 'Config key {} not found'.format(subkey)
            try:
                # Handle the case when v is a string literal.
                val = literal_eval(value)
            except BaseException:
                val = value
            assert isinstance(val, type(cfg[subkey])) or cfg[subkey] is None, 'type {} does not match original type {}'.format(type(val), type(cfg[subkey]))
            cfg[subkey] = val
            #self.config_file = cfg
    
    def print(self, log):
        log.logger.info('Config:')
        log.logger.info(pprint.pformat(self.config_file))

class my_log():
    def __init__(self, prefix_name):
        TIMESTAMP = "{0:_%m_%d_%H_%M}".format(datetime.now())
        if prefix_name:
            TIMESTAMP = prefix_name + TIMESTAMP
        log_dir = os.path.join('results', TIMESTAMP)
        log_name = os.path.join(log_dir, TIMESTAMP + '.log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(handlers.TimedRotatingFileHandler(filename=log_name))
        

    def info(information):
        self.logger.info(informaiton)

class rand_num():
    def __init__(self, seed):
        self.seed = seed
    
    def set_seed(self):
        random.seed(self.seed)
        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        torch.cuda.manual_seed(self.seed)
        torch.backends.cudnn.deterministic=True## Not sure when is needed

    def worker_init_fn(self, worker_id):
        np.random.seed(self.seed + worker_id)