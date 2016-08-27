#6679.32500005seconds
from selenium import webdriver
from datetime import datetime, timedelta
import requests
import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
import settings
from models import Base, Inmates
import csv
import os
import tempfile
from sqlalchemy import or_

class Inmate(object):
	def __init__(self):
		self.inmateID = ""
		self.firstName = ""
		self.lastName = ""
		self.middleName = ""
		self.age = ""
		self.city = ""
		self.state = ""
		self.address = ""
		self.zip = ""
		self.phoneNumber = ""
		self.facility = ""
		self.bookingDateTime = ""
		self.charges = []

def main():
	startTime = time.time()
	engine = create_engine(URL(**settings.DATABASE), echo=False)
	Session = sessionmaker(bind=engine)
	session = Session()
	Base.metadata.create_all(engine)
	
	isTableEmpty = len(session.query(Inmates).all()) == 0
	inmateIDsInDatabase = []
	if not isTableEmpty:
		inmatesFromDatabase = session.query(Inmates).all()
		inmateIDsInDatabase = [inmate.inmateID for inmate in inmatesFromDatabase]
	
	reload(sys)
	sys.setdefaultencoding('utf-8')
	now = datetime.now()

	yest = now - timedelta(days=1)
	yest2 = now - timedelta(days=2)
	tomorrow = now + timedelta(days=1)
	dates = ["%d-%02d-%02d" % (date.year, date.month, date.day) for date in [now, yest, yest2]]
	datesBe = ["%02d/%02d/%d" % (date.month, date.day, date.year) for date in [now, yest, yest2]]
	log_path = os.path.join(tempfile.mkdtemp(), 'ghostdriver.log')
	driver = webdriver.PhantomJS(service_log_path=log_path)
	baseURL = "https://jailtracker.com/jtclientweb/jailtracker/index/"
	getInmatesUrl = "https://jailtracker.com/JTClientWeb/(%s)/JailTracker/GetInmates?limit=999999&sort=OriginalBookDateTime"
	getChargesUrl = "https://jailtracker.com/jtclientweb/(%s)/jailtracker/GetCharges"
	jsonURL = "https://jailtracker.com/JTClientWeb/(%s)/JailTracker/GetInmate?arrestNo=%s"
	chargeKeys = ["TICS ", "TRAFF", "TRAFFIC IN", "POSS", "CULTIVATION", "MANUFACTURING"]
	
	inmates = []
	inmatesIDs = []
	countyCity = {"Allen":"Scottsville", "Ballard":"Wickliffe", "Barren":"Glasgow", "Bell":"Pineville", "Big":"Paintsville", "Bourbon":"Paris", "Boyd":"Catlettsburg", "Boyle":"Danville", "Breckinridge":"Hardinsburg", "Bullitt":"Shepherdsville", "Calloway":"Murray", "Campbell":"Newport", "Carroll":"Carrollton", "Carter":"Grayson", "Casey":"Liberty", "Clark":"Winchester", "Clay":"Manchester", "Crittenden":"Marion", "Daviess":"Owensboro", "Franklin":"Frankfort", "Fulton":"Hickman", "Grant":"Williamstown", "Greenup":"Greenup", "Hardin":"Elizabethtown", "Harlan":"Evarts", "Hart":"Munfordville", "Henderson":"Henderson", "Hopkins":"Madisonville", "Jackson":"McKee", "Jessamine":"Nicholasville", "Kenton":"Covington", "Knox":"Barbourville", "Larue":"Hodgenville", "Laurel":"London", "Leslie":"Hyden", "Lewis":"Vanceburg", "Lincoln":"Stanford", "Madison":"Richmond", "Marion":"Lebanon", "Mason":"Maysville", "Monroe":"Tompkinsville", "Montgomery":"Mt. Sterling", "Ohio":"Hartford", "Oldham":"La Grange", "Pike":"Pikeville", "Powell":"Stanton", "Pulaski":"Somerset ", "Rockcastle":"Mt. Vernon", "Rowan":"Morehead", "Russell":"Russell Springs", "Shelby":"Shelbyville", "Simpson":"Franklin", "Taylor":"Campbellsville", "Three":"Beattyville", "Union":"Morganfield", "Whitley":"Williamsburg", "Woodford":"Versailles"}
	facilities = ["ALLEN_COUNTY_KY", "BALLARD_COUNTY_KY", "BARREN_COUNTY_KY", "http://www.bellcountydetention.com/InmateList/InmateList.aspx", "Big_Sandy_KY", "Bourbon_COUNTY_KY", "Boyd_County_KY", "Boyle_County_KY", "BRECKINRIDGE_COUNTY_KY", "BULLITT_COUNTY_KY", "Calloway_COUNTY_KY", "Campbell_County_KY", "CARROLL_COUNTY_KY", "CARTER_COUNTY_KY", "casey_county_KY", "Clark_County_KY", "Clay_COUNTY_KY", "CRITTENDEN_COUNTY_KY", "DAVIES_COUNTY_KY", "FRANKLIN_COUNTY_REGIONAL_KY", "FULTON_COUNTY_REGIONAL_KY", "Grant_County_KY", "Greenup_County_KY", "Hardin_COUNTY_KY", "HARLAN_COUNTY_KY", "HART_COUNTY_KY", "HENDERSON_COUNTY_KY", "HOPKINS_COUNTY_KY", "JACKSON_COUNTY_KY", "JESSAMINE_COUNTY_KY", "KENTON_COUNTY_KY", "KNOX_COUNTY_KY", "Larue_County_KY", "LAUREL_COUNTY_KY", "LESLIE_COUNTY_KY", "LEWIS_COUNTY_KY", "LINCOLN_COUNTY_KY", "Madison_COUNTY_KY", "MARION_COUNTY_KY", "MASON_COUNTY_KY", "MONROE_COUNTY_KY", "MONTGOMERY_COUNTY_REGIONAL_JAIL_KY", "OHIO_COUNTY_KY", "Oldham_County_KY", "PIKE_COUNTY_KY", "POWELL_COUNTY_KY", "PULASKI_COUNTY_KY", "ROCKCASTLE_COUNTY_KY", "ROWAN_COUNTY_KY", "russell_county_KY", "Shelby_County_KY", "SIMPSON_COUNTY_KY", "Taylor_County_KY", "Three_Forks_Regional_KY", "UNION_COUNTY_KY", "Whitley_County_KY", "Woodford_County_KY"]
	for facility in facilities:
		if "bellcounty" not in facility:
			request = requests.get(baseURL + facility)
			if request.status_code != 200:
				continue
			dynParam = request.url.partition('(')[-1].rpartition(')')[0]
			request = requests.get(getInmatesUrl % dynParam)
			jsonInmates = []
			try:
				jsonInmates = request.json()['data']
			except:
				request = requests.get(getInmatesUrl % dynParam)
				time.sleep(2)
				jsonInmates = request.json()['data']
			if not isTableEmpty:
				jsonInmates = [jsonInmate for jsonInmate in jsonInmates if jsonInmate['OriginalBookDateTime'] in dates]
			if len(jsonInmates) == 0:
				continue
			facilityName = jsonInmates[0]['Facility'].title()
			facilityCounty = facilityName.split(' ')[0]
			for jsonInmate in jsonInmates:
				#if not isTableEmpty:
				#	if jsonInmate['OriginalBookDateTime'] != date:
				#		continue
				jsonInmateArrestNo = jsonInmate['ArrestNo']
				if not isTableEmpty:
					if jsonInmateArrestNo in inmateIDsInDatabase:
						continue
				request = requests.post((getChargesUrl % dynParam), data={"arrestNo":jsonInmateArrestNo})
				inmateCharges = []
				try:
					inmateCharges = request.json()['data']
				except:
					request = requests.post((getChargesUrl % dynParam), data={"arrestNo":jsonInmateArrestNo})
					time.sleep(2)
					inmateCharges = request.json()['data']
				#inmateChargeCodes = [str(charge['ArrestCode']) for charge in inmateCharges]
				#isDrugRelatedArrest = any(c.startswith(('4', '021', '023')) for c in inmateChargeCodes)
				isDrugRelatedArrest = False
				for inmateCharge in inmateCharges:
					isDrugRelatedArrest = inmateCharge['ArrestCode'].startswith(('021', '023'))
					if not isDrugRelatedArrest:
						if inmateCharge['ArrestCode'].startswith('4'):
							isDrugRelatedArrest = any(cK in inmateCharge['ChargeDescription'] for cK in chargeKeys)
					if isDrugRelatedArrest:
						break
				if isDrugRelatedArrest:
					inmatesIDs.append(jsonInmateArrestNo)
					#if not isTableEmpty:
					#	if jsonInmate['OriginalBookDateTime'] != date:
					#		continue
					request = requests.get(jsonURL % (dynParam, jsonInmateArrestNo))
					inmateJSON = []
					try:
						inmateJSON = request.json()['data']
					except:
						request = requests.get(jsonURL % (dynParam, jsonInmateArrestNo))
						time.sleep(2)
						inmateJSON = request.json()['data']
					inmate = Inmate()
					inmate.inmateID = jsonInmateArrestNo
					for field in inmateJSON:
						if "First" in field['Field']:
							inmate.firstName = field['Value']
						elif "Last" in field['Field']:
							inmate.lastName = field['Value']
						elif "Middle" in field['Field']:
							inmate.middleName = field['Value']
						elif "Current" in field['Field']:
							inmate.age = field['Value']
						elif "City" in field['Field']:
							inmate.city = field['Value']
						elif "State" in field['Field']:
							inmate.state = field['Value']
						elif "Address" in field['Field']:
							inmate.address = field['Value']
						elif "Zip" in field['Field']:
							inmate.zip = field['Value']
						elif "Booking" in field['Field']:
							inmate.bookingDateTime = field['Value']
					for inmateCharge in inmateCharges:
						charge = [inmateCharge['ArrestCode'], inmateCharge['ChargeDescription'], inmateCharge['ArrestDate']]
						inmate.charges.append(" ".join(charge))
					if len(inmate.city) == 0 and len(inmate.state) == 0:
						if ',' in inmate.address:
							cityState = inmate.address.split(',')
							inmate.city = cityState[0]
							inmate.state = cityState[1].lstrip()
							inmate.address = ""
						else:
							inmate.city = countyCity[facilityCounty]
							inmate.state = "KY"
					elif len(inmate.city) > 0 and len(inmate.state) == 0:
						inmate.state = "KY"
					elif ',' in inmate.address:
						cityState = inmate.address.split(',')
						inmate.city = cityState[0]
						inmate.state = cityState[1].lstrip()
					inmate.facility = facilityName
					print inmate.inmateID, inmate.firstName, inmate.lastName, facility[:15]
					inmates.append(inmate)
		else:
			request = requests.get(facility)
			time.sleep(40)
			if request.status_code != 200:
				continue
			driver.get(facility)
			time.sleep(2)
			bellBaseURL = "http://www.bellcountydetention.com/InmateList/InmateView.aspx?ID="
			pageRow = driver.find_element_by_xpath("//table[@id='dgInmates']/tbody/tr[last()]")
			pageLinks = pageRow.find_elements_by_xpath(".//a[count(preceding-sibling::span)=1]")
			pages = len(pageLinks) + 1
			#pageLink = "//a[@href='javascript:__doPostBack('dgInmates$ctl24$ctl0%s','')']"
			for i in xrange(pages):
				inmateRows = driver.find_elements_by_xpath("//table[@id='dgInmates']/tbody/*")[1:-1]
				inmateIDs = []
				for inmateRow in inmateRows:
					id = inmateRow.find_element_by_xpath(".//a").get_attribute('href').split('=')[1]
					inmateIDs.append(id)
				for inmateID in inmateIDs:
					if not isTableEmpty:
						if inmateID in inmateIDsInDatabase:
							continue
					driver.get(bellBaseURL + inmateID)
					time.sleep(1)
					chargeRows = driver.find_elements_by_xpath("//table[@id='DataList1']/tbody/*")
					charges = []
					codeElementID = "//span[@id='DataList1_ctl%02d_Code']"
					descriptionElementID = "//span[@id='DataList1_ctl%02d_Description']"
					courtDateElementID = "//span[@id='DataList1_ctl%02d_CourtDate']"
					for j in xrange((len(chargeRows)-2)/2):
						code = driver.find_element_by_xpath(codeElementID % (j + 1)).text
						description = driver.find_element_by_xpath(descriptionElementID % (j + 1)).text
						courtDate = driver.find_element_by_xpath(courtDateElementID % (j + 1)).text
						charges.append([code, description, courtDate])
					isDrugRelatedArrest = False
					for charge in charges:
						isDrugRelatedArrest = charge[0].startswith(('021', '023'))
						if not isDrugRelatedArrest:
							if charge[0].startswith('4'):
								isDrugRelatedArrest = any(cK in charge[1] for cK in chargeKeys)
						if isDrugRelatedArrest:
							break
					if isDrugRelatedArrest:
						inmatesIDs.append(jsonInmateArrestNo)
						bookingDate = driver.find_element_by_xpath("//span[@id='lblBookDate']").text
						if not isTableEmpty:
							if bookingDate not in datesBe:
								continue
						inmate = Inmate()
						fullName = driver.find_element_by_xpath("//span[@id='lblInmateNameMain']").text
						fullName = fullName.split(',')[0].strip()
						fullNameParts = fullName.split(' ')
						inmate.inmateID = inmateID
						inmate.firstName = fullNameParts[0]
						inmate.lastName = fullNameParts[-1]
						inmate.middleName = ' '.join(fullNameParts[1:-1])
						inmate.age = driver.find_element_by_xpath("//span[@id='lblAge']").text
						cityState = driver.find_element_by_xpath("//span[@id='lblAddress']").text
						inmate.city = cityState.split(',')[0]
						inmate.state = cityState.split(',')[1].lstrip()
						inmate.facility = "Bell County Detention Center"
						bookingDate = driver.find_element_by_xpath("//span[@id='lblBookDate']").text
						bookingTime = driver.find_element_by_xpath("//span[@id='lblBookTime']").text
						inmate.bookingDateTime = bookingDate + " " + bookingTime
						for charge in charges:
							inmate.charges.append(" ".join(charge))
						print inmate.inmateID, inmate.firstName, inmate.lastName, facility[:15]
						inmates.append(inmate)
				driver.find_element_by_xpath("//a[@id='HyperLink1']").click()
				if i != (pages - 1):
					linkRow = driver.find_element_by_xpath("//table[@id='dgInmates']/tbody/tr[last()]")
					linkRow.find_element_by_xpath(".//a[count(preceding-sibling::span)=1]").click()
			driver.quit()
	for inmate in inmates:
		if session.query(Inmates).filter(Inmates.inmateID == inmate.inmateID).count() == 0:
			session.add(Inmates(inmate.inmateID, inmate.firstName.title().encode('utf-8'), inmate.lastName.title().encode('utf-8'), inmate.middleName.title().encode('utf-8'), inmate.age, inmate.city.title(), inmate.state, inmate.address.title(), inmate.zip, inmate.phoneNumber, inmate.facility, inmate.bookingDateTime, '|'.join(inmate.charges)))
	session.commit()
	#if not isTableEmpty:
	#	releasedInmates = list(set(inmateIDsInDatabase) - set(inmatesIDs))
	#	for releasedInmate in releasedInmates:
	#		session.delete(session.query(Inmates).filter(Inmates.inmateID == releasedInmate).one())
	#session.commit()
	with open("/home/ec2-user/jailtracker/jailTrackerInmates.csv", "w") as f:
		writer = csv.writer(f)
	        now = datetime.now()
        	thisWeek0 = now
       		thisWeek0 = thisWeek0.strftime("%-m/%-d/%Y")
        	thisWeek1 = now - timedelta(days=1)
        	thisWeek1 = thisWeek1.strftime("%-m/%-d/%Y")
        	thisWeek2 = now - timedelta(days=2)
        	thisWeek2 = thisWeek2.strftime("%-m/%-d/%Y")
        	thisWeek3 = now - timedelta(days=3)
        	thisWeek3 = thisWeek3.strftime("%-m/%-d/%Y")
        	thisWeek4 = now - timedelta(days=4)
        	thisWeek4 = thisWeek4.strftime("%-m/%-d/%Y")
        	thisWeek5 = now - timedelta(days=5)
        	thisWeek5 = thisWeek5.strftime("%-m/%-d/%Y")
        	thisWeek6 = now - timedelta(days=6)
        	thisWeek6 = thisWeek6.strftime("%-m/%-d/%Y")
		#inmatesFromDatabase = session.query(Inmates).all()
		inmatesFromDatabase = session.query(Inmates).filter(or_(Inmates.bookingDateTime.like(thisWeek0 + "%"), Inmates.bookingDateTime.like(thisWeek1 + "%"), Inmates.bookingDateTime.like(thisWeek2 + "%"), Inmates.bookingDateTime.like(thisWeek3 + "%"), Inmates.bookingDateTime.like(thisWeek4 + "%"), Inmates.bookingDateTime.like(thisWeek5 + "%"), Inmates.bookingDateTime.like(thisWeek6 + "%"))).all()
		for inmate in inmatesFromDatabase:
			writer.writerow((inmate.inmateID, inmate.firstName.title().encode('utf-8'), inmate.lastName.title().encode('utf-8'), inmate.middleName.title().encode('utf-8'), inmate.age, inmate.city.title(), inmate.state, inmate.address.title(), inmate.zip, inmate.phoneNumber, inmate.facility, inmate.bookingDateTime, inmate.charges))
	print str(str(time.time() - startTime) + "seconds")
if __name__ == '__main__':
	main()
