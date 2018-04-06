## a quick description
##
## needs to be able to grab data maybe once per second, maybe faster/slower
## depending on processor tax
##
## probably a while loop that depends on an input break of some sort
## have had a hard time getting that working, but may have to succeed here
##
## create the variables to get the book numbers, 10 will be needed total
##
## cant seem to get current price from this page, may have to find a new
## solution or just guess in the margin of the bid / ask
##
## will need to store to a file, probably by date and time or just numberd with
## date and time included.
##
## file should probably be CSV of sorts, with arrays being stored.
##
## should be pretty well seperated into different methods for everything that
## that needs to be done, this way it should help with the threading/mutiprocess
##
## making use of time will be necessary
##
## get each block working seperatly, this will help with interfacing later, and
## spreading the work load.
##
####
### this will end up being a module to feed the extra level 2 data i want,
### to a main program that will give me the summary and which direction the
### stock should go, and if it is a good buy or sell.
####
## ...

#
#

## the data must be checked every time it is gotten, so that only new data is
## obtained. (this may not be true, will need to check the timing of how long
## it takes)




from lxml import html
import requests
import time

ticker = 'SNMX'

def clean_Output(tmp):

    output = []
    cnt = -1
    check = 0
    try:
        for i in tmp:
            #print('FOO', i)
            for j in i:
                #print ('FOO2', j)
                if j != "'" and j != "," and j != "[" and j != "]" and j != " ":
                    if check < 0:
                        cnt += 1
                    #print(j)
                    output[cnt] += j
                    check = 0
                else:
                    if check == 0:
                        output.append('')
                    check = -1
                    
    except Exception as e:
        print("Error in clean_Output:", e)
            
    return output

def lxml_Scrape(ticker):

    try:
        
        page = requests.get('https://ca.finance.yahoo.com/q/ecn?s='+ticker)
        tree = html.fromstring(page.content)
        #output = tmp = []

        tmp = []

        tmp.append(str(tree.xpath('//table//th/text()')))               #table names
        tmp.append(str(tree.xpath('//table//tbody//td/text()')))         #body data

        #print(tmp)
        #print (output[0][1], "\n \n \n", output[1],  "\n \n \n")   #used for debugging
        output = clean_Output(tmp)
        
        return output
    except Exception as e:
        print("Error in lxml_Scrape:", e)
    
##    here lies legacy code i may need in the future to remember how to use lxml
##    buyer = tree.xpath('//div[@title="buyer-name"]/text()')


def timer(method):

    t0 = time.clock()

    method()

    t1 = time.clock()

    total = t1 - t0

    print ("\n\n\n", total)

def is_Int(test):
    try:
        a = float(test)
        b = int(a)
        if a == b:
            return "TRUE"
        else:
            return "FALSE"
    except:
        return "STRING"


def show_Output():

    try:
        output = lxml_Scrape(ticker)
    except Exception as e:
        print("Error setting output from lxml_Scrape call:", e)

    table_Headers, price_Headers, bid_Data, ask_Data, tmp = [],[],[],[],[]
    first_Pass = True
    arm_Switch = False
    last_Int = False
    last_Int2 = False
    
    try:
        for j in output:
            #print('foo2',j)
            if is_Int(j) == "STRING" and j == "Size" and first_Pass == True and arm_Switch == False:

                arm_Switch = True                       #THE SWITCH IS ARMED!!!
                last_Int = False
                #print("THE SWITCH IS ARMED")

            elif is_Int(j) == "STRING" and j == "Price" and first_Pass == True and arm_Switch == True:

                first_Pass = False
                last_Int = False
                #print("THE SWITCH IS FLIPPED")
                
            elif is_Int(j) == "FALSE" and first_Pass == True and arm_Switch == True:
                try:
                    try:
                        bid_Data[0]
                    except:
                        bid_Data.append([])
                        #print(bid_Data)
                    bid_Data[0].append(j)
                    last_Int = False
                    #print("bid data - 1", first_Pass, arm_Switch)
                except Exception as e:
                    print("Error in output, elif 2:", e)
                
            elif is_Int(j) == "TRUE" and first_Pass == True and arm_Switch == True:
                try:
                    try:
                        bid_Data[1]
                    except:
                        bid_Data.append([])
                    if last_Int == True:
                        bid_Data[1][len(bid_Data[1]) -1] += j
                        last_Int = False
                    else:
                        bid_Data[1].append(j)
                    last_Int = True
                    #print("bid data - 2")
                except Exception as e:
                    print("Error in output, elif 3:", e)
                
            elif is_Int(j) == "FALSE" and first_Pass == False:
                try:
                    try:
                        ask_Data[0]
                    except:
                        ask_Data.append([])
                    ask_Data[0].append(j)
                    last_Int = False
                    #print("ask data - 1")
                except Exception as e:
                    print("Error in output, elif 4:", e)
                
            elif is_Int(j) == "TRUE" and first_Pass == False:
                try:
                    try:
                        ask_Data[1]
                    except:
                        ask_Data.append([])
                    if last_Int == True:
                        ask_Data[1][len(ask_Data[1]) -1] += j
                        last_Int = False
                    else:
                        ask_Data[1].append(j)
                    last_Int = True
                    #print("ask data - 2")
                except Exception as e:
                    print("Error in output, elif 5:", e)

