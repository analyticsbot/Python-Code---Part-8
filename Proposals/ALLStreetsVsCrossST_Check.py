import arcpy
from arcpy import env

##### Input #####
shp = "C:/Users/dotcid034/Desktop/Export_Output (1)/Export_Output.shp" 

col_fields = ["Cross_St","AllStreets","Doyourname"]
cur = arcpy.da.UpdateCursor(shp,col_fields)
for row in cur:
	val = None
	short_primary = ""
	short_cross = ""
	print row
	
	#if the cross-street string is empty, return 2
	if str(row[1]) == " ":
		print "None"
		val = 2
	else:
		#get the short version of the primary st
		primary_st = []
		primary_st = row[0].split()
		if len(primary_st) >= 2:
			prim_suffix = primary_st[len(primary_st)-1][0]
			primary_st[len(primary_st)-1] = prim_suffix
			short_primary = ' '.join(primary_st)
			print short_primary

		#shorten cross streets, each of which is separated by " & "
		cross_streets = []
		cross_streets = row[1].split(" & ")
		for i in cross_streets:
			print i
			streets2 = []
			streets2 = i.split()
			if len(streets2) >= 2:
				cross_suffix = streets2[len(streets2)-1][0]
				streets2[len(streets2)-1] = cross_suffix
				short_cross = ' '.join(streets2)
				print short_cross
				if short_cross == short_primary:
					val = 1
	
	#if the string is not empty, and if there is no match, return 0
	if val is None:
		val = 0

	#update the cursor
	row[2] = val
	cur.updateRow(row)


