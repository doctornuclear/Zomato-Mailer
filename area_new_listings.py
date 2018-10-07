from imports import *
import smtplib

#/*****loads area's links*****\

area_links_file = open("areas.txt","r+")
area_links_un = area_links_file.readlines()
area_links_file.close()
area_links = []
for link in area_links_un:
	area_links.append(link.strip("\n"))


#/*****loads restaurant links already done*****\

restaurants_done_file = open("restaurants_done.txt","r+") 
restaurants_done_un = restaurants_done_file.readlines()
restaurants_done_file.close()
restaurants_done = []
for link in restaurants_done_un:
	restaurants_done.append(link.strip("\n"))


#DRIVER LOADED IN IMPORTS
#CHECKS EVERY AREA'S 3 PAGES FOR NEW RESTAURANT SORTED NEW
this_run_new_links = []

for link in area_links:	
	for i in range(1,4):
		driver.get(link+"?all=1&sort=recent&page=%d"%(i))
		rest_ele = driver.find_elements_by_css_selector(".result-title.hover_feedback.zred.bold.ln24.fontsize0 ") #conatins all restaurant links		
		
		for x in range(0,len(rest_ele)):
			time.sleep(0)
			rest_link = rest_ele[x].get_attribute("href")
			if rest_link in restaurants_done:
				print "restaurant link already in file", rest_link
				continue
			else:
				print rest_link
				this_run_new_links.append(rest_link)


#               DONE   ADD RESTAURANT RANDOMIZER
#				DONE   ADD LINK OPENER
#				DONE   ADD DETAILS MAILER

#loop
print "FOUND "+str(len(this_run_new_links))+" RESTAURANTS"
mail_sent = 0

for x in range(0,len(this_run_new_links)):


	random_number_for_links_selection = random.randint(0,len(this_run_new_links)-1)
	print random_number_for_links_selection
	print len(this_run_new_links)
	link_to_send = this_run_new_links[random_number_for_links_selection]

	this_run_new_links.remove(link_to_send)

	driver.get(link_to_send)
	if "404" in driver.title:
		print "broken link"
		continue

	rest_name = unicode(driver.find_elements_by_css_selector(".ui.large.header.left")[0].text).encode("utf-8")
	print "NAME: ",rest_name,"\n"

	rest_area = unicode(driver.find_elements_by_css_selector(".left.grey-text.fontsize3")[0].text).encode("utf-8")
	print "AREA: ",rest_area,"\n"
	
	try:
		rest_type_encoded = ((driver.find_elements_by_css_selector(".grey-text.fontsize3"))[1].text).encode("utf-8")
		rest_type_decoded = rest_type_encoded.decode("utf-8")
		rest_type = rest_type_decoded.encode("ascii","ignore")

	except:
		rest_type = "Maybe Delivery"	
			
	if "Caf" in rest_type:
		rest_type = rest_type+"e"
	print "TYPE:",rest_type,"\n"
					


	rest_phno = unicode(driver.find_elements_by_css_selector(".fontsize2.bold.zgreen")[0].text).encode("utf-8")
	print "PHONE NO: ",rest_phno,"\n"


	try:
		cost_for_two = int(driver.find_element_by_xpath("//div[1]/div/div[1]/div[3]/div[1]/div[1]/div[3]/div/div/span[2]").text.split(" for")[0].encode("ascii","ignore").replace(",",""))

			
	except:
		try:
			cost_for_two = int(driver.find_element_by_xpath("//div[1]/div/div[1]/div[4]/div[1]/div[1]/div[3]/div/div/span[2]").text.split(" for")[0].encode("ascii","ignore").replace(",",""))

		except:
			try:
				cost_for_two = int(driver.find_element_by_xpath("//div[1]/div/div[1]/div[3]/div[1]/div[1]/div[3]/div/div/span[2]").text.split(" for")[0].encode("ascii","ignore").replace(",",""))
			except:
				pass

	print "Cost for Two: ",cost_for_two,"\n"
	

	print "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x"	
	


	#try:
		#driver.find_element_by_css_selector(".opening-soon-label.res-notification-label.ui.big.yellow.label.ml0")

	# mail_body ="\n\n\n"+"Name: "+rest_name+"\n"+"Area: "+rest_area+"\n"+"Type: "+rest_type+"\n"+"Phone Number: "+rest_phno+"\n"+"Zomato Link: "+link_to_send+"\n"+"Cost for two: "+str(cost_for_two)
	

	# try:  
	#     server = smtplib.SMTP('smtp.gmail.com', 587)
	#     server.ehlo()
	# except:  
	#     print 'Something went wrong...'

	# fromaddr = 'automationbots2121@gmail.com'
	# toaddrs  = 'hardik.squarefork@gmail.com'
	# msg = mail_body
	# username = 'automationbots2121@gmail.com'
	# password = 'asdfmnbv'
	# server = smtplib.SMTP('smtp.gmail.com:587')
	# server.starttls()
	# server.login(username,password)
	# server.sendmail(fromaddr, toaddrs, msg)
	# server.quit()	

	print "MAIL SENT"
	mail_sent +=1
	print "MAILS SENT TILL NOW! " +str(mail_sent) 
	# except: 
	# 	pass

print this_run_new_links	