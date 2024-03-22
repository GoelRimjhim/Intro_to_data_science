#Importing the required libraries

from sklearn.cluster import KMeans
import os
import pandas as pd
import numpy as np
from tqdm import tqdm

from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input

#Function for  pre-processing and extracting the image features

def image_features(directory):
    train = InceptionV3(weights='imagenet', include_top=False) 
    #for pre-processing, pre defined weights used for identifying the object from the image
    features = []  # list of features extracted
    image_name = []  # the image names
    for i in tqdm(directory):
        file_name=''+i   #  file name format in which images are present in the directory
        img=image.load_img(file_name,target_size=(224,224))
        x = img_to_array(img) #converting the image to array
        x=np.expand_dims(x,axis=0) # expanding the array for adding cluster information
        x=preprocess_input(x) # pre-processing the arrays
        feature=train.predict(x) # testing
        feature=feature.flatten()  # dimension reduction
        features.append(feature) # adding the features to the list
        image_name.append(i) #adding the image name to the list
    return features,image_name

#Getting the images from the directory, extracting the features and making the dataframe

file_path = os.getcwd() # the working directory
#print(path)
image_path=os.listdir('006')  #the files are named as '006..'
#print(img_path)
#extracting the features using the function defined in previous cell
image_features,image_name=image_feature(image_path)
# creating the pandas dataframe for the images
image_cluster = pd.DataFrame(image_name,columns=['Image name'])
#print(image_cluster)
  
#Applying k means

k = 2 #number of clusters to be formed
''' initial state for each iteration is chosen randomly
    max. number of iterations allowed for a single run = 10000000
    tolerance in clustering  = 1e-15
    Number of times the algorithm is run with different centroids = 500
    
'''
clusters = KMeans(k, random_state =None,max_iter=10000000,tol=1e-15,n_init=500)
clusters.fit(image_features) #computing the clusters from the extracted features
X = clusters.fit_transform(image_features)  # computing the distance from centroids
print(X)

#Visualising the results

image_cluster["Cluster Number"] = clusters.labels_ #adding labels to each cluster
print(image_cluster)