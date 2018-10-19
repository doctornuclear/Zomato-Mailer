from imports import *
import smtplib
import datetime
#/*****loads area's links & removing \n *****\

area_links_file = open("areas.txt","r+")
area_links_un = area_links_file.readlines()
area_links_file.close()
area_links = []
for link in area_links_un:
	area_links.append(link.strip("\n"))


#/*****loads restaurant links already done & removing \n *****\

restaurants_done_file = open("restaurants_done.txt","r+") 
restaurants_done_un = restaurants_done_file.readlines()
restaurants_done_file.close()
restaurants_done = []
for link in restaurants_done_un:
	restaurants_done.append(link.strip("\n"))

restaurants_done_file = open("restaurants_done.txt","a+") 
found_new_file = open("found_new_file.txt","a+")

#DRIVER LOADED IN IMPORTS
#CHECKS EVERY AREA'S 3 PAGES FOR NEW RESTAURANT SORTED NEW

areas_done_file = open("areas_done.txt","r+")
areas_done_un = areas_done_file.readlines()
areas_done = []
for x in areas_done_un:
	areas_done.append(x.split())
areas_done_file.close()	
areas_done_file = open("areas_done.txt","a+")


area_links = list(set(area_links) - set(areas_done))
new_restaurant_number = 0
def get_details_and_mail(this_run_new_links):
	
	mail_sent = 0
	broken_links = 0
	this_run_new_links = list(set(this_run_new_links))

	for x in range(0,len(this_run_new_links)):

		try:
			random_number_for_links_selection = random.randint(0,len(this_run_new_links)-1)
			print random_number_for_links_selection
			print len(this_run_new_links)
			link_to_send = this_run_new_links[random_number_for_links_selection]

			this_run_new_links.remove(link_to_send)

			time.sleep(2)
			driver.get(link_to_send)
			if "404" in driver.title:
				print "broken link"
				broken_links +=1
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
							


			rest_phno = unicode(driver.find_elements_by_css_selector(".fontsize2.bold.zgreen")[0].text).encode("ascii","ignore")
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
			


			# try:
			# 	driver.find_element_by_css_selector(".opening-soon-label.res-notification-label.ui.big.yellow.label.ml0")
			# 	pass
			mail_body = "\n\n\n"	+"Name: "+rest_name+"\n"	+"Area: "+rest_area+"\n"	+"Type: "+rest_type+"\n"	+"Phone Number: "+rest_phno+"\n"	+"Zomato Link: "+link_to_send+"\n"	+"Cost for two: "+ str(cost_for_two)
			

			try:  
			    server = smtplib.SMTP('smtp.gmail.com', 587)
			    server.ehlo()
			except:  
			    print 'Something went wrong...'
			    break
			#cc = ["hardik_sapra1@yahoo.in","hardik.squarefork@gmail.com,alsocialvocial@gmail.com"]    
			fromaddr = 'automationbots2121@gmail.com'
			#toaddrs  = ["info@thebluebeans.com","sv.sales2018@gmail.com"]
			toaddrs  = ["hardik_sapra1@yahoo.in","hardik.squarefork@gmail.com"]
			message_subject = "New Restaurant Found!"
			username = 'automationbots2121@gmail.com'
			password = 'asdfmnbv'
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			#toaddrs = [toaddrs] + cc   

			server.login(username,password)
			#cc = ["nikita@thebluebeans.com","alsocialvocial@gmail.com"]
			for email in toaddrs:
				msg = ("From: %s\r\n" % fromaddr
			        + "To: %s\r\n" % email
			        #+ "BCC: %s\r\n" % ",".join(cc)
			        + "Subject: %s\r\n" % message_subject
			        + "\r\n" 
			        + mail_body)
				
				server.sendmail(fromaddr, email, msg)
				time.sleep(2)
				print "mail sub part sent to %s" % email
			server.quit()	

			print "MAIL SENT"
			mail_sent +=1
			print "MAILS SENT TILL NOW! " +str(mail_sent) 
			print "BROKEN LINKS TILL NOW! " + str(broken_links)

			restaurants_done_file.write(link_to_send+"\n")
			restaurants_done_file.flush()
			# except: 
			# 	pass
		except Exception as e:
			print "Some Prblem Occurred!"	
			print(e)

			


def get_links_from_page(area_links,areas_done_file,new_restaurant_number):
	print area_links
	for link in area_links:	
		this_run_new_links=[]
		for i in range(1,4):
			time.sleep(2)
			driver.get(link+"?all=1&sort=recent&nearby=0&page=%d"%(i))
			rest_ele = driver.find_elements_by_css_selector(".result-title.hover_feedback.zred.bold.ln24.fontsize0 ") #conatins all restaurant links		
			
			for x in range(0,len(rest_ele)):
				time.sleep(1)
				rest_link = rest_ele[x].get_attribute("href")
				if rest_link in restaurants_done or rest_link in this_run_new_links:
					print "restaurant link already in file", rest_link
					continue
				else:
					print rest_link
					this_run_new_links.append(rest_link)
		
		print this_run_new_links			
		get_details_and_mail(this_run_new_links)
		areas_done_file.write(link+"\n")
		new_restaurant_number += len(this_run_new_links)


		return new_restaurant_number
#               DONE   ADD RESTAURANT RANDOMIZER
#				DONE   ADD LINK OPENER
#				DONE   ADD DETAILS MAILER

#loop

new_restaurant_number = get_links_from_page(area_links,areas_done_file,new_restaurant_number)

now = datetime.datetime.today().strftime('%Y-%m-%d')
print "FOUND "+str(len(new_restaurant_number))+" RESTAURANTS"
found_new_file.write(now + " : "+"Found "+ str(len(new_restaurant_number)))
found_new_file.flush()


areas_done_file.close()
restaurants_done_file.close()	
found_new_file.close()
