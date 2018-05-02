from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def upload_csv(request):

	# save uploaded file in temp location

	# server_csv = CSVParser()
	# server_csv.set_filename(temp file name)
	
	# login_data = server_csv.parse_file()

	# update login_data to data store (DB)

	# return redirect to success page
	# or
	html="<html><body>{0} was succesfully processed.<h3>{1} rows uploaded</h3></body></html>".format("logins.csv",282)
	return HttpResponse(html)


def logins_by_server(request):
	# fairly lightweight data so get all server login data to minimise DB round-trips
	# can use javascript locally to filter if necessary plus will give user a more
	# responsive feel as we will not have network issues to contend with after first 
	# data fetch

	# Would probably use an ORM here, but rough SQL...
	# select s.server_name, s.server_ip, l.login_date, u.username, login l from logins l where l.date >= '2017-01-01' and l.date <='2018-04-30'
	# join server s on l.server_id = s.server_id
	# join user u on l.user_id = u.user_id
	
	# need to think about a fail-safe limit on the number of rows returned - say, 10k
	
	# build JSON data from DB data...
	# the client must render the data correctly and create filter controls etc

	jsondata="{\"servers\":{ \"stone\":{\"ipaddr\":\"201.23.18.80\"}},\"logins\":{...},\"users\":{}}"
	return HttpResponse(jsondata,mimetype='application/json')

