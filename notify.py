import smtplib
from email.mime.text import MIMEText

def notifyUserByEmail(email_id, link):
    #content = ("Price Dropped! check out the link : "+link)

    msg = MIMEText(u'<a href='+link+'>Price Dropped!</a>','html')
    msg['Subject'] = 'subject'

    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('sanyamcoder','Sanyam@99')
    mail.sendmail('sanyamcoder@gmail.com',email_id,msg.as_string()) 
    mail.close()
    print("Sent")



# you have to get price by website in realtime, we can pass the product link in parameter of getPrice()
def getPrice():
    i = input('Enter the current price of product checked by site : ')
    i = int(i)
    return i

users_list=[] 
#user_dict would be element of users_list eg user1

user1 = {'name':'Ajay','check_products':[],'email_id':'im7akash@gmail.com'}
#pdt_desc would be element of check_products

pdt_desc = {'product_name':'Puslar 220','link':'https://www.amazon.in/LG-inch-55cm-LCD-Monitor/dp/B01IBM5V66/ref=sr_1_2?dchild=1&keywords=monitor&qid=1621311255&s=computers&sr=1-2','threshold_price':20000,'site':'Amazon','stored_prices':[]}
#searched_price would be element in pdt_desc

searched_price = {'price':22000,'date':'22/5/2021'}
pdt_desc['stored_prices'].append(searched_price)
searched_price = {'price':23400,'date':'23/5/2021'}
pdt_desc['stored_prices'].append(searched_price)


user1['check_products'].append(pdt_desc)
# adding product_details in user's account

users_list.append(user1)
# adding user in the list of users which are to be notified on price drop

# user2 = user1.copy()
# user2['name'] = 'Saklecha'

# user1['check_products'][0]['threshold_price'] = 50000
# # Threshold getting changed in both users !!


# Making extra users
user2 = {'name':'Sanyam','check_products':[],'email_id':'rox.akash707510@gmail.com'}
#pdt_desc would be element of check_products

pdt_desc = {'product_name':'Suzuki 23F','link':'https://www.amazon.in/Logitech-M90-Mouse-Dark-Grey/dp/B003D8ZT0C/ref=cm_cr_arp_d_product_top?ie=UTF8','threshold_price':50000,'site':'Flipkart','stored_prices':[]}
#searched_price would be element in pdt_desc

searched_price = {'price':80000,'date':'22/5/2021'}
pdt_desc['stored_prices'].append(searched_price)
searched_price = {'price':60000,'date':'23/5/2021'}
pdt_desc['stored_prices'].append(searched_price)


user2['check_products'].append(pdt_desc)
users_list.append(user2)


#print(users_list)


for u_dict in users_list:
    print("User : "+u_dict['name'])
    for pdt_dict in u_dict['check_products']:
        print("Product : "+pdt_dict['product_name'])
        print("Threshold price : "+str(pdt_dict['threshold_price']))
        print("stored_prices for product are : ",pdt_dict['stored_prices'])
        curr_price = getPrice()
        if(curr_price<pdt_dict['threshold_price']):
            print("User notified for Price drop")
            notifyUserByEmail(u_dict['email_id'],pdt_dict['link'])

        new_searched_price = {'price':curr_price,'date':'26/5/2021'}
        pdt_dict["stored_prices"].append(new_searched_price)
        #print(pdt_dict)

print("\n\nUpdated the stored_prices!!")
print(users_list)





