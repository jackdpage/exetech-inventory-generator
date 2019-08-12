import csv
from shutil import copyfile
import os
import jinja2

FILE = []
NAV = {}
OUTPUT_LOCATION = 'web/'

with open('assets.csv', 'r') as f:
  for i in csv.reader(f):
    FILE.append(i)

FILE.pop(0)

def generate_nav_categories():
  for row in FILE:
    if row[1] not in NAV:
      NAV[row[1]] = {}
    if row[2] not in NAV[row[1]]:
      NAV[row[1]][row[2]] = {}

def copy_resources():
  try:
    os.mkdir(OUTPUT_LOCATION)
  except FileExistsError:
    pass
  try:
    os.mkdir(OUTPUT_LOCATION+'css')
  except FileExistsError:
    pass
  copyfile('css/style.css', OUTPUT_LOCATION+'css/style.css')
  

def generate_nav_pages():
  environment = jinja2.Environment(lstrip_blocks=True, trim_blocks=True, loader=jinja2.FileSystemLoader(['html']))
  template = environment.get_template('index.html')
  index_page = template.render(departments=NAV)
  with open(OUTPUT_LOCATION+'index.html', 'w+') as f:
    f.write(index_page)
  dept_template = environment.get_template('dept.html')
  category_template = environment.get_template('category.html')
  for department in NAV:
    dept_page = dept_template.render(department=department, categories=NAV[department])
    try:
      os.mkdir(OUTPUT_LOCATION+department.lower())
    except FileExistsError:
      pass
    with open(OUTPUT_LOCATION+department.lower()+'/index.html', 'w+') as f:
      f.write(dept_page)
    for category in NAV[department]:
      cat_page = category_template.render(department=department, category=category, items=NAV[department][category])
      with open(OUTPUT_LOCATION+department.lower()+'/'+category.lower()+'.html', 'w+') as f:
        f.write(cat_page)

def generate_indiv_list():
  for row in FILE:
    if row[7] == 'Individual':
      namestr = row[4] + ' ' + row[5]
      category = NAV[row[1]][row[2]]
      if namestr not in category:
        category[namestr] = {'desc': row[6], 'qty': 1}
      else:
        category[namestr]['qty'] += 1
      if row[9] and row[10]:
        category[namestr]['day'] = row[9] 
        category[namestr]['week'] = row[10]
      if row[16]:
        category[namestr]['img'] = row[16]

def generate_kit_list():
  for row in FILE:
    if row[7] == 'Kit':
      namestr = row[8]
      category = NAV[row[1]][row[2]]
      if namestr not in category:
        category[namestr] = {'desc': row[6], 'qty': 1}
      else:
        category[namestr]['qty'] += 1
      if row[9] and row[10]:
        category[namestr]['day'] = row[9]
        category[namestr]['week'] = row[10]
      if row[16]:
        category[namestr]['img'] = row[16]

generate_nav_categories()
generate_indiv_list()
generate_kit_list()
copy_resources()
generate_nav_pages()
