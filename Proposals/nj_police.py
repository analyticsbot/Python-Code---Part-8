import mechanize
from bs4 import BeautifulSoup
import re

br = mechanize.Browser()
url  = 'http://www.icrimewatch.net/offenderdetails.php?OfndrID=2310977&AgencyID=55260'
br.open(url)
html = br.response().read()

soup = BeautifulSoup(html)

trs = soup.findAll('tr')

offenseLabel = soup.find('span', attrs = {'class':'offenseLabel'})
offenseLabel1 = offenseLabel.findNextSibling()
offenseLabel1 = offenseLabel.findNext('td')
offenseLabel1.getText()
u'\n                                14-3A - AGGRAVATED CRIMINAL SEXUAL CONTACT                               '
text = soup.find('td', attrs = {'valign':'top'}).getText()
aa = re.sub( '\n+', '\n', text ).strip()
aa.split('\n')

[u'Details', u'Name:', u'DENNIS J JABLONSKI ', u'Registration #:', u'                      2310977', u'Level:', u'Tier 2 - Moderate Risk                    ', u'Physical Description', u'\u2022 Age:', u'53 \xa0(DOB: 01/30/1963)', u'\u2022 Height:', u"5'10''", u'\u2022 Sex:', u'M', u'\u2022 Weight:', u'210lbs', u'\u2022 Race:', u'White', u'\u2022 Eyes:', u'Brown', u'\u2022 Hair:', u'Gray', u'\u2022 Scars/Tattoos:', u'\xa0', u'\xa0', u'\xa0', u'\xa0', u'Address', u'3  BARCELONA COURT MANCHESTER TWP, NJ 08759\xa0', u'\t\t      ', u'                            View Map', u'Offenses', u'\u2022 Description:', u'                                14-3A - AGGRAVATED CRIMINAL SEXUAL CONTACT                               ', u'\u2022 Date Convicted:', u'                                07/13/2006                      ', u'\u2022 Conviction State:', u'                              Illinois                              ', u'\u2022', u'                                                                          Release Date:', u'                                                                      ', u' ', u'\u2022 Details:', u'\u2022 County of Conviction:', u' ', u'\xa0', u'\xa0', u'Comments', u'                                        \xa0', u'\xa0', u'\xa0', u'\xa0', u'Share this information with a friend!', u' ', u'\xa0', u'DENNIS J JABLONSKI', u'Submit a tip or correction for this offender', u'Register to track this offender', u'Vehicles', u'Name:', u'DENNIS J JABLONSKI ', u'Registration #:', u'                      2310977', u'Level:', u'Tier 2 - Moderate Risk                    ', u' ', u'Vehicles', u'Plate', u'Make', u'Model', u'Year', u'Color', u'NJ ZB405D', u'Ford', u'Escape', u'2004', u'Gray ', u'\xa0', u'\xa0', u'\xa0', u'Share this information with a friend!', u' ', u'\xa0', u'DENNIS J JABLONSKI', u'Submit a tip or correction for this offender', u'Register to track this offender']
