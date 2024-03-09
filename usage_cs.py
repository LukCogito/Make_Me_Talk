from preprocesing_functions_en import nacti_soubor_vypis_spec_znaky, najdi_spec_znaky
from preprocesing_functions_cs import nahrad_spec_znaky, nahrad_cisla_slovy

cesta = './data/fv1.txt'

#nacti_soubor_vypis_spec_znaky(cesta)

nahrad_cisla_slovy(cesta)
nahrad_spec_znaky(cesta)