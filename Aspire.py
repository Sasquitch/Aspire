#Aspire mooring data
import os
from os.path import isfile, join
#from pandas import read_csv
from netCDF4 import Dataset
from netCDF4 import stringtochar
import numpy as np
import time

rawFileName = "sbe39_5527.asc"
file = open(rawFileName,'r')

netCDFfile = rawFileName[:-4] + '.nc'
nc = Dataset(netCDFfile, 'w', format = 'NETCDF4')

today = time.time()
today = ("File created on: ", time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(today)))

num_rows = 0
temperature = []
conductivity = []
pressure = []
date = []
time = []

#present in certain files but not others
"""
for cols in file: 
		num_rows += 1
		words = [words.split() for words in cols.splitlines()]
		if num_rows == 1:
			temperature.append(words[0][0])
			pressure.append(words[0][2])
		else:
			temperature.append(float(words[0][0]) + 273)
			pressure.append(float(words[0][2])*10)

		conductivity.append(words[0][1])
		
		date.append(words[0][3] + ' ' + words[0][4] + ' ' + words[0][5])
		time.append(words[0][6])

""" 
for cols in file:
	num_rows += 1
	words = [words.split() for words in cols.splitlines()]
	temporary_temperature = words[0][0]
	temperature.append(temporary_temperature[:-1])
	temporary_date = words[0][1] + ' ' + words[0][2] + ' ' + words[0][3]
	date.append(temporary_date[:-1])
	time.append(words[0][4])

#cond and pressure present in certain files but not others
temperature.pop(0)
#conductivity.pop(0)
#pressure.pop(0)
date.pop(0)
time.pop(0)
latitude = -73.82
longitude = -113.07

nc.createDimension('time', num_rows-1) #remove first line if there is a header
nc.createDimension('timeSeries',1)

#lat_var = nc.createVariable("latitude", np.double, ("timeSeries"))
#lat_var.units = "degrees_north"
#lat_var.axis = "Y"
#lon_var = nc.createVariable("longitude", np.double, ("timeSeries"))
temp_var = nc.createVariable("temperature", np.double, ("time"))
temp_var.units = 'K'
temp_var.notes ='TEMPERATURE - WATER [WATER TEMPERATURE]'
temp_var.standard_name = 'sea_water_temperature'

#present in certain files but not others.
"""
cond_var = nc.createVariable("conductivity", np.double, ("time"))
cond_var.standard_name = 'sea_water_electrical_conductivity'
cond_var.units = 'S m-1'
cond_var.notes = 'CONDUCTIVITY (mS/cm)'

pres_var = nc.createVariable('pressure', np.double, ("time"))
pres_var.standard_name = 'sea_water_pressure'
pres_var.units = 'dbar'
pres_var.notes = 'PRESSURE - BAROMETRIC'
"""

date_var = nc.createVariable("date", 'S1',("time"))
time_var = nc.createVariable("time", 'S1',("time"))

nc.title = netCDFfile[:-3]
nc.keywords = "ASPIRE,Amundsen Sea,Temperature Sensors,conductivity sensor"
nc.conventions = "CF-1.6"
nc.publisher_name = "US National Centers for Environmental Information"
nc.publisher_email = "ncei.info@noaa.gov"
nc.publisher_url = "https://www.ncei.noaa.gov"
nc.creator_name = 'Dr. Sharon Stammerjohn'
nc.creator_email = 'Sharon.Stammerjohn@colorado.edu'
nc.institution = 'Institute of Arctic and Alpine Research'
nc.abstract = 'WATER TEMPERATURE, CONDUCTIVITY, and others collected from MOORINGS in Amundsen Sea from 2010-12-16 to 2012-02-16'
nc.character_string = 'ISO 19115-2 Geographic Information - Metadata - Part 2: Extensions for Imagery and Gridded Data'
nc.summary = 'A sediment trap mooring (Ducklow et al., 2015; Randall-Goodwin et al., 2015) was deployed in the Amundsen Sea (73.82S, 113.07W) on December 16, 2010 from the RV/IB Nathaniel B. Palmer (NBP) during the ASPIRE research cruise (Yager et al., 2012; http://AntarcticASPIRE.org). The mooring was retrieved on February 16, 2012 by the RV/IB Aaron.  There was an SBE37 at 292m and an SBE39 at 753m.'
nc.notes = 'These sensors were deployed on a sediment trap mooring (Ducklow et al., 2015) offshore of the Dotson Ice Shelf in the Amundsen Sea to monitor the variability in temperature and conductivity in the winter mixed layer (at 292 m depth) as well as temperature near-bottom (at 753 m depth, 32 m from bottom)'
nc.credit = 'Suggested Author List: Stammerjohn, Sharon; Abrahamsen, Povl; Ducklow, Hugh; Yager, Patricia.'
nc.funding = 'Related Funding Agency: National Science Foundation (NSF)'
line1 = 'Randall-Goodwin, E., Meredith, M. P., Jenkins, A., Yager, P. L., Sherrell, R. M., Abrahamsen, E. P., . . . Stammerjohn, S. E. (2015). Freshwater distributions and water mass structure in the Amundsen Sea Polynya region, Antarctica. Elem Sci Anth, 3: 000065, 1-22. doi:10.12952/journal.elementa.000065'
line2 = 'Ducklow, H. W., Wilson, S. E., Post, A. F., Stammerjohn, S. E., Erickson, M., Lee, S. H., . . . Yager, P. L. (2015). Particle flux on the continental shelf in the Amundsen Sea Polynya and western Antarctic Peninsula. Elem Sci Anth, 3(000046). doi:10.12952/journal.elementa.000046'
line3 = 'Yager, P., Sherrell, R., Stammerjohn, S., Alderkamp, A.-C., Schofield, O., Abrahamsen, P., . . . Wilson, S. (2012). ASPIRE: The Amundsen Sea Polynya International Research Expedition. Oceanography, 25(3), 40-53. doi:10.5670/oceanog.2012.73'
nc.references = line1 + '\n' + line2 + '\n' + line3
nc.instrument = 'SeaBird SBE37,SeaBird SBE37,SeaBird SBE39'

nc.latitude = latitude
nc.longitude = longitude

temp_var[:] = temperature
#cond_var[:] = conductivity
#pres_var[:] = pressure
date_var[:] = date
time_var[:] = time



file.close()
