import os
import ast
import cv2
import shutil
import argparse
import configparser
import numpy as np
import seaborn as sns
import tifffile as tiff
import matplotlib.pyplot as plt
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import utility as util
import filters as filters

def get_config_info(args):
	'''
		Get the information from configure file
	'''
	config = configparser.ConfigParser(allow_no_value=True)
	config.read(args.Config)

	arg_dict = {}
	if len(args.FilePath) > 0:
		arg_dict['file'] = args.FilePath
	else:
		arg_dict['file'] = config['basic_setting']['FilePath']

	arg_dict['channel_name_list'] = list(config['basic_setting']['channel_name_list'])
	arg_dict['action'] = args.Action
	arg_dict['cfg_file'] = args.Config
	arg_dict['KeepIntermedia'] = args.KeepIntermedia

	if len(args.OutDir) > 0:
		arg_dict['outdir'] = args.OutDir
	elif 'OutDir' in config['basic_setting'].keys():
		arg_dict['outdir'] = config['basic_setting']['OutDir']
	else:
		arg_dict['outdir'] = os.getcwd()

	util.print_dict(arg_dict)

	if 'd' in arg_dict['action']:
		arg_dict['denoise_setting'] = {}
		for key in config['denoise_setting']:
			arg_dict['denoise_setting'][key] = config['denoise_setting'][key]

		if arg_dict['denoise_setting']['extrema_filter']:
			arg_dict['extrema_filter'] = {}
			for key in config['extrema_filter']:
				arg_dict['extrema_filter'][key] = config['extrema_filter'][key]

		if arg_dict['denoise_setting']['adaptive_threshold_filter']:
			arg_dict['adaptive_threshold_filter'] = {}
			for key in config['adaptive_threshold_filter']:
				arg_dict['adaptive_threshold_filter'][key] = config['adaptive_threshold_filter'][key]

		if arg_dict['denoise_setting']['morphology_operations']:
			arg_dict['morphology_operations'] = {}
			for key in config['morphology_operations']:
				arg_dict['morphology_operations'][key] = config['morphology_operations'][key]

		if arg_dict['denoise_setting']['circularity_filter']:
			arg_dict['circularity_filter'] = {}
			for key in config['circularity_filter']:
				arg_dict['circularity_filter'][key] = config['circularity_filter'][key]

	return arg_dict

def get_stat(mtx, channel_name, page, temp_dir, y_curr):
	flattened_data = np.sort(mtx.ravel())[::-1]
	mean_value = np.mean(flattened_data)
	std_deviation = np.std(flattened_data)

	info_list = []
	info_list.append(channel_name + ' Channel Info:')
	info_list.append('- Shape: ' + str(mtx.shape))
	info_list.append('- Zero Rate: ' + str(round(np.sum(flattened_data==0)/len(flattened_data), 4)*100)[:5] + '%')
	info_list.append('- Mean:' + str(round(mean_value,4)) + '    STD:' + str(round(std_deviation,4)))
	info_list.append('- Value Range: ' + str(np.min(flattened_data)) + '~' + str(np.max(flattened_data)))

	for info in info_list:
		page.drawString(100, y_curr, info)
		y_curr -= 20

	y_curr -= 250
	x_axis = np.arange(len(flattened_data))
	plt.figure(figsize=(12, 6))
	plt.plot(x_axis, flattened_data, color='blue', linewidth=0.5)
	plt.yscale('log')
	plt.xscale('log')
	plt.axhline(y=mean_value, color='green', linestyle='--', linewidth=1, label='Mean')
	plt.text(0.95, mean_value, 'Mean: {:.2f}'.format(mean_value), 
		ha='right', va='bottom', transform=plt.gca().get_yaxis_transform(), color='green')
	plt.axhline(y=mean_value + std_deviation, color='red', linestyle='--', linewidth=1, label='Mean + 1 SD')
	plt.text(0.95, mean_value + std_deviation, 'Mean + 1 SD: {:.2f}'.format(mean_value + std_deviation), 
		ha='right', va='bottom', transform=plt.gca().get_yaxis_transform(), color='red')
	plt.axhline(y=mean_value + 2 * std_deviation, color='purple', linestyle='--', linewidth=1, label='Mean + 2 SD')
	plt.text(0.95, mean_value + 2 * std_deviation, 'Mean + 2 SD: {:.2f}'.format(mean_value + 2 * std_deviation), 
		ha='right', va='bottom', transform=plt.gca().get_yaxis_transform(), color='purple')
	plt.xlabel('Index')
	plt.ylabel('Values')
	plt.grid(True)
	plt.savefig(os.path.join(temp_dir, channel_name+' Value Distribution.png'))
	plt.close()
	page.drawImage(os.path.join(temp_dir, channel_name+' Value Distribution.png'), 50, y_curr, width=500, height=250)
	y_curr -= 20
	return y_curr


