from __future__ import division

import time
import sys
import hists

from MODPlot import *

import logging
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.WARNING)

input_analysis_file = sys.argv[1]

plot_labels = { "data": "CMS 2010 Open Data", "pythia": "Pythia 8.215", "herwig": "Herwig 7", "sherpa": "Sherpa 2.2.0", "theory": "Theory (MLL)" }
plot_colors = {"theory": "red", "pythia": "blue", "herwig": "green", "sherpa": "purple", "pythia_post": "red", "data": "black", "data_post": "red"}

def get_key(keyword):

	'''
	if 'eta' in keyword:
		return 'eta'
	elif 'pT' in keyword:
		return 'pT'
	elif 'phi' in keyword:
		return 'phi'

	return keyword.split('_')[0]
	'''
	return keyword

def parse_file(input_file, pT_lower_cut=150., pT_upper_cut=20000., softdrop_pT_lower_cut=0., softdrop_pT_upper_cut=20000., eta_cut=2.4):
	
	# We read the file line by line, and for each line, we fill the corresponding histograms.
	# This is desirable to creating lists of values since this will not hold anything in memory. 

	all_hists = hists.all_hist_templates()

	keywords = []
	keywords_set = False

	
	with open(input_file) as infile:

		
		line_number = 0

		for line in infile:

			#if line_number > 50:
			if False:
				break

			line_number += 1

			try:
				numbers = line.split()

				if numbers[0] == "#" and (not keywords_set):
					keywords = numbers[2:]
					keywords_set = True

				elif numbers[0] == "Entry":

					pT_index = keywords.index("hardest_pT") + 1
					softdrop_pT_index = keywords.index("pT_after_SD") + 1
					eta_index = keywords.index("hardest_eta") + 1
					prescale_index = keywords.index("prescale") + 1
					phi_index = keywords.index("hardest_phi") + 1
					mul_index = keywords.index("mul_pre_SD") + 1
					zg_index = keywords.index("zg_10") + 1

					# if abs(float(numbers[eta_index])) < eta_cut and float(numbers[pT_index]) > pT_lower_cut and float(numbers[pT_index]) < pT_upper_cut and float(numbers[softdrop_pT_index]) > softdrop_pT_lower_cut and float(numbers[softdrop_pT_index]) < softdrop_pT_upper_cut:
					
					for i in range(len(keywords)):

						keyword = keywords[i]

						if keyword in all_hists.keys():
							# Loop through each individual hist in all_hists[key] and fill it only if the current line satisfies all the accompanying conditions.

							for mod_hist in all_hists[keyword]:
								if line_number == 10:
                                                                        print mod_hist
                                                                        print keyword
                                                                        print len(keywords)
								hist = mod_hist.hist()
								conditions = mod_hist.conditions()

								condition_satisfied = 1
								for condition_keyword, condition_function in conditions:
									keyword_index = keywords.index(condition_keyword) + 1
									condition_satisfied *= int( condition_function(float(numbers[keyword_index])) )
                                                                        #if line_number % 10000 == 0:
                                                                        #print line_number
                                                                        #print condition_keyword
                                                                        #print condition_satisfied
                                                                        

								condition_satisfied = bool(condition_satisfied)
								
								if condition_satisfied:
									if mod_hist.use_prescale():
                                                                                #print "in prescale"
                                                                                #print "prescale index"
                                                                                #print prescale_index
                                                                                #print float(numbers[prescale_index]) + 1
                                                                                #print float(numbers[prescale_index + 1])
										hist.fill_array( [float(numbers[i + 1])], [float(numbers[prescale_index])] )	 # + 1 because we ignore the first keyword "Entry".
									else:
										hist.fill_array( [float(numbers[i + 1])] )	 # + 1 because we ignore the first keyword "Entry".
								

						'''
						keyword = keywords[i]

						if key in all_hists.keys():

							print "tada"

							# Loop through each individual hist in all_hists[key] and fill it only if the current line satisfies all the accompanying conditions.
							for mod_hist in all_hists[key]:
								print mod_hist
								# all_hists[key].fill_array( [ float(numbers[i + 1]) ], [ float(numbers[prescale_index]) ] ) # + 1 because we ignore the first keyword "Entry".
						'''


			except:
				pass


                print "Lines {}".format(line_number)                
	return all_hists