##            else:
##                ask_data = [["EMPTY"],["EMPTY"]]
##                bid_data = [["EMPTY"],["EMPTY"]]

    except Exception as e:
        print("Error in show_Output, building data arrays:", e)            

            
##    for k in output[1]:
##        tmp.append(k)
##        print(k)
##
##    print(table_Headers,tmp,output[1])
    #print(table_Headers,output)
    first_line = True
    try:
        len(bid_Data[0])
        #print("passed bid test")
    except:
        bid_data = [["EMPTY"],["EMPTY"]]

    try:
        len(ask_Data[0])
        #print("passed ask test")
    except:   
        #print("setting ask")        
        ask_Data = [["EMPTY"],["EMPTY"]]

    ask_Weight = 0
    bid_Weight = 0
    total_Weight = 0
         
    try:
        if len(bid_Data[0]) > len(ask_Data[0]):
            try:
                for i in range(len(bid_Data[0])):
                    if first_line == True:
                        print('{:{align}{width}}'.format('STOCK: '+ ticker, align='<', width='48') + '\n' +
                              '{:{align}{width}}'.format('BID', align='^', width='24') +
                              '{:{align}{width}}'.format('ASK', align='^', width='24'))
                        first_line = False
                    try:
                        print('{:{align}{width}}'.format(bid_Data[0][i], align='>', width='12') +
                              '{:{align}{width}}'.format(" "+bid_Data[1][i], align='<', width='12') +
                              '{:{align}{width}}'.format(ask_Data[0][i], align='>', width='12') +
                              '{:{align}{width}}'.format(" "+ask_Data[1][i], align='<', width='12'))
                        ask_Weight += int(ask_Data[1][i])
                        bid_Weight += int(bid_Data[1][i])

                    except:
                        print('{:{align}{width}}'.format(bid_Data[0][i], align='>', width='12') +
                              '{:{align}{width}}'.format(" "+bid_Data[1][i], align='<', width='12') +
                              '{:{align}{width}}'.format(" ", align='>', width='12') +
                              '{:{align}{width}}'.format(" ", align='<', width='12'))
                        #ask_Weight += int(ask_Data[1][i])
                        bid_Weight += int(bid_Data[1][i])

                total_Weight = ask_Weight + bid_Weight
                
                print('{:{align}{width}}'.format(str(((bid_Weight / total_Weight)*100))+" %", align='^', width='24') +
                      '{:{align}{width}}'.format(str(((ask_Weight / total_Weight)*100))+" %", align='^', width='24'))
                        
            except Exception as e:
                    print("Error in output; output if-for loop:", e)

        else:
            try:
                for i in range(len(ask_Data[0])):
                    if first_line == True:
                        print('{:{align}{width}}'.format('STOCK: '+ ticker + '\n', align='<', width='48') + '\n' +
                              '{:{align}{width}}'.format('BID', align='^', width='24') +
                              '{:{align}{width}}'.format('ASK', align='^', width='24'))
                        first_line = False

                    try:
                        print('{:{align}{width}}'.format(bid_Data[0][i], align='>', width='12') +
                              '{:{align}{width}}'.format(" "+bid_Data[1][i], align='<', width='12') +
                              '{:{align}{width}}'.format(ask_Data[0][i], align='>', width='12') +
                              '{:{align}{width}}'.format(" "+ask_Data[1][i], align='<', width='12'))
                        ask_Weight += int(ask_Data[1][i])
                        bid_Weight += int(bid_Data[1][i])

                    except:
                        print('{:{align}{width}}'.format(" ", align='>', width='12') +
                              '{:{align}{width}}'.format(" ", align='<', width='12') +
                              '{:{align}{width}}'.format(ask_Data[0][i], align='>', width='12') +
                              '{:{align}{width}}'.format(" "+ask_Data[1][i], align='<', width='12'))
                        ask_Weight += int(ask_Data[1][i])
                        #bid_Weight += int(bid_Data[1][i])

                total_Weight = ask_Weight + bid_Weight
                
                print('{:{align}{width}}'.format(str(((bid_Weight / total_Weight)*100))+" %", align='^', width='24') +
                      '{:{align}{width}}'.format(str(((ask_Weight / total_Weight)*100))+" %", align='^', width='24'))
                
            except Exception as e:
                    print("Error in output; output else-for loop:", e)

    except Exception as e:
        print("Error in show_Output, printing data:", e)

                
try:
    for i in range(100):
        timer(show_Output)
except Exception as e:
    print("interupted, ending now!", e)
