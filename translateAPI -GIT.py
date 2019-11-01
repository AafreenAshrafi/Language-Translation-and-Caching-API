#Translation API
import urllib.request
import urllib.parse
import re
import xml.etree.ElementTree as ET
import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("-text","--text",required = True,action = 'store')
parser.add_argument("-lang","--lang",required = True,action = 'store')
args = parser.parse_args()
                                                                                              
#print(text1)
#print(lang1)
#reading the input from user side or through HTML
#print('language we support is english,french,german ')

##text1=input('enter your text to be converted ')
##lang1=input('enter the language to convert your text to ')
output=''
text1=args.text
lang1=args.lang

# kn,en,hi,es=spanish,fr =french are the codes used by Google Translate API
for_cache_check=False
if lang1 =='french':
    l2='fr'
    for_cache_check=True

elif lang1 =='english':
    l2='en'
    for_cache_check=True

elif lang1 =='german':
    l2='de'
    for_cache_check=True
else :
    
    print('not supported language')
    for_cache_check=False

#cache check functionality being called first for cached items
   
def cache_check():
    tree = ET.parse('C:/Users/python/Django tutorial/mysite/htranslation/templates/htranslation//cacheFile.xml')
    root = tree.getroot()
    found = False
    for elem in root:
       found = False
       for subelem in elem:
           d = subelem.attrib
           #print (d)
       #for eachattribute,att in enumerate(d):
           #print('call in enumerator')
           if text1 in d['texttochange']:
               if lang1 in d['lang']:
                   #print('in cached file')
                   ans=(subelem.text)
                   print('the word {} in {} is {} \n'.format(text1,lang1,ans))
                   found= True
       if found != True:
            #print('calling main function')
            main_function()

            
#file size check for cache
def file_size(fname):
    global size_file
    statinfo= os.stat(fname)
    size_file =statinfo.st_size
    #print('file size is',size_file)

def main_function():
    #print('in main function')
    u1 ='https://translation.googleapis.com/language/translate/v2?q='
    #print(text1)
    #print(l2)
    u2 ='&target='
    u3 ='*************************************'#add the api key here
    url =u1+text1+u2+l2+u3
    #print(url)

    # passing the URL for request*******************************

    try :
        #print(url)
        headers ={}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url,headers = headers)
        resp = urllib.request.urlopen(req)
        respdata = resp.read()
        savefile = open('withresults.txt','w')
        savefile.write(str(respdata))
        savefile.close()
        #print(respdata)
        answers = re.findall(r'translatedText":\s"(.*?)",\\n',str(respdata))
        for ans in answers:
            print('the word {} in {} is {} \n'.format(text1,lang1,ans))
##            output= ('the word {} in {} is {} \n'.format(text1,lang1,ans))
##        with open("outputhtml.html","w") as fp:
##            fp.write("""<html>
##                     <body>"""+output+"""</body></html>""")     
##            fp.close()
##        savefile = open('cachefile.txt','a')
##        savefile.write(str(output))
##        savefile.close()

        
        file_size("C:/Users/python/Django tutorial/mysite/htranslation/templates/htranslation//cacheFile.xml")
        if (size_file>=352):
            # Write a new file**********************************
            data = ET.Element('data')
            items = ET.SubElement(data,'items')
            item1 = ET.SubElement(items,'item')
            item1.set('texttochange',text1)
            item1.set('lang',lang1)
            item1.text =ans
            mydata = (ET.tostring(data).decode('utf-8'))
            myfile = open('C:/Users/python/Django tutorial/mysite/htranslation/templates/htranslation//cacheFile.xml','w')
            myfile.write(str(mydata))
            myfile.close()

        else:
            #Modify a new file******************************************
            tree = ET.parse('C:/Users/python/Django tutorial/mysite/htranslation/templates/htranslation//cacheFile.xml')
            root = tree.getroot()
            attrib={}
            attrib = {'lang':lang1,'texttochange':text1}
            subelement = root[0].makeelement('item',attrib)
            ET.SubElement(root[0],'item',attrib)
            d=(len(root[0]))
            #print(d)
            root[0][d-1].text =ans
            tree.write('C:/Userspython/Django tutorial/mysite/htranslation/templates/htranslation//cacheFile.xml')
        

    except Exception as e:
        print(str(e))
if for_cache_check==True:
    cache_check()



    

