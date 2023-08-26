# import library
import re
import numpy as np
from PIL import Image
import easyocr
reader = easyocr.Reader(['en'])
#get all text content of Card
def access_all_elements(bounds):
  list1=[]
  for x in bounds:
    list1.append(x[1])
  return list1
#regular expression to extract phone, email, website link etc
mobile_no=[]
email_id=[]
website=[]
list_index=[]
#content_list=access_all_elements(bounds)
def regular_expression(content_list):
  for i in range(len(content_list)):
    if re.match(r'^[\+]*\d{2,3}-\d{3}-\d{4}$', content_list[i]):
      mobile_no.append(content_list[i])
      list_index.append(i)
    elif re.match(r'^[a-zA-Z]+@[a-zA-Z0-9.-_]+[\s\.]+com$', content_list[i]):
      email_id.append(content_list[i])
      list_index.append(i)
    else:
      if re.match(r'^[wW]{3}[\s\.][a-zA-Z0-9.-_]+[\s\.]+com$', content_list[i]):
        website.append(content_list[i])
        list_index.append(i)
      elif content_list[i]=='WWW' or content_list[i]=='www':
        website.append(content_list[i]+" "+content_list[i+1])
        list_index.append(i)
        list_index.append(i+1)
        i+=1
    i+=1
  temp_list1=content_list.copy()
  try:

    for x in list_index:
      content_list.remove(temp_list1[x])
  except:
    pass

  return content_list
#content_list=regular_expression()

#list creation for futher manipulation
def remaining_manipulation(bounds,content_list):
  lst=[]
  for x in bounds:
    if x[1] in content_list:
      lst.append((x[0],x[1]))
  return lst

#divide category for addess and company name
def divide_category(p1, n):
  cat1=[]
  cat2=[]
  cat1.append((0,0))
  c= abs(p1[0][0][0][1]-p1[0][0][3][1])
  for i in range(1,n):
    if(abs(abs(p1[i][0][0][1]-p1[i][0][3][1])-c)<15):
      cat1.append((i,0))
    else:
      cat2.append((i,1))
  return cat1,cat2

#deciding horizontal & vertical field for address
def horizontal(cat1,lst):
  hor=[]
  vert=[]
  vert.append(cat1[0][0])
  hor.append(cat1[0][0])
  hp=lst[cat1[0][0]][0][0][0]
  for i in range(1,len(cat1)):
    if(abs(lst[cat1[i][0]][0][0][0]-hp)<=5):
      vert.append(cat1[i][0])
    else:
      hor.append(cat1[i][0])
  return hor,vert

#sorting all text of address based on nearest coordinate
import numpy as np
def arrangement(hor,lst):
  temp_lst=[]
  for i in hor:
    temp_lst.append(lst[i][0][0][0])
  arr=np.argsort(temp_lst)
  temp_lst.clear()
  temp_lst1=[]
  for x in arr:
    temp_lst1.append(hor[x])
  return temp_lst1

#complete address
def address(hor, vert, lst):
  i=0
  str1=""
  for x in vert:
    str1+=lst[x][1]+" "
    if(np.array(hor).ndim>i):
      i+=1
      for z in hor[1:]:
        str1+=lst[z][1]+" "
  return str1

#company name
def company_name(cat2,lst):
  str1=""
  for x in cat2:
    str1=str1+lst[x[0]][1]+" "
  return str1

def main_method(image_data):
  image = image_data
  bounds = reader.readtext(image, detail=1)
  name_of_employee = bounds[0][1]
  designation = bounds[1][1]
  del bounds[:2]
  content_list = access_all_elements(bounds)
  content_list = regular_expression(content_list)
  lst=remaining_manipulation(bounds, content_list)
  cat1, cat2 = divide_category(lst, len(lst))
  hor, vert = horizontal(cat1, lst)
  hor = arrangement(hor, lst)
  company_address = address(hor, vert, lst)
  company_name1=company_name(cat2,lst)
  all_contents = company_address.split()
  #print(all_contents)
  # pin code #actually pin code size must be 6 but some images give size 7 that's why I have taken >=6
  pin_code = (all_contents[-1] if len(all_contents[-1]) >= 6 else (all_contents[-1] + all_contents[-2])).rstrip(',:;#^&*@')
  # state_name
  state_name = (all_contents[-2] if len(all_contents[-1]) >= 6 else all_contents[-3]).rstrip(',:;#^&*@')
  # city name
  city_name = (all_contents[-3] if len(all_contents[-1]) >= 6 else all_contents[-4]).rstrip(',:;#^&*@')
  # area name
  area_name = (' '.join([x.rstrip(',:;#^&*@') for x in all_contents[:-3]]) if len(all_contents[-1]) == 6 else ' '.join([x.rstrip(',:;#^&*@') for x in all_contents[:-4]]))
  return (company_name1,name_of_employee,designation,mobile_no,email_id,website,area_name,city_name,state_name,pin_code)
  #return (area_name)

'''
with open('path.txt','r') as f:
  path=f.read()
  res = main_method(path)
  print(res)
'''
#res=main_method(r'./image/1.png')
#print(res)

