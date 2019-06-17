from __future__ import print_function

import argparse
import configparser as cp

class Params() : 
    def __init__(self, config_file) : 
        # attributes read in from config file 
        self.dataset = config_file.get('dataset', 'dataset')
        self.data_location = config_file.get('dataset', 'dataset_location')

        self.arch = config_file.get('cnn', 'architecture')        
        self.depth = config_file.get('cnn', 'depth')       
        self.cardinality = config_file.get('cnn', 'cardinality')
        self.widen_factor = config_file.get('cnn', 'widen_factor')
        self.growth_rate = config_file.get('cnn', 'growth_rate')
        self.compression_rate = config_file.get('cnn', 'compression_rate')

        # self.start_epoch = config_file.getint('training_hyperparameters', 'start_epoch')
        self.printOnly = config_file.getboolean('training_hyperparameters', 'print_only')
        self.epochs = config_file.getint('training_hyperparameters', 'total_epochs')
        self.train_batch = config_file.getint('training_hyperparameters', 'train_batch')
        self.test_batch = config_file.getint('training_hyperparameters', 'test_batch') 
        self.lr = config_file.getfloat('training_hyperparameters', 'learning_rate')
        self.minLR = config_file.getfloat('training_hyperparameters', 'min_lr')
        self.dropout = config_file.getfloat('training_hyperparameters', 'dropout_ratio')
        self.gamma = config_file.getfloat('training_hyperparameters', 'gamma')
        self.momentum = config_file.getfloat('training_hyperparameters', 'momentum') 
        self.weight_decay = config_file.getfloat('training_hyperparameters', 'weight_decay') 
        self.mo_schedule = [self.__to_num(i) for i in config_file.get('training_hyperparameters', 'momentum_schedule').split()]
        self.lr_schedule = [self.__to_num(i) for i in config_file.get('training_hyperparameters', 'lr_schedule').split()]
        self.trainValSplit = config_file.getfloat('training_hyperparameters', 'train_val_split')
        
        self.sub_classes = config_file.get('pruning_hyperparameters', 'sub_classes').split() 

        self.manual_seed = config_file.getint('pytorch_parameters', 'manual_seed')
        self.workers = config_file.getint('pytorch_parameters', 'data_loading_workers')
        self.gpu_id = config_file.get('pytorch_parameters', 'gpu_id')
        self.pretrained = config_file.get('pytorch_parameters', 'pretrained')        
        self.checkpoint = config_file.get('pytorch_parameters', 'checkpoint_path')
        self.test_name = config_file.get('pytorch_parameters', 'test_name')
        self.resume = config_file.getboolean('pytorch_parameters', 'resume')
        self.branch = config_file.getboolean('pytorch_parameters', 'branch')
        self.evaluate = config_file.getboolean('pytorch_parameters', 'evaluate')
        self.tee_printing = config_file.get('pytorch_parameters', 'tee_printing')

        # attributes used internally
        self.use_cuda = True
        self.start_epoch = 0 
        self.curr_epoch = 0 
        self.train_loss = 0 
        self.train_top1 = 1
        self.train_top5 = 1
        self.test_loss = 0 
        self.test_top1 = 1
        self.test_top5 = 1
        self.bestValidLoss = 0.0

        # muppet attributes 
        self.runMuppet = config_file.getboolean('muppet_hyperparameter', 'run_muppet')
        self.bitWidth = config_file.getint('muppet_hyperparameters', 'bit_width')
        self.dataType = config_file.get('muppet_hyperparameters', 'data_type')
        self.roundMeth = config_file.get('muppet_hyperparameters', 'round_meth')
        self.policyResolution = config_file.getint('muppet_hyperparameters', 'policy_resolution')
        self.policyPatience = config_file.getint('muppet_hyperparameters', 'policy_patience')
        self.lowPrecLimit = config_file.getint('muppet_hyperparameters', 'low_prec_limit')
        self.fp32EpochsPerLR = config_file.getint('muppet_hyperparameters', 'fp32_epochs_per_lr')

        self.meanGD = 0
        self.maxGD = 0
        self.gdViolations = 0
        self.sumOfNorms = {}
        self.sumOfGrads = {}
        self.quantised = (self.bitWidth != 'Float')
        self.sub_classes = []
        
    def get_state(self) : 
        return self.__dict__

    def __to_num(self, x) : 
        try : 
            return int(x) 
        except ValueError: 
            return float(x) 

def parse_command_line_args() : 
    parser = argparse.ArgumentParser(description='PyTorch Pruning')

    # Command line vs Config File
    parser.add_argument('--config-file', default='None', type=str, help='config file with training parameters')
    
    args = parser.parse_args()

    return args
