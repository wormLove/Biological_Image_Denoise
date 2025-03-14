import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter
from scipy.ndimage import binary_opening, binary_closing, generate_binary_structure

def extrema_filter(mtx, upper_limit=10000, base_value = 'median', std_multi=1):
	mtx[mtx > upper_limit] = 0

	positive_values = mtx[mtx > 0]
	if base_value == 'median':
		base_value = np.median(positive_values)
	elif base_value == 'mean':
		base_value = np.mean(positive_values)
	else:
		base_value = 0
	std = np.std(mtx)
	mtx[mtx < (base_value + std_multi*std)] = 0

	return mtx

def adaptive_thre_Filter(mtx, filter_size = 50, muitl_mean = 5):
	local_mean = uniform_filter(mtx, size=filter_size)
	adaptive_threshold = 5 * local_mean
	mtx[mtx < adaptive_threshold] = 0
	return mtx

def morph_op(mtx, rank=2, connectivity=2, opening_operation=True, closing_operation=True):
	s_square = generate_binary_structure(rank, connectivity)
	morph_data = np.copy(mtx)

	if opening_operation == 'True':
		morph_data = binary_opening(morph_data, structure=s_square)
	if closing_operation == 'True':
		morph_data = binary_closing(morph_data, structure=s_square)

	if opening_operation == 'True' or closing_operation == 'True':
		return mtx * morph_data
	else:
		return mtx

def circularity_Filter(mtx, circularity_thre = 0.75, area_thre = 10):
	binary_mtx = (mtx > 0).astype(np.uint8)*255
	contours, _ = cv2.findContours(binary_mtx, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	filtered_mtx = np.zeros_like(binary_mtx)

	for contour in contours:
		area = cv2.contourArea(contour)
		perimeter = cv2.arcLength(contour, True)
		circularity = 4 * np.pi * (area / (perimeter ** 2)) if perimeter != 0 else 0

		if area > area_thre and circularity > circularity_thre:
			cv2.drawContours(filtered_mtx, [contour], -1, 255, thickness=cv2.FILLED)

	mtx[filtered_mtx == 0] = 0
	return mtx

