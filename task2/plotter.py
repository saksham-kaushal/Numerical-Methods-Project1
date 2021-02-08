import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

def q_i(df):
	print('\n')
	print(df.name, ':')
	cols = ['retrieved_abs_mag','true_abs_mag']
	for col in cols:
		print(col,'mean =',df[col].mean())
		print(col,'stddev =',df[col].std())
	return

def q_ii(df):
	cols=['retrieved_abs_mag','true_abs_mag']
	cols.append('dist_category')
	print('\n')
	print('Mean :')
	print(df[cols].groupby('dist_category').mean())
	print('\n')
	print('Dispersion :')
	print(df[cols].groupby('dist_category').std())

def q_a(df,columns):
	# plt.clf()
	sns.set()
	# palette = ['#ffd66b','#522d5b']
	palette = sns.cubehelix_palette(2,rot=0.4,dark=0.3,light=0.75)
	bins = np.arange(0,df[columns].max().max(),200)
	sns.displot(data=df[columns],kind='hist',palette=palette,bins=bins,legend=False,aspect=2)
	plt.xlabel('Distance (in parsecs)', fontsize=9)
	plt.ylabel('Count', fontsize=9)
	plt.legend(labels=['True distance','Distance retrieved from parallax measurements'], fontsize=9)
	# plt.show()
	plt.savefig('./plots/hist_dist_true-retrieved.jpg',bbox_inches='tight',pad_inches=0.5,dpi=480)
	return

def q_b(df):
	sns.set()
	sns.relplot(data=df,x='retrieved_dist',y='retrieved_abs_mag',kind='scatter',color='#827397',s=5,linewidth=0.05,aspect=2)
	plt.xlabel('Distance retrieved from parallax measurements (in parsecs)', fontsize=9)
	plt.ylabel('Absolute magnitude retrieved from parallax measurements', fontsize=9)
	# plt.show()
	plt.savefig('./plots/scatter_retrieved_dist-abs_mag.jpg',bbox_inches='tight',pad_inches=0.5,dpi=480)
	return

def q_c(df):
	sns.set()
	# palette = ['#fff0d7','#4dabab','#1089b1','#baeaf4']
	palette = sns.cubehelix_palette(4,rot=0.4,dark=0.75,light=0.1)
	bins = np.linspace(df['retrieved_abs_mag'].min(),df['retrieved_abs_mag'].max(),50)
	plot = sns.displot(data=df,x='retrieved_abs_mag',kind='hist',hue='dist_category',\
		bins=bins,palette=palette,legend=True,aspect=2)
	plt.xlabel('Absolute magnitude retrieved from parallax measurements', fontsize=9)
	plt.ylabel('Count', fontsize=9)
	plot._legend.set_title('Distance range')
	plt.savefig('./plots/hist_retrieved_absmag.jpg',bbox_inches='tight',pad_inches=0.5,dpi=480)
	sns.set(rc={'legend.frameon':True})
	grid= sns.FacetGrid(data=df,col='dist_category',sharey=False,\
		palette=palette,aspect=2,hue='dist_category',col_wrap=2, margin_titles=True,legend_out=True)
	grid.map_dataframe(sns.histplot,x='retrieved_abs_mag',legend=True,bins=bins)
	grid.set_axis_labels('Absolute magnitude retrieved from parallax measurements','Count',fontsize=9)
	grid.set_titles(col_template="{col_name}", row_template="{row_name}")
	plt.savefig('./plots/hist_individual_retrieved_absmag.jpg',bbox_inches='tight',pad_inches=0.5,dpi=480)
	# plt.show()
	return

#------------------ Main --------------------------------

fname = 'LK.dat'
col_names = ['true_parallax','true_dist','apparent_mag','observed_parallax','parallax_err','retrieved_dist','true_abs_mag','retrieved_abs_mag','photometric_err']

df = pd.read_csv(fname, delim_whitespace=True, header=None, names=col_names, skiprows=15)
df = df[df['retrieved_abs_mag']!=99.0]
df = df[df['retrieved_dist']<=4000]
df.name = '0-4000pc'
bins = [0,1000,2000,3000,4000]
categories = ['upto 1kpc distance','1-2kpc distance range','2-3kpc distance range', '3-4kpc distance range']
df['dist_category']=pd.cut(df['retrieved_dist'],bins=bins,labels=categories)

q_i(df)
q_ii(df)
q_a(df,['retrieved_dist','true_dist'])
q_b(df)
q_c(df)