input_analysis_file = sys.argv[1]

plot_types = ['error', 'hist', 'hist', 'hist']
colors = [ plot_colors['data'], plot_colors['pythia'], plot_colors['herwig'], plot_colors['sherpa'] ]
labels = [ plot_labels['data'], plot_labels['pythia'], plot_labels['herwig'], plot_labels['sherpa'] ]


start = time.time()

data_hists = parse_file(input_analysis_file, eta_cut=10.)
#pythia_hists = parse_file("/home/aashish/pythia_truth.dat", eta_cut=10.)
#herwig_hists = parse_file("/home/aashish/herwig_truth.dat", eta_cut=10.)
#sherpa_hists = parse_file("/home/aashish/sherpa_truth.dat", eta_cut=10.)

end = time.time()

print "Finished parsing all files in {} seconds. Now plotting them!".format(end - start)



def get_hist_list(var):
	# return [ data_hists[var], pythia_hists[var], herwig_hists[var], sherpa_hists[var] ]

	hists = []

	for i in range(len(data_hists[var])):
#		data_pythia_herwig_sherpa_hists = [ data_hists[var][i], pythia_hists[var][i], herwig_hists[var][i], sherpa_hists[var][i] ]
#		hists.append( data_pythia_herwig_sherpa_hists )
		data_only_hists = [ data_hists[var][i], data_hists[var][i], data_hists[var][i], data_hists[var][i] ]
		hists.append( data_only_hists )

	return hists



start = time.time()



# for pythia_hists,  in get_hist_list('hardest_pT'):


print "Plotting pT!"

pT_plot = MODPlot( get_hist_list('hardest_pT'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, multi_page=True, y_scale='log', ratio_plot=True, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="Jet $p_T$", y_label="A.U.")
pT_plot.plot("hardest_pT.pdf")





print "Plotting eta!"

#eta_plot = MODPlot( get_hist_list('hardest_eta'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, multi_page=True, ratio_plot=False, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="Jet $\eta$", y_label="A.U.", x_lims=(-5., 5.))
eta_plot = MODPlot( get_hist_list('hardest_eta'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, multi_page=True, ratio_plot=False, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="Jet $\eta$", y_label="A.U.")
eta_plot.plot("hardest_eta.pdf")




print "Plotting phi!"

#phi_plot = MODPlot( get_hist_list('hardest_phi'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, ratio_plot=False, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="Jet $\phi$", y_label="A.U.", x_lims=(0, 2*np.pi))
phi_plot = MODPlot( get_hist_list('hardest_phi'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, ratio_plot=False, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="Jet $\phi$", y_label="A.U.")
phi_plot.plot("hardest_phi.pdf")


print "Plotting constituent multiplicity!"

constituent_multiplicity_plot = MODPlot( get_hist_list('mul_pre_SD'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, ratio_plot=False, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="Constituent Multiplicity", y_label="A.U.")
constituent_multiplicity_plot.plot("constituent_multiplicity.pdf")


print "Plotting zg!"

#constituent_multiplicity_plot = MODPlot( get_hist_list('zg_10'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, ratio_plot=True, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="$z_g$", y_label="A.U.", x_lims=(0, 0.6))
constituent_multiplicity_plot = MODPlot( get_hist_list('zg_10'), plot_types=plot_types, plot_colors=colors, plot_labels=labels, ratio_plot=True, ratio_to_index=1, ratio_label="Ratio\nto\nPythia", x_label="$z_g$", y_label="A.U.")
constituent_multiplicity_plot.plot("zg.pdf")





end = time.time()

print "Finished all plotting in {} seconds.".format(end - start)


