import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.spatial import cKDTree
from skimage import measure, io, color
from scipy.stats import entropy

def estimate_local_holder(points, radii):
    tree = cKDTree(points)
    alphas = []

    for p in points:
        counts = []
        for r in radii:
            # count points inside ball of radius r
            cnt = len(tree.query_ball_point(p, r))
            counts.append(cnt)
        counts = np.array(counts)
        
        # log-log fit: log(N(r)) ~ alpha * log(r) + c
        valid = counts > 1
        if np.sum(valid) > 2:
            coeffs = np.polyfit(np.log(radii[valid]), np.log(counts[valid]), 1)
            alpha = coeffs[0]
        else:
            alpha = np.nan
        alphas.append(alpha)
    
    return np.array(alphas)

path_to_data = "/home/mello/Research/Organoids_complexity/Correlation_metabolites/data_new"
batches = sorted(list(os.listdir(path_to_data)))

stitched_data = pd.read_csv('Stitched_AR.csv')

result = []
for batch in batches:
    batch_name = batch.split('batch')[1]    
    days = sorted(list(os.listdir(path_to_data+'/'+batch)))
    for day in days:
        if day != 'Stitched':
            images = sorted(list(os.listdir(path_to_data+'/'+batch+'/'+day+'/predicted_masks/')))
        else:
            images = sorted(list(os.listdir(path_to_data+'/'+batch+'/'+day)))     
            
        for name in images:
            day_name = name.split('_')[3][2:]
            wells_name = name.split('_')[4]
            
            if 'stitched' in name:
                path2image = path_to_data+'/'+batch+'/'+day+'/predicted_masks/'+name
                print(name.split('.png')[0])
                xlen = stitched_data[stitched_data['Mask'] == name.split('_predmask.png')[0]].Width.to_numpy()[0]
                ylen = stitched_data[stitched_data['Mask'] == name.split('_predmask.png')[0]].Height.to_numpy()[0]
            else:
                path2image = path_to_data+'/'+batch+'/'+day+'/predicted_masks/'+name
            
            if batch_name == '1':
                if day_name == '24':
                    xlen = 1024
                    ylen = 768
                elif int(day_name) < 17:
                    xlen = 1128
                    ylen = 832           
                else:
                    xlen = 1128
                    ylen = 832
         
            elif batch_name == '3':
                xlen = 1920
                ylen = 1440
                            
            else:
                if int(day_name) < 17:
                    xlen = 1128
                    ylen = 832           
                else:
                    xlen = 1128
                    ylen = 832               
            

            image = cv2.imread(path2image,cv2.IMREAD_GRAYSCALE)            
            non_zero_pixels = np.count_nonzero(image)

            if non_zero_pixels > 1:
                dim = (xlen, ylen)
                img = cv2.resize(image, dim, interpolation=cv2.INTER_CUBIC)            
                # create contour
                ret, thresh = cv2.threshold(img, 30, 250, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(image=cv2.flip(thresh,1), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                c = max(contours, key = cv2.contourArea)          
                points = c.reshape(-1, 2)
                points = points[:, ::-1] 
                # Radii for sandbox scaling
                radii = np.logspace(0.5, 2.0, 10)  # from ~3 to 100 pixels
                alphas = estimate_local_holder(points, radii)

                hist, bin_edges = np.histogram(alphas, bins=10, density=True)
                p = hist / np.sum(hist)  # normalize to sum=1
                H = entropy(p, base=2)

                data_dict = {}
                data_dict['Filename'] = name
                data_dict['Day'] = day_name
                data_dict['Wells'] = wells_name
                data_dict['Batch'] = batch_name            
                data_dict['Complexity'] = max(alphas) - min(alphas)
                result.append(data_dict)
            else:
                continue
        
df = pd.DataFrame(result)
df.to_excel('Multifractal_analysis_newData.xlsx')

