11/19/2020

Update: 	Changing the name convention from "uQQQQQQ" to "uQQQQQQ_QQ" 
		where "_" is the decimal point.

Who: 		Solution suggested by Kenneth and Sebastian

Updated files: 	(1) .site_packages/riverpy/fGlobal.py 
		- function read_Q_str and write_Q_str are added

		(2) .site_packages/riverpy/cMakeTable.py
		- Line 82 

		(3) GetStarted/cWaterLevel.py 
		- Line 56 - 60

		(4) GetStarted/cConnectivityAnalysis.py
		- Line 168 - 170

		
11/21/2020

Update: 	Replace the function read_Q_str

Who:		Solution suggested by Sebastian

Updated file:	(1) .site-packages/riverpy/fGlobal.py
		- Line 362 - Make read_Q_str more stable
		- Line 597 - num:09.3f -> num:10.3f


12/2/2020

Update: 	SHArC analysis

who: 		Anzy

Updated files:	(1) cHSI.py
		- Line 118 - CalculateGeometryAttributes_management error
		  : Replaced "AREA" with "AREA_GEODESIC"
		- Line 146 - Defining Q
		  : q_str = fGl.read_Q_str(str(csi),prefix=fish_shortname)
		- Line 149 - Finding Q
		  : if str(fGl.write_Q_str(q)) == str(fGl.write_Q_str(q_str)):
		- Line 265, 266, 273 - Defining Q
		- Line 464-465, 487-488 - Defining Q
		- Line 474,496 - Using Q in the name of raster file

