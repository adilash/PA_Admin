"""
Created on Tue Feb 27 21:27:55 2018

@author: abhiram haridas (abhiramharidas@gmail.com)
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import auth

import sys
import traceback
import json
from datetime import datetime
import dash_utils

cred = credentials.Certificate('./admin-PA.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-allocator.firebaseio.com/',
    'storageBucket': 'project-allocator.appspot.com'       
})

def network_error():

	print "\nUnable to read/write data  Check your internet connection and try again. If connection is alright modify source to view stacktrace.\n"
	
	print "\n The traceback for the error occurred\n"
	traceback.print_exc()
	print "\n\n"

	sys.exit()



def manage_users():

	print ("\nEnter 1 to manage students")
	print ("Enter 2 to manage faculty")
	print ("Enter 3 to exit")

	choice = raw_input()
	
	try:
		choice = int(choice)
	except ValueError:
		print "\nError! Invalid input.\n"
		return

	if choice == 1:

		print ("\nEnter 1 to add students")
		print ("Enter 2 to remove student")
		print ("Enter 3 to exit")

		try:
			choice = int(choice)
		except ValueError:
			print "\nError! Invalid input.\n"
			return

		if choice == 1:

			name = raw_input("\nEnter student name : ")
			login_mail = raw_input("Enter login mail : ")
			password = raw_input("Enter login password : ")
			roll_no = raw_input("Enter student roll number : ")
			p_email = raw_input("Enter personal email : ")
			phone = raw_input("Enter phone : ")

			db_ref_string = 'Student/%s'           #Student/uid

			try:

				user = auth.create_user(
    				email = login_mail,
    				email_verified = True,
    				phone_number = phone,
    				password = password,
    				disabled=False)

				data = {

					'nameof' : name,
					'personalemail' : p_email,
					'rollnumber' : roll_no,
					'phonenumber' : phone,
					'uid' : user.uid,
					'groupid' : ''
				}

				db_ref = db.reference(db_ref_string % user.uid)
				db_ref.set(data)

			except:
				network_error()






def manage_AOE():

	db_ref_string = 'AreaExpertise'
	try:
		db_ref = db.reference(db_ref_string)
		data = db_ref.get()
	except:
		network_error()


	while(1):

		print ("\nEnter 1 to view Areas of Expertise")
		print ("Enter 2 to add Area of Expertise")
		print ("Enter 3 to remove Area of Expertise")
		print ("Enter 4 to edit Area of Expertise")
		print ("Enter 5 to exit")
	
		choice = raw_input()
		
		try:
			choice = int(choice)
		except ValueError:
			print "\nError! Invalid input.\n"
			continue
	
		if choice == 1:
	
			print('')
			i = 0
			for key in data:
				print i," ",data[key]
				i = i+1
	
		elif choice == 2:
	
			new_area = raw_input("Enter new Area of Expertise : ")
			
	
			try:
				new_area_ref = db_ref.push()
				new_area_ref.set(new_area)
				data[new_area_ref.key] = new_area
				print('\nArea of Expertise added successfully')

			except:
				network_error()
	
		elif choice == 3:
	
			print('')
			i = 0
			keys = []
			for key in data:
				print i," ",data[key]
				keys.append(key)
				i = i+1
	
			print('')
			index = raw_input("Enter index of item to remove : ")
	
			try:
				index = int(index)
			except ValueError:
				print "\nError! Invalid input.\n"
				continue
	
			if index >= len(data):
				print "\nError! Invalid input.\n"
				continue
	
			data.pop(keys[index])
	
			try:
				db_ref.set(data)
				print('\nArea of Expertise removed successfully')
			except:
				network_error()
	
		elif choice == 4:
	
			print('')
			i = 0
			keys = []
			for key in data:
				print i," ",data[key]
				keys.append(key)
				i = i+1
	
			print('')
			index = raw_input("Enter index of item to edit : ")
			new_val = raw_input("Enter new value : ")
	
			try:
				index = int(index)
			except ValueError:
				print "\nError! Invalid input.\n"
				continue
	
			if index >= len(data):
				print "\nError! Invalid input.\n"
				continue
	
			data[keys[index]] = new_val
	
			try:
				db_ref.set(data)
				print('\nArea of Expertise edited successfully')
			except:
				network_error()
	
		elif(choice == 5):
			return;
		else:
			print "Invalid input"

	



#============================================   MAIN FUNCTION STARTS HERE ===================================================


choice = 0
print ("Welcome to Project Allocator Admin console!\n")

while(choice != 3):	
	
	print ("\nEnter 1 to manage users")
	print ("Enter 2 to manage Areas of Expertise")
	print ("Enter 3 to exit")

	choice = raw_input()
	
	try:
		choice = int(choice)
	except ValueError:
		print "\nError! Invalid input.\n"
		choice = 0
		continue

	if(choice == 1):
		manage_users()
	elif(choice == 2):
		manage_AOE()
	elif(choice == 3):
		continue;
	else:
		print "\nError! Invalid input.\n"

