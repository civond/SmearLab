'''
FMON MODULE
Preferences (Constants in Freely Moving Olfactory Navigation Task)

Written By: Sarah Stednitz (sstednit@uoregon.edu) & Teresa Findley (tmfindley15@gmail.com)
Last Updated: 2.24.21, Dorian Yeh
'''
from numpy.random import choice
#     [USER INPUT]     #

experimenter = 'Dorian Yeh' #your full name
trainer = 'None' #who is training you? (if applicable -- if no one, put 'none') 
sex = 'F' #of mouse, not experimenter (female or male)
mouse_id = "2152" #mouse subject number
initial_weight = '19.91' #in grams
group_name = "100-0" #what experiment are you running? (OPTIONS: trainer1, trainer2, 100-0, 80-20, 60-40, interleaved, abs-conc, non-spatial, nostril-occlusion) 
#IMPORTANT: trainer1 and trainer2 are run through separate codes (labeled trainer#1 and trainer#2)...everything else runs in MASTERCODE
sniffing = 'no' #is the sniff wire plugged in? (yes, no) 
percentinvial= '0.01' #what percent of odorant is in the odor vial (should be written on the label) 
occluded_nostril = 'none' #is a nostril occluded? (none, left, right, left-sham, right-sham)
wcL = '6.96'#left water port calibration (how many microliters per reward?)
wcR = '6.95' #right water port calibration
wcIP = '6.67' #initiation water port calibration
odortype = '2-PE' #odor identity (pinene, octanol, amyl acetate, methyl salicate, etc.)

side_bias = 0; #set to 0 for left and right trials, set to 1 for only right trials, set to 2 for only left trials 

#Odor vials! Key: 6 = blank, 7 = vanillin (1%), 8 = 2-PE (0.01%)
odor_vial = 8 #main odor (7 = vanillin), 8 = 2PE
alternate_vial = 8 #alternate odor
blank_vial = 6

#Only for non-spatial experiments
non_spatial_condition = 'odor_identity' #OPTIONS: odor_concentration or odor_identity

#     [SET UP]     #


##IMPORTS
##libraries
import numpy as np, serial, ctypes,nidaqmx
int32 = ctypes.c_long; uInt64 = ctypes.c_ulonglong; float64 = ctypes.c_double #64 bit float
#     [OPTIONS]     #

##TRIAL
random_groupsize = 40 #group of trials that contain an even # of events, divisible by 20
total_groupsize = 800 #total number of possible trials, must be divisible by random_groupsize
show_active_stats = True;
#Data Paths
base_dir = "D:/FMON_Project/data/goodmice/" #root of data path (below, data compilation file location)
#Timing
count_requirement = 4 #how many frames in one quadrant registers response? 
iti_correct = 4; iti_incorrect = 10 #inter-trial intervals
timeout_delay = 5*60 #how long does the timeout between trials?
#Online Tracking
y_min = 0; y_max = 720; x_min = 0; x_max = 1210;
x_sections = 3; y_sections = 2 #how many partitions? 
#Valve Designations
left_valve = 2; right_valve = 1; rightport = 1; leftport = 2; nosepokeport = 4; MFC_air = 1; MFC_n2 = 2;

##NI USB-6009 DATA COLLECTION
samplingrate = 800; buffersize = 25; channel_num = 6 #number of channels
#Name Channels (this is how the files will be saved in the datapath)
ch0 = 'sniff'; ch1 = 'NP'; ch2 = 'LFV'; ch3 = 'RFV';

##ARDUINO & TEENSY COMMUNICATION
port='\\\\.\\COM5'; tnsyport = '\\\\.\\COM4';

#     [CONSTANTS]     #

##TRIAL
if group_name == 'trainer1' or group_name == 'trainer2' or group_name == 'trainer2_non-spatial':
    sessionlength = 30#in minutes

if group_name == '100-0' or group_name == '90-10' or group_name == '80-20' or group_name == '60-40' or group_name =='90-10_alt' or group_name == '90-10_interleaved':
    sessionlength = 40 #in minutes

    
if group_name == 'interleaved' or group_name == 'abs-conc' or group_name == 'non-spatial' or group_name == 'nostril-occlusion' or group_name == 'mineral-oil' or group_name == 'thresholding':
    sessionlength = 40 #in minutes
session_length = sessionlength * 60
#Online Tracking
num_sections = x_sections*y_sections; section  = [np.nan]*num_sections; section_center = [np.nan]*num_sections; 

##NI USB-6009 DATA COLLECTION
channels = 'Dev1/ai0:' + str(channel_num-1); ni_data = nidaqmx.Task()

##ARDUINO & TEENSY COMMUNICATION
ard = serial.Serial(port,115200,timeout=1); tnsy = serial.Serial(tnsyport,115200,timeout=1)
