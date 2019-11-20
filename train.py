from libs.utils import options, rand_num, config

def main():
    ##1. import libs ok
    ##2. get args ok
    ###2.1 get config
    ###2.2 modify config
    ##3. dataset
    ##4. models
    ##5. do the thing
    ##log things
    
    args = options().parse() #get arguments from the command line
    config(args).get_config() #get configurations from both .yaml file and user-specfic.
    rand_num(0).set_seed()

if __name__ == '__main__':
    main()