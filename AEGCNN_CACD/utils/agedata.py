#SAURAV RAI
#AGE DATA FILE FOR THE CACD DATASET

import os
import pickle
import numpy as np
from PIL import Image
from torch.utils.data import Dataset
from utils import settings
from sklearn import metrics
import torch

class AgeFaceDataset(Dataset):
    def __init__(self,transform = None ,istrain =False, isvalid=False ,isquery = False ,isgall1 = False ,isgall2 =False ,isgall3 =False):
        super().__init__()  
        self.metafile = os.path.join('/home/Saurav/Desktop/DB/meta_data/cacd_metafile_latest.pkl')
        
        with open(self.metafile, 'rb') as fd:
            self.morph_dict = pickle.load(fd)

        self.labels = list(self.morph_dict.keys())
        self.images = list(self.morph_dict.values())
        self.root_path = settings.args.root_path

        self.transform =transform     
        # LIST OF INFORMATION OF THE IMAGES   
        self.istrain = istrain
        self.isvalid = isvalid
        self.isquery = isquery
        self.isgall1 = isgall1
        self.isgall2 = isgall2
        self.isgall3 = isgall3
        #ALL THE LIST VARIABLES REQUIRED FOR TEST PART
        self.list_test_ids = []  
        self.list_test_ages = []
        self.all_test_list = []
        self.test_query_list = []
        self.test_gall1_list = []
        self.test_gall2_list = []
        self.test_gall3_list = []
       #ALL THE LIST VARIABLES REQUIRED FOR TRAIN PART
        self.list_train_ids= []
        self.list_train_ages =[]
        self.all_train_list = []
       #THIS ONE IS FOR VALIDATION SET:
        self.list_valid_ids= []
        self.list_valid_ages =[]
        self.all_valid_list = []
        self.valid_query_list = []
        self.valid_gall1_list = []
        self.valid_gall2_list = []
        self.valid_gall3_list = []
        for i in range(len(self.labels)):
            # 1 .THE TEST SET:
            if(self.images[i][2] == 3 or self.images[i][2]==4 or self.images[i][2] ==5 ):
                if(self.images[i][0] not in self.list_test_ids):
                    self.list_test_ids.append(self.images[i][0])
                if(self.images[i][3] not in self.list_test_ages):
                    self.list_test_ages.append(self.images[i][3])
                self.list_test_ids.sort() 
                self.list_test_ages.sort()
               
            # 2 .THIS IS FOR THE VALID SET SET:
            else: # THE TOTAL NO OF IMAGES IS : 29826 
                if(self.images[i][2] == 6 or self.images[i][2]==7 or self.images[i][2] ==8  or self.images[i][2] == 9 or self.images[i][2] == 10 or self.images[i][2] ==11 or self.images[i][2]== 12 or self.images[i][2] == 13 or self.images[i][2] ==14):

                    if(self.images[i][0] not in self.list_valid_ids):
                        self.list_valid_ids.append(self.images[i][0])
                    if(self.images[i][3] not in self.list_valid_ages):
                        self.list_valid_ages.append(self.images[i][3])
                    self.list_valid_ids.sort() 
                    self.list_valid_ages.sort()
                 
             # 3 .THIS IS THE TRAIN PART
                else:
                    if(self.images[i][0] not in self.list_train_ids):
                        self.list_train_ids.append(self.images[i][0])
                    if(self.images[i][3] not in self.list_train_ages):
                        self.list_train_ages.append(self.images[i][3])
                   
                    self.list_train_ids.sort() 
                    self.list_train_ages.sort()

        #THIS IS FOR THE TRAIN PART
        x = range(15,51)
        y = range(1,3) 
        #THIS ONE IS FOR IDS
        dic= {}
        for i in range(len(self.list_train_ids)):
            dic.update({self.list_train_ids[i]:i})
        #THIS ONE IS FOR THE AGE IDS
        dic1 = {}
        for i  in range(len(self.list_train_ages)):
            dic1.update({self.list_train_ages[i]:i})
             
        for i in range(len(self.labels)):
            
            if(self.images[i][2] in x or self.images[i][2] in y):

                self.all_train_list.append([dic[self.images[i][0]],self.images[i][1],self.images[i][2],dic1[self.images[i][3]],self.images[i][4],self.images[i][5]])
                    

        #THIS IS FOR THE TEST PART
        b = range(3,6)
        dic2 ={}
        #THIS ONE FOR THE IDS
        for i in range(len(self.list_test_ids)):
            dic2.update({self.list_test_ids[i]:i})
        #THIS ONE IS FOR THE AGE IDS
        dic3 = {}
        for i  in range(len(self.list_test_ages)):
            dic3.update({self.list_test_ages[i]:i})
        
        for i in range(len(self.labels)):
            
            if(self.images[i][2] in b):

                self.all_test_list.append([dic2[self.images[i][0]],self.images[i][1],self.images[i][2],dic3[self.images[i][3]],self.images[i][4],self.images[i][5]])
                    
                if (self.images[i][4] == 2013):
                    self.test_query_list.append([dic2[self.images[i][0]],self.images[i][1],self.images[i][2],dic3[self.images[i][3]],self.images[i][4],self.images[i][5]])
                    #count_query_test = count_query_test + 1
                    
                if(self.images[i][4] == 2004 or self.images[i][4] == 2005 or self.images[i][4] == 2006):
                    self.test_gall1_list.append([dic2[self.images[i][0]],self.images[i][1],self.images[i][2],dic3[self.images[i][3]],self.images[i][4],self.images[i][5]])
                    #count_sub1_test = count_sub1_test + 1 
               
                if(self.images[i][4] == 2007 or self.images[i][4] == 2008 or self.images[i][4] == 2009):
                    self.test_gall2_list.append([dic2[self.images[i][0]],self.images[i][1],self.images[i][2],dic3[self.images[i][3]],self.images[i][4],self.images[i][5]])
                    #count_sub2_test = count_sub2_test + 1
               
                if(self.images[i][4] == 2010 or self.images[i][4] == 2011 or self.images[i][4] == 2012):
                    self.test_gall3_list.append([dic2[self.images[i][0]],self.images[i][1],self.images[i][2],dic3[self.images[i][3]],self.images[i][4],self.images[i][5]])
        #THIS IS FOR THE VALID SET:		                
        c = range(6,15)
        dic4 ={}
        #THIS ONE FOR THE IDS
        for i in range(len(self.list_valid_ids)):
            dic4.update({self.list_valid_ids[i]:i})
        #THIS ONE IS FOR THE AGE IDS
        dic5 = {}
        for i  in range(len(self.list_valid_ages)):
            dic5.update({self.list_valid_ages[i]:i})
        
        for i in range(len(self.labels)):
            
            if(self.images[i][2] in c):

                    #THIS ONE ADDS ALL THE INFORMATION AND THERE  
                self.all_valid_list.append([dic4[self.images[i][0]],self.images[i][1],self.images[i][2],dic5[self.images[i][3]],self.images[i][4],self.images[i][5]])
                
                #THIS ONE CONTAINS ALL THE QUERY IMAGES IN THE VALID SET
                if (self.images[i][4] == 2013):
                    self.valid_query_list.append([dic4[self.images[i][0]],self.images[i][1],self.images[i][2],dic5[self.images[i][3]],self.images[i][4],self.images[i][5]])
                  #THIS ONE CONTAINS ALL THE 1st GALLERY IMAGES IN THE VALID SET
                if(self.images[i][4] == 2004 or self.images[i][4] == 2005 or self.images[i][4] == 2006):
                    self.valid_gall1_list.append([dic4[self.images[i][0]],self.images[i][1],self.images[i][2],dic5[self.images[i][3]],self.images[i][4],self.images[i][5]])
                 #THIS ONE CONTAINS ALL THE 2nd GALLERY IMAGES IN THE VALID SET
                if(self.images[i][4] == 2007 or self.images[i][4] == 2008 or self.images[i][4] == 2009):
                    self.valid_gall2_list.append([dic4[self.images[i][0]],self.images[i][1],self.images[i][2],dic5[self.images[i][3]],self.images[i][4],self.images[i][5]])
                 #THIS ONE CONTAINS ALL THE 3rd GALLERY IMAGES IN THE VALID SET
                if(self.images[i][4] == 2010 or self.images[i][4] == 2011 or self.images[i][4] == 2012):
                    self.valid_gall3_list.append([dic4[self.images[i][0]],self.images[i][1],self.images[i][2],dic5[self.images[i][3]],self.images[i][4],self.images[i][5]])
       
    def __len__(self):

        #THIS IS FOR THE TRAINING PART
        if self.istrain is True and self.isvalid is False and self.isquery is False and self.isgall1 is False and self.isgall2 is False and self.isgall3 is False:
            return len(self.all_train_list)
    
        #THIS IS THE VALID PART
        if self.istrain is False and self.isvalid is True and  self.isquery is True and self.isgall1 is False and self.isgall2 is False and self.isgall3 is False:
            return len(self.valid_query_list)
        if self.istrain is False and self.isvalid is True and self.isquery is False and self.isgall1 is True and self.isgall2 is False and self.isgall3 is False:
            return len(self.valid_gall1_list)
        if self.istrain is False and self.isvalid is True  and self.isquery is False and self.isgall1 is False and self.isgall2 is True and self.isgall3 is False:
            return len(self.valid_gall2_list)
        if self.istrain is False and self.isvalid is True and self.isquery is False and self.isgall1 is False and self.isgall2 is False and self.isgall3 is True:
            return len(self.valid_gall3_list)
    
        #THIS IS FOR THE TESTING PART
        if self.istrain is False and self.isvalid is False and self.isquery is True and self.isgall1 is False and self.isgall2 is False and self.isgall3 is False:
            return len(self.test_query_list)
        if self.istrain is False and self.isvalid is False and self.isquery is False and self.isgall1 is True and self.isgall2 is False and self.isgall3 is False:
            return len(self.test_gall1_list)
        if self.istrain is False and self.isvalid is False and self.isquery is False and self.isgall1 is False and self.isgall2 is True and self.isgall3 is False:
            return len(self.test_gall2_list)
        if self.istrain is False and self.isvalid is False and self.isquery is False and self.isgall1 is False and self.isgall2 is False and self.isgall3 is True:
            return len(self.test_gall3_list)
            
       

    def __getitem__(self, i):
         
        # THIS IS THE TRAINING PART
        if self.istrain is True and self.isvalid is False and self.isquery is False and self.isgall1 is False and self.isgall2 is False and self.isgall3 is False: 

            #This will contain the image part
            file1 = self.all_train_list[i][5]
            #print('file1 is:',file1) 
            #This will contain the age part 
            age_part = self.all_train_list[i][3]
            #print('age_part is:',age_part)
            label = self.all_train_list[i][0] 
            #print('label is:',label)
            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')

                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label
        
        #THIS IS THE VALID PART
        if self.istrain is False and self.isvalid is True and self.isquery is True and self.isgall1 is False and self.isgall2 is False and self.isgall3 is False:

            #This will contain the image part
            file1 = self.valid_query_list[i][5]
            #This will contain the age part 
            age_part = self.valid_query_list[i][3]

            label = self.valid_query_list[i][0] 

            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')

                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label
       
       


        if self.istrain is False and self.isvalid is True and self.isquery is False and self.isgall1 is True and self.isgall2 is False and self.isgall3 is False:    

            #This will contain the image part
            file1 = self.valid_gall1_list[i][5]
            #This will contain the age part 
            age_part = self.valid_gall1_list[i][3]

            label = self.valid_gall1_list[i][0] 

            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')

                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label


        if self.istrain is False and self.isvalid is True and self.isquery is False and self.isgall1 is False and self.isgall2 is True and self.isgall3 is False:
        
            #This will contain the image part
            file1 = self.valid_gall2_list[i][5]
            #This will contain the age part 
            age_part = self.valid_gall2_list[i][3]

            label = self.valid_gall2_list[i][0]

            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')

                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label

        if self.istrain is False and self.isvalid is True and self.isquery is False and self.isgall1 is False and self.isgall2 is False and self.isgall3 is True:

            #This will contain the image part
            file1 = self.valid_gall3_list[i][5]
            #This will contain the age part 
            age_part = self.valid_gall3_list[i][3]

            label = self.valid_gall3_list[i][0]

            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')

                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label


        #THIS IS THE TEST PART
        
        if self.istrain is False and self.isvalid is False and  self.isquery is True and self.isgall1 is False and self.isgall2 is False and self.isgall3 is False:  

            #This will contain the image part
            file1 = self.test_query_list[i][5]
            #This will contain the age part 
            age_part = self.test_query_list[i][3]

            label = self.test_query_list[i][0] 

            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')
 
                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label
       
        if self.istrain is False and self.isvalid is False and self.isquery is False and self.isgall1 is True and self.isgall2 is False and self.isgall3 is False: 

            #This will contain the image part
            file1 = self.test_gall1_list[i][5]
            #This will contain the age part 
            age_part = self.test_gall1_list[i][3]

            label = self.test_gall1_list[i][0] 

            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')

                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label


        if self.istrain is False and self.isvalid is False and self.isquery is False and self.isgall1 is False and self.isgall2 is True and self.isgall3 is False:
            #print('I am in the gall2:')
            #This will contain the image part
            file1 = self.test_gall2_list[i][5]
            #print('The image:',file1)
            #This will contain the age part 
            age_part = self.test_gall2_list[i][3]
            #print('The age part:',age_part)
            label = self.test_gall2_list[i][0]
            #print('The label:',label)
            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')
                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label
       
        if self.istrain is False and self.isvalid is False and self.isquery is False and self.isgall1 is False and self.isgall2 is False and self.isgall3 is True:
        
            #This will contain the image part
            file1 = self.test_gall3_list[i][5]
            #This will contain the age part 
            age_part = self.test_gall3_list[i][3]

            label = self.test_gall3_list[i][0]

            path1 = os.path.join(self.root_path, file1)
            if os.path.exists(path1):
                x = Image.open(path1).convert('L')
                if self.transform:
                    x =  self.transform(x)

                return x,age_part,label























