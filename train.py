from libs.utils import options, config, my_log, rand_num
from datasets import get_dataset

def main():
    ##1. import libs ok
    ##2. get args --------√
    ###2.1 get config ----√
    ###2.2 modify config -√
    ##3. dataset
    ###flip scale crop ---√
    ###rotate tranflate noise 
    ##4. models
    ##5. do the thing
    ##log things
    
    
    my_config = config(options().parse())  #get arguments from the command line
    my_config.get_config() #get configurations from both .yaml file and user-specfic.
    log = my_log(my_config.config_file.prefix_name)

    my_config.print(log)
    rand_num(my_config.config_file.seed).set_seed()

    trainset = get_dataset(name=my_config.config_file.dataset, args=my_config.config_file, log=log, mode='train')
    valset = get_dataset(name=my_config.config_file.dataset, args=my_config.config_file, log=log, mode='val')
    testset = get_dataset(name=my_config.config_file.dataset, args=my_config.config_file, log=log, mode='test')
    #kwargs = {'num_workers': args.workers, 'pin_memory': True} \
    self.trainloader = data.DataLoader(trainset, batch_size=my_config.config_file.train.batch_size, shuffle=True, **kwargs)
    self.valloader = data.DataLoader(valset, batch_size=my_config.config_file.val.batch_size, shuffle=False, **kwargs)
    self.testloader = data.DataLoader(testset, batch_size=my_config.config_file.test.batch_size, shuffle=False, **kwargs)


    
    
if __name__ == '__main__':
    main()