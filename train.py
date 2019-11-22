from libs.utils import options, config, my_log, rand_num

def main():
    ##1. import libs ok
    ##2. get args --------√
    ###2.1 get config ----√
    ###2.2 modify config -√
    ##3. dataset
    ##4. models
    ##5. do the thing
    ##log things
    
    
    my_config = config(options().parse())  #get arguments from the command line
    my_config.get_config() #get configurations from both .yaml file and user-specfic.
    log = my_log(my_config.config_file.prefix_name)

    my_config.print(log)

    rand_num(my_config.config_file.seed).set_seed()

    ##do with dataset
    
if __name__ == '__main__':
    main()