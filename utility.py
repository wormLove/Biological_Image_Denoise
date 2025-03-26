import os
import cv2
import datetime
import numpy as np
import tifffile as tiff
from tqdm import tqdm

def write_file(f, data):
    f = open(f, 'a')
    f.write(str(data) + '\n')
    f.close()

def get_timestamp():
    ct = datetime.datetime.now()
    return ct.strftime("%Y%m%d-%H%M%S")

def print_dict(d):
    for key, value in d.items():
        print('\t' + str(key).ljust(30, ' ') + str(value))

def find_connected_components(channel):
    ret, thresh = cv2.threshold(channel, 1, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    return labels, num_labels-1

def save_mtx_png(mtx, image_path):
    binary_matrix = (mtx > 0).astype(int) * 255
    cv2.imwrite(image_path, binary_matrix)

def save_rgb_png(mtx, chidx_list, channel_name_list, image_path, gen_overlap):
    input_channel_order = list(channel_name_list)
    channel_name_to_index = {input_channel_order[i]: i for i in range(3)}

    output_map = {
        channel_name_to_index['R']: 2,
        channel_name_to_index['G']: 1,
        channel_name_to_index['B']: 0
    }

    binary_matrix = np.zeros_like(mtx)
    for chidx in chidx_list:
        mapped_channel = output_map[chidx]
        binary_matrix[mapped_channel] = (mtx[chidx] > 0).astype(int) * 255
    binary_matrix = np.transpose(binary_matrix, (1, 2, 0))
    cv2.imwrite(image_path, binary_matrix.astype(np.uint8))

    if gen_overlap != 'True':
        return 0

    print('Calculating Overlap...')
    overlap_info_file = image_path.split('.')[0]+'_overlap_info.txt'
    green_labels, g_total_count = find_connected_components(binary_matrix[:, :, 1].astype(np.uint8))
    red_labels, r_total_count = find_connected_components(binary_matrix[:, :, 2].astype(np.uint8))

    result_matrix = np.zeros_like(binary_matrix)
    overlap_centroids = []
    overlap_count = 0

    for g_label in tqdm(np.unique(green_labels)[1:]):
        green_mask = green_labels == g_label
        if np.max(binary_matrix[:, :, 2][green_mask]) > 0:
            result_matrix[:, :, 1][green_mask] = binary_matrix[:, :, 1][green_mask]

            red_mask_in_green_area = binary_matrix[:, :, 2][green_mask] > 0
            coords = np.column_stack(np.where(green_mask))
            coords_in_red_area = coords[red_mask_in_green_area]
            centroid = coords_in_red_area.mean(axis=0)
            overlap_centroids.append(centroid)
            overlap_count += 1

    for r_label in tqdm(np.unique(red_labels)[1:]):
        red_mask = red_labels == r_label
        if np.max(binary_matrix[:, :, 1][red_mask]) > 0:
            result_matrix[:, :, 2][red_mask] = binary_matrix[:, :, 2][red_mask]

    overlap_g_ratio = overlap_count / g_total_count if g_total_count > 0 else 0
    overlap_r_ratio = overlap_count / r_total_count if r_total_count > 0 else 0

    with open(overlap_info_file, 'w') as f:
        f.write("overlap_centroid_coordinate:\n")
        for centroid in overlap_centroids:
            f.write(f"{centroid[0]:.2f}, {centroid[1]:.2f}\n")
        
        f.write(f"G channel count: {g_total_count}\n")
        f.write(f"R channel count: {r_total_count}\n")
        f.write(f"Overlap count: {overlap_count}\n")
        f.write(f"Overlap in G ratio: {overlap_g_ratio:.2%}\n")
        f.write(f"Overlap in R ratio: {overlap_r_ratio:.2%}\n")

    cv2.imwrite(image_path.split('.')[0]+'_overlap.png', result_matrix.astype(np.uint8))
    tiff.imwrite(image_path.split('.')[0]+'_overlap.tif', result_matrix.astype(np.uint8))

def save_mtx_tiff(mtx, image_path):
    tiff.imwrite(image_path, mtx)

def print_Stat(mtx, save_tend = False):
    flattened_data = np.sort(mtx.ravel())[::-1]
    mean_value = np.mean(flattened_data)
    std_deviation = np.std(flattened_data)
    print('Shape: ' + str(mtx.shape))
    print('Value Range: ' + str(np.min(flattened_data)) + '~' + str(np.max(flattened_data)))
    print('Mean:' + str(round(mean_value,4)) + ' STD:' + str(round(std_deviation,4)))
    print('Zero Rate: ' + str(round(np.sum(flattened_data == 0)/len(flattened_data), 4)*100)[:5] + '%')

    
