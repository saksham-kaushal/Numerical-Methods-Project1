import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

#----------------- General purpose functions ------------------

def split_data(df, col, bins):
	df_list=[]
	for i in range(len(bins)-1) :
		df_list.append(df[(df[col]>bins[i]) & (df[col]<=bins[i+1])])
		df_list[i].name = str(bins[i])+'-'+str(bins[i+1])+'pc'
	return df_list

def get_stats(df, col=None):
	print(df.name,':')
	if col==None:
		print(df.mean())
		print(df.std())
	else:
		print(col,'mean =',df[col].mean())
		print(col,'stddev =',df[col].std())
	return

def scatter(df,x,y):
	plt.clf()
	sns.set()
	sns.relplot(x=x,y=y, data=df, kind='scatter', marker='.',linewidth=0.1,aspect=1.5,s=7)
	return

def distance_hist(df,parameters):
	plt.clf()
	sns.set()
	palette = ['#ffd56b','#350b40']
	bins = np.arange(0,df[parameters].max().max(),200)
	sns.displot(df[parameters], palette=palette, bins=bins,kind='hist',legend=False, aspect=2)
	return

def mag_hist(df):
	plt.clf()
	sns.set()
	palette = ['#005086','#318fb5','#f7d6bf','#b0cac7']
	bins = np.linspace(df.min().min(),df.max().max(),70)
	sns.displot(df,palette=palette,kind='hist',legend=False,aspect=2,alpha=0.7,bins=bins)
	# legend = axis._legend
	# legend.set_title('Distance range')
	return

def individual_mag_hists(df):
	plt.clf()
	sns.set()
	palette = ['#005086','#318fb5','#f7d6bf','#b0cac7']
	# bins = np.linspace(df.min().min(),df.max().max(),70)
	# fig, axes = plt.subplots(2,2)
	# fig.suptitle('Histograms plotted separately')
	sns.displot(df,x='retrieved_abs_mag',palette=palette,kind='hist',legend=False,aspect=2,alpha=0.7,hue='dist_category')
	# for i in range(4):
	# 	sns.displot(df[list(df.columns)[i][:]], ax=axes[i//2,i%2], color=palette[i],kind='hist',legend=False,aspect=2,alpha=0.7,bins=bins)
	plt.show()

#-------------------Question based functions-------------------------

def q_i(df):
	get_stats(df,'retrieved_abs_mag')
	get_stats(df,'true_abs_mag')
	return

def q_ii(df_list):
	for bin_data in df_list:
		get_stats(bin_data, 'retrieved_abs_mag')
		get_stats(bin_data, 'true_abs_mag')
	return

def q_a(df):
	distance_hist(df,['retrieved_dist','true_dist'])
	plt.xlabel('Distance (in parsecs)', fontsize=9)
	plt.ylabel('Count', fontsize=9)
	plt.legend(labels=['True distance','Distance retrieved from parallax measurements'], fontsize=9)
	plt.savefig('hist_dist_true-retrieved.jpg',bbox_inches='tight',pad_inches=0.5,dpi=480)
	return

def q_b(df):
	scatter(df,'retrieved_dist','retrieved_abs_mag')
	plt.xlabel('Distance retrieved from parallax measurements (in parsecs)', fontsize=9)
	plt.ylabel('Absolute magnitude retrieved from parallax measurements', fontsize=9)
	# plt.plot(figsize=(7,5),dpi=100)
	plt.savefig('scatter_retrieved_dist-abs_mag.jpg',bbox_inches='tight',pad_inches=0.5,dpi=480)
	return

def q_c(df_list):
	parameter = 'retrieved_abs_mag'
	mag_df = pd.concat([df[parameter] for df in df_list],axis=1,keys=[i.name for i in df_list])
	print([i.name for i in df_list])
	mag_hist(mag_df)
	plt.xlabel('Absolute magnitude retrieved from parallax measurements', fontsize=9)
	plt.ylabel('Count', fontsize=9)
	colnames=mag_df.columns.values.tolist()
	print(colnames[::-1])
	plt.legend(labels=colnames[::-1], fontsize=9, title='Distance range')
	plt.savefig('hist_retrieved_absmag.jpg',bbox_inches='tight',pad_inches=0.5,dpi=480)
	# individual_mag_hists(mag_df)
	# plt.show()
	return

def q_c_test(df):
	bins = [0,1000,2000,3000,4000]
	categories = ['upto 1kpc distance','1-2kpc distance range','2-3kpc distance range', '3-4kpc distance range']
	df['dist_category'] = pd.cut(df['retrieved_dist'],bins,labels=categories)
	print(df.dtypes)
	individual_mag_hists(df)
	return

fname = 'LK.dat'
col_names = ['true_parallax','true_dist','apparent_mag','observed_parallax','parallax_err','retrieved_dist','true_abs_mag','retrieved_abs_mag','photometric_err']

df = pd.read_csv(fname, delim_whitespace=True, header=None, names=col_names, skiprows=13)
df = df[df['retrieved_abs_mag']!=99.0]
df = df[df['retrieved_dist']<=4000]
df.name = '4000pc'
df_list = split_data(df,'retrieved_dist',[0,1000,2000,3000,4000])

print('(i)')
q_i(df)
print('\n')
print('(ii)')
q_ii(df_list)
q_a(df)
q_b(df)
q_c(df_list)
q_c_test(df)

# print(split_data(df,'retrieved_dist',[0,1000,2000,3000,4000]))
# print('true_abs_mag mean = ',df[].mean())
# print('true_abs_mag stddev = ',df['true_abs_mag'].std())
# print('retrieved_abs_mag mean =',df['retrieved_abs_mag'].mean())
# print('retrieved_abs_mag stddev =',df['retrieved_abs_mag'].std())
# plt.show()