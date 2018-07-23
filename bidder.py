from selenium import webdriver
import time
import ebaySeleniumOperatons as eso

#Globals
amountForSearch = 0.26 #in usd #double
actualBidAmmount = 0.32 #in usd #double
with open('login.txt') as f:
    #login.txt is included in .gitignore
    #in login.txt provide #1st line - username,2nd line - password
    lines = f.readlines()
emailUsed = lines[0]
passswordUsed = lines[1]
#Globals

#chrome webdriver
driver = webdriver.Chrome()
#set implicit wait for 1 second.
driver.implicitly_wait(0)
#use explicit waits for each element that must be clicked on.


#URL LIST
#https://www.ebay.com/sch/i.html?_odkw=fidget+-cap+-caps+-bearing+-bearings+-weight&_sop=1&_udhi=0.2&_mPrRngCbx=1&LH_FS=1&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xfidget+-cap+-caps+-bearing+-bearings+-weight+-yo.TRS0&_nkw=fidget+-cap+-caps+-bearing+-bearings+-weight+-yo&_sacat=0"
urls = [
"https://www.ebay.com/sch/i.html?_odkw=leather+case+samsung+%28s7%2Cs8%2Cj3%2Cj5%2Cj7%29&_sop=1&_udhi=0.6&_mPrRngCbx=1&LH_FS=1&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xleather+case+samsung+%28s7%2Cs8%2Cj3%2Cj5%2Cj7%2Ca3%2Ca5%2Ca7%29.TRS0&_nkw=leather+case+samsung+%28s7%2Cs8%2Cj3%2Cj5%2Cj7%2Ca3%2Ca5%2Ca7%29&_sacat=0", #leather case samsung (s7,s8,j3,j5,j7,a3,a5,a7) pod 0.6
"https://www.ebay.com/sch/i.html?_odkw=leather+case+iphone++-%22iphone+5%22+-%22iphone+4%22&_sop=1&_udhi=0.6&_mPrRngCbx=1&LH_FS=1&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xleather+case+iphone+%286%2C7%29++-%22iphone+5%22+-%22iphone+4%22.TRS0&_nkw=leather+case+iphone+%286%2C7%29++-%22iphone+5%22+-%22iphone+4%22&_sacat=0", #iphone 6,7 leather case pod 0.6
"https://www.ebay.com/sch/i.html?_odkw=%28leather%2CPU%2Cflip%29+case+huawei&_sop=1&_udhi=0.6&_mPrRngCbx=1&LH_FS=1&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.X%28leather%2CPU%2Cflip%29+case+huawei+%28p9%2Cp10%29.TRS0&_nkw=%28leather%2CPU%2Cflip%29+case+huawei+%28p9%2Cp10%29&_sacat=0", #huawei p9,p10 po 0.6
"https://www.ebay.com/sch/i.html?_odkw=%28leather%2CPU%2Cflip%29+case+%282017%2C2016%2Ciphone%29&_sop=1&_udhi=0.6&_mPrRngCbx=1&LH_FS=1&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.X%28leather%2CPU%2Cflip%29+case+%282017%2C2016%29.TRS0&_nkw=%28leather%2CPU%2Cflip%29+case+%282017%2C2016%29&_sacat=0", #(leather,PU,flip) case (2017,2016) 
]

if __name__ == "__main__":
    eso.signin(driver,emailUsed,passswordUsed)
    eso.bidOnItems(driver,eso.findSearchItems(urls,amountForSearch),actualBidAmmount)