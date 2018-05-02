# parse a potentially malformed CSV file


# idea 1 - use standard csv package (if it chokes, we will switch to operating on the data directly)
import csv
import datetime
DT = datetime.datetime
# seems to handle csv data OK

class User(object):
	def __init__(self, username,full_name):
		self.username=username
		self.full_name=full_name
		self.contacts=[]
	
	def update_contact(self,contact):
		if contact and contact not in self.contacts:
			self.contacts.append(contact)

	def __repr__(self):
		return "{0}: full_name:{1}".format(self.username, self.full_name)

	def key(self):
		return self.username

class Server(object):
	def __init__(self, server_ip, server_name):
		self.ipaddr=server_ip
		if server_name:
			self.name=server_name
		else:
			self.name='?'

	def __repr__(self):
		return "{0}: name:{1}".format(self.ipaddr,self.name)

	def key(self):
		return self.ipaddr


class Login(object):
	def __init__(self, login_date, user, server):
		self.login_date = login_date
		self.user = user
		self.server = server

	def __repr__(self):
		return "{0}->{1}@{2}".format(self.server.name or self.server.ip, self.user.username,self.login_date)

	def key(self):
		return "{0}~{1}~{2}".format(self.login_date, self.user.key, self.server.key)
    	
def parse_date(s):
	s=s.rstrip()
	dt=None
	try:
		dt=DT.strptime(s, "%Y-%m-%d")
	except:
		try:
			dt=DT.strptime(s, "%Y-%m-%d %H:%M:%S")
		except:
			dt=DT.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
	finally:
		return dt

class CSVParser(object):
    
	users={}
	# dict of: User objects indexed by username - this list is built 
	# from the data we are processing, but it would be an idea to read
	# a list of known users from the permanent data store (e.g. DB)
	
	servers_by_ip={}
	# dict of: Server objects indexed by ip address - this list is built 
	# from the data we are processing, but it would be an idea to read
	# a list of known servers from the permanent data store (e.g. DB)
	
	logins={}
	# dict of: Login objects indexed by date, username and server ip - indexed
	# so we can avoid duplicate entries
	
	collected_rows=[]

	date_subs = {
		',15-':',2015-',
		',16-':',2016-',
		',17-':',2017-'}
	
	date_seps = ['\\','|','/' ]


	def __init__(self):
		self._filename = None
		self._headers = None
		self._rows = []

	def set_filename(self, filename):
		self._filename = filename
	
	def parse_file(self):
		with open(self._filename,newline='') as f:
			reader = csv.reader(f, delimiter=',')
			self._headers = next(reader)
			assert(self._headers[0]=='server-name' and self._headers[1]=='server-ip' and 
			self._headers[2]=='username' and self._headers[3]=='full-name' and 
			self._headers[4]=='contact' and self._headers[5]=='login-time')
			for row in reader:
				self.fix_row(row)
				# let the fix_row method control which rows are ultimately recorded
		self.final_sweep()
		

	def final_sweep(self):
    	# now we have processed the login data, let's
		# see if there's anything we can do to improve the
		# data quality...
		# 1. update server_name from server_ip_table
		# 2. generating final reporting rows to update database
		pass

	def fix_row(self, row):
    	# ensure potentially missing fields are consistently recorded as None
		for row_idx in [0,4]:
			if row[row_idx]=='':
				row[row_idx]=None
		
		# read columns from row
		server_name, server_ip, username, full_name, contact, login_time = row
		
		# sanity check for user and server keys
		assert(username!='')
		assert(server_ip!='')
		
		# is it an already encountered server?
		if server_ip in self.servers_by_ip:
			server = self.servers_by_ip[server_ip]
		else:
			server = Server(server_ip, server_name)
			self.servers_by_ip[server_ip] = server
		# do we know this user?
		if username in self.users:
			user = self.users[username]
			
			# can we improve the contact data quality?
			if contact:
				user.update_contact(contact)
		else:
			user = User(username, full_name)
			self.users[username]=user
			
		# fix login time...
		for src in self.date_seps:
			login_time=login_time.replace(src,'-')

		for yr2d,yr4d in self.date_subs.items():
    		#if yr2d in login_time:
			login_time = login_time.replace(yr2d, yr4d)
    		
		login_dt = parse_date(login_time)
		
		# sanity check for login time which must be a valid date 
		assert(login_dt!=None)

		# can we improve the server.name data quality?
		if not server.name and server_name:
			server.name = server_name
		
		login = Login(login_dt, user, server)
		if not login.key in self.logins:
			# not a duplicate entry, so can record
			self.logins[login.key].append(login)
		else:
			# duplicate entry so skip
			pass
		

def main():
	csvparser = CSVParser()
	csvparser.set_filename('C:/dev/django_projects/sen-level-interview/data/logins.csv')
	csvparser.parse_file()

if __name__ == "__main__":
	main()