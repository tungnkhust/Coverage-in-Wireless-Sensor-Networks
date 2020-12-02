import yaml
import sys

ROOT_PATH = '/home/tungnk/Desktop/learning/20201/Evolution_Computing/Coverage-in-Wireless-Sensor-Networks'

with open(ROOT_PATH + '/config/config.yaml', 'r') as pf:
    config = yaml.safe_load(pf)
    NUM_TARGET = config['TARGET']['NUM_TARGET']
    Q_MIN = config['TARGET']['Q_MIN']
    Q_MAX = config['TARGET']['Q_MAX']
    W = config['DOMAIN']['W']
    H = config['DOMAIN']['H']
    Rs = config['RADIUS']['SENSE']
    Rc = config['RADIUS']['TRANSFER']
    EPSILON = config['OPTIONAL']['EPSILON']
    CHANGE_DATA = config['DATA']['CHANGE_DATA']
    CHANGE_Q = config['TARGET']['CHANGE_Q']
    N_TEST = config['DATA']['N_TEST']