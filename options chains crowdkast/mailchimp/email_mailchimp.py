import mailchimp
import jinja2
from datetime import date, timedelta

## define static variables

## api key for mailchimp for crowdkast
api_key = '05a4f6a09a5c9e736df5ec010c74a99f-us11'
debug_ = False

# Define Campaign Type 
campaignType = 'regular' # other possible values 'plaintext', 'variate', 'rss'
list_name = 'test' # Subscriber List. The exact name as in the mailchimp
subject = 'Testing'
from_email = 'ravi.shankar1788@gmail.com'
from_name = 'Crowdkast' #default_from_name=Crowdkast
email_title = ''

# template variables
template_loc = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\options chains crowdkast\\mailchimp\\template'
file_name = 'crowdkast.html'
minDate = ''
todayDate = str(date.today().strftime("%Y%d%m")) # value tested todayDate - '20150501'
yestDate = str((date.today() - timedelta(days=1)).strftime("%Y%d%m")) #value tested yestDate = '20150401'
recent_updates = "Crowdkast Volatility Forecasts are the expected +/- percentage movement in the underlying over the specified period. Crowdkast volatility forecasts are derived from thousands of crowd sourced data points from amateur and institutional analysts on popular investment discussion platforms."

def loadUVolDataForIndex(minDate, distribution):
    """Method to load volatility values for Indexes"""
    return [['DJIA', 'DJIA', 'DJIA', 'DJIA', 'DJIA', 'DJIA', 'DJIA', 'DJIA', 'DJIA', 'DJIA', 'DJIA', \
             'NASDAQ100', 'NASDAQ100', 'NASDAQ100', 'NASDAQ100', 'NASDAQ100', 'NASDAQ100', 'NASDAQ100', \
             'NASDAQ100', 'NASDAQ100', 'NASDAQ100', 'NASDAQ100', 'S&P500', 'S&P500', 'S&P500', 'S&P500', \
             'S&P500', 'S&P500', 'S&P500', 'S&P500', 'S&P500', 'S&P500', 'S&P500'], ['20150101', '20150201', \
            '20150301', '20150401', '20150501', '20150601', '20150701', '20150801', '20150901', '20151001', \
            '20151101', '20150101', '20150201', '20150301', '20150401', '20150501', '20150601', '20150701', \
            '20150801', '20150901', '20151001', '20151101', '20150101', '20150201', '20150301', '20150401', \
            '20150501', '20150601', '20150701', '20150801', '20150901', '20151001', '20151101'], \
            [12.1198, 12.5991, 4.33364, 5.52686, 6.52762, 8.16996, 12.8572, 14.5453, 16.0842, \
            17.537, 19.3157, 15.3895, 15.1621, 6.4492, 7.18625, 9.77404, 13.9578, 17.2242, 19.0652, 20.5106,\
             21.7565, 23.0677, 14.7887, 14.879, 5.69868, 5.9093, 9.04973, 10.6975, 15.4474, 18.6354, 20.5595,\
             21.9925, 23.2808]]

def getIndexValues(index, volatility_values):
    """Method to get values for a particular index"""
    index_ = []
    date = []
    values = []
    count = 0
    for value in volatility_values[0]:
            if value == index:
                    index_.append(index)
                    date.append(volatility_values[1][count])
                    values.append(volatility_values[2][count])
            count +=1
    return [index_, date, values]

## get values for respective indexes    
volatility_values = loadUVolDataForIndex(minDate,'crowdkast_distribution_daily')
djia_volatility_values = getIndexValues('DJIA', volatility_values)
nsdq_volatility_values = getIndexValues('NASDAQ100', volatility_values)
snp_volatility_values = getIndexValues('S&P500', volatility_values)

## calculate the values to be filled in the html template
## change is calculated as ((today value/ yesterday value)-1)*100
djia_percetage = djia_volatility_values[2][djia_volatility_values[1].index(todayDate)]
djia_change = ( ((djia_volatility_values[2][djia_volatility_values[1].index(todayDate)])/(djia_volatility_values[2][djia_volatility_values[1].index(yestDate)]))-1)*100
snp_percetage = snp_volatility_values[2][snp_volatility_values[1].index(todayDate)]
snp_change = (((snp_volatility_values[2][snp_volatility_values[1].index(todayDate)])/(snp_volatility_values[2][snp_volatility_values[1].index(yestDate)]))-1)*100
nsdq_percetage = nsdq_volatility_values[2][nsdq_volatility_values[1].index(todayDate)]
nsdq_change = ( ((nsdq_volatility_values[2][nsdq_volatility_values[1].index(todayDate)])/(nsdq_volatility_values[2][nsdq_volatility_values[1].index(yestDate)]))-1)*100

## setting the context for the jinja template variables
context = {'djia_percetage':"%.2f" %djia_percetage, 'djia_change': "%.2f" %djia_change, \
           'snp_percetage':"%.2f" %snp_percetage, 'snp_change':"%.2f" %snp_change, \
           'nsdq_percetage':"%.2f" %nsdq_percetage, 'nsdq_change':"%.2f" %nsdq_change, 'recent_updates' = recent_updates}

def render_jinja_html(template_loc,file_name,**context):
    """function to render the html template"""
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_loc+'/')
    ).get_template(file_name).render(context)

## Sending the email campaign                
# a. Connect to mailchimp via the api key. debug = True prints too much text
m = mailchimp.Mailchimp(apikey=api_key, debug=debug_)

# b. Specify Subscriber List 
list_id = m.lists.list(filters={'list_name':list_name})['data'][0]['id']

# c. Add the options 
options = {} 
options['list_id'] = list_id
options['subject'] = subject
options['from_email'] = from_email
options['from_name'] = from_name
options['title'] = email_title

# d. Create the content - use jinja html template.
content = {}
html = render_jinja_html(template_loc,file_name,**context)
content['html'] = html

# e. Create the campaign
campaignDetails = m.campaigns.create(type=campaignType, options=options,content=content)

# f. Send the campaign
sendStatus = m.campaigns.send(cid=campaignDetails['id'])
if sendStatus['complete'] == True: 
    print "Email Campaign Successfully Sent"
else:
    print "Error in sending the Email Campaign"