def main(args):
	arg_dict = get_config_info(args)

	image_name = os.path.basename(arg_dict['file']).split('.')[0]
	data = tiff.imread(arg_dict['file'])
	output_dir = os.path.join(arg_dict['outdir'], image_name+'-'+util.get_timestamp())
	temp_dir = os.path.join(output_dir, 'TEMP')
	os.makedirs(temp_dir, exist_ok=True)

	if 's' in arg_dict['action']:
		c = canvas.Canvas(os.path.join(output_dir,'channel_stat_report.pdf'), pagesize=letter)
		for channel_idx in range(data.shape[0]):
			y_curr = 700
			y_curr = get_stat(data[channel_idx], arg_dict['channel_name_list'][channel_idx], c, temp_dir, y_curr)
			if channel_idx < data.shape[0]-1:
				c.showPage()
		c.save()

	if 'd' in arg_dict['action']:
		print('De-noise setting:')
		util.print_dict(arg_dict['denoise_setting'])
		chidx_list = ast.literal_eval(arg_dict['denoise_setting']['channel_plan'])

		data_filtered = np.copy(data)

		if arg_dict['denoise_setting']['extrema_filter'] == 'True':
			print('Extrema_filter parameter setting:')
			filter_name = 'extrema_filter'
			util.print_dict(arg_dict[filter_name])
			for chidx in chidx_list:
				data_filtered[chidx] = filters.extrema_filter(
											data_filtered[chidx], 
											upper_limit = int(arg_dict[filter_name]['max_thre']), 
											base_value = arg_dict[filter_name]['base_value'],
											std_multi = int(arg_dict[filter_name]['std_multi']))
				if arg_dict['KeepIntermedia']=='True':
					util.save_mtx_png(data_filtered[chidx].astype(np.uint8), 
									  os.path.join(temp_dir, filter_name+'_CH'+str(chidx)+'.png'))

		if arg_dict['denoise_setting']['adaptive_threshold_filter'] == 'True':
			print('Adaptive_threshold_filter parameter setting:')
			filter_name = 'adaptive_threshold_filter'
			util.print_dict(arg_dict[filter_name])
			for chidx in chidx_list:
				data_filtered[chidx] = filters.adaptive_thre_Filter(
											data_filtered[chidx], 
											filter_size = int(arg_dict[filter_name]['filter_size']), 
											muitl_mean = int(arg_dict[filter_name]['mean_multi']))
				if arg_dict['KeepIntermedia']=='True':
					util.save_mtx_png(data_filtered[chidx].astype(np.uint8), 
									  os.path.join(temp_dir, filter_name+'_CH'+str(chidx)+'.png'))

		if arg_dict['denoise_setting']['morphology_operations'] == 'True':
			print('Morphology_operations parameter setting:')
			filter_name = 'morphology_operations'
			util.print_dict(arg_dict[filter_name])
			for chidx in chidx_list:
				data_filtered[chidx] = filters.morph_op(
											data_filtered[chidx],
											rank = int(arg_dict[filter_name]['kernal_rank']), 
											connectivity = int(arg_dict[filter_name]['connectivity']),
											opening_operation = arg_dict[filter_name]['opening_operation'],
											closing_operation = arg_dict[filter_name]['closing_operation'])
				if arg_dict['KeepIntermedia']=='True':
					util.save_mtx_png(data_filtered[chidx].astype(np.uint8), 
									  os.path.join(temp_dir, filter_name+'_CH'+str(chidx)+'.png'))

		if arg_dict['denoise_setting']['circularity_filter'] == 'True':
			print('Circularity_filter parameter setting:')
			filter_name = 'circularity_filter'
			util.print_dict(arg_dict[filter_name])
			for chidx in chidx_list:
				data_filtered[chidx] = filters.circularity_Filter(
											data_filtered[chidx],
											circularity_thre = float(arg_dict[filter_name]['circularity_thre']),
											area_thre = int(arg_dict[filter_name]['area_thre']))
				if arg_dict['KeepIntermedia']=='True':
					util.save_mtx_png(data_filtered[chidx].astype(np.uint8), 
									  os.path.join(temp_dir, filter_name+'_CH'+str(chidx)+'.png'))

		util.save_mtx_tiff(data_filtered, 
			os.path.join(output_dir, image_name+'_filtered.tif'))
		util.save_rgb_png(data_filtered, chidx_list, arg_dict['channel_name_list'],
			os.path.join(output_dir, image_name+'_filtered.png'), 
			arg_dict['denoise_setting']['gen_overlap'])
			

	if arg_dict['KeepIntermedia']=='False':
		shutil.rmtree(temp_dir)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='DeNoise Pipeline')
	parser.add_argument('--FilePath', type=str, default='',
						help='Path to your image file.')
	parser.add_argument('--Action', type=str, default='d',
						help='s for statistics, d for de-noise, sd or ds will do statistics and de-noise.')
	parser.add_argument('--Config', type=str, default='args.cfg',
						help='Path to your configure file.')
	parser.add_argument('--KeepIntermedia', type=str, default='True',
						help='If set to True, all intermedia result will be kept.')
	parser.add_argument('--OutDir', type=str, default='',
						help='Path of your output.')

	args = parser.parse_args()
	main(args)





