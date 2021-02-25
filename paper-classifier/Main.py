import pandas as pd

from Visualizer_HiTi import Visualizer_HiTi
from Classifier import Classifier

w = Classifier()
v = Visualizer_HiTi()


series_hi_ti_mult_con = pd.Series([-1, 6, 7, 8, 198, 90, 172, 118, 55, 91, 70, 91, 251, 117, 279, 49, 150, 66, 344, 205, 234, 335, 556, 766, 1115, 614],
                                  index = ['1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'])

series_hi_ti_mult_con = series_hi_ti_mult_con.astype('float64')

series_amount_mult_con = pd.Series([8, 16, 25, 29, 376, 190, 344, 425, 264, 398, 322, 577, 655, 551, 894, 687, 713, 901, 1347, 1619, 2262, 1700, 2001, 3282, 4050, 3696],
                                   index = ['1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'])

series_amount_mult_con = series_amount_mult_con.astype('float64')

#result = w.grob_einordnen("arXiv_cs_ai_1993-2018")
#w.grob_einordnen("IJCAI_1997-2017")
#w.grob_einordnen("ECAI_2000-2016")

#v.create_radar_diagram(pd.read_csv("final.csv"))

#v.visualize_HI_vs_TI(series_hi_ti_mult_con.div(series_amount_mult_con), "arXiv>CS>AI, AAAI, IJCAI and ECAI", "mult_conf")

#hi_ti_icml = w.compare_hi_ti("ICML_1988-2019")
#v.visualize_HI_vs_TI(hi_ti_icml, "ICML", "icml")

hi_ti_aitpoics = w.compare_hi_ti("AITopics_1903-2018")
v.visualize_HI_vs_TI(hi_ti_aitpoics, "AITopics", "aitopics")
