import configparser
import urllib.error
import xml.etree.ElementTree as xml
from os.path import exists, isdir
from os import makedirs, listdir
from textblob import TextBlob
from shutil import copyfile
import codecs
import pymysql


def dbConnect(config: dict):
	host = config['Parser']['db_host']
	user = config['Parser']['db_user']
	password = config['Parser']['db_pass']
	database = config['Parser']['db_base']
	charset = 'utf8mb4'
	cursorclass = pymysql.cursors.DictCursor

	conn = pymysql.connect(host=host,user=user,password=password,database=database,charset=charset,cursorclass=cursorclass)
	link = conn.cursor()
	link.execute("SELECT VERSION()")
	data = link.fetchone()
	print (f"Database version: {data['VERSION()']}")
	return link, conn


def readConfig(ini: str) -> dict:
	""" Read config, check for errors and store values

	:param ini: Path to config_wa_gw.ini
	:return: Config as dict
	"""
	# Read config
	config = configparser.ConfigParser()
	config.read(ini)
	# Check debug mode
	if config['Parser']['debug'] == "True":
		print("Debug Mode Enabled")
	return config


# noinspection PyArgumentList
def loadXML(path: str, comments=False, useBackup=False, debug=False):
	if not exists(path): raise Exception(f'Path {path} doesn\'t exist!')
	if useBackup: backup(path, debug)
	parser = xml.XMLParser(target=xml.TreeBuilder(insert_comments=comments))
	tree = xml.parse(path,parser)
	root = tree.getroot()
	if debug: print(f'Loaded {path}')
	return tree, root


def saveXML(path: str, tree: xml.ElementTree, debug=False):
	xml.indent(tree, space='\t')
	tree.write(path, encoding='utf-8-sig',xml_declaration=True)
	string = xml.tostring(tree.getroot(),'unicode').replace('\n','\r\n')
	string = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n{string}"
	if debug: print(f'Saved {path}')
	with codecs.open(path,'w','utf-8-sig') as file:
		file.write(string)


def backup(path, debug=False):
	pybak = path+'.bak'
	if not exists(pybak):
		copyfile(path,pybak)
		if debug: print(f'Created {pybak}')
	return pybak


def getAllXML(path: str):
	files = []
	for file in listdir(f"./data/{path}"):
		if file.endswith(".xml"):
			files.append(file)
	return files


def itemsRead(items: dict, debug=False):
	print(f"Reading Items...")
	type = "Item"
	files = getAllXML(type)
	itemNo = 0
	for file in files:
		treeItem, rootItem = loadXML(path=f'./data/{type}/{file}', debug=debug)
		for item in rootItem.findall('Item'):
			itemNo = itemNo + 1
			itemId = item.get('id')
			# append to dict
			items[itemId] = {}
			items[itemId]['id'] = itemId
			items[itemId]['category'] = item.get('category') if item.get('category') else ''
			items[itemId]['icon'] = item.get('icon') if item.get('icon') else ''
			items[itemId]['name'] = item.get('name') if item.get('name') else ''
			items[itemId]['grade'] = item.get('rareGrade') if item.get('rareGrade') else ''
			items[itemId]['level'] = item.get('level') if item.get('level') else ''
			items[itemId]['classes'] = item.get('requiredClass') if item.get('requiredClass') else ''
			items[itemId]['races'] = item.get('requiredRace') if item.get('requiredRace') else ''
			items[itemId]['gender'] = item.get('requiredGender') if item.get('requiredGender') else ''
			items[itemId]['tradable'] = item.get('tradable') if item.get('tradable') else ''
			items[itemId]['obtainable'] = item.get('obtainable') if item.get('obtainable') else ''
			items[itemId]['dyeable'] = item.get('changeColorEnable') if item.get('changeColorEnable') else ''

	print(f"Reading Items complete: {itemNo}")
	return items


def itemsAddName(items: dict, debug=False):
	print(f"Adding Item Names...")
	type = "StrSheet"
	files = getAllXML(type)
	itemNo = 0
	for file in files:
		treeItem, rootItem = loadXML(path=f'./data/{type}/{file}', debug=debug)
		for item in rootItem.findall('String'):
			itemId = item.get('id')
			# append to dict
			if itemId in items:
				itemNo = itemNo + 1
				items[itemId]['name_de'] = item.get('string')
				items[itemId]['name_en'] = item.get('string')

	print(f"Adding Item Names complete: {itemNo}")
	return items


def itemsInsertDb(items: dict, link, conn) -> bool:
	print(f"Inserting Items...")
	save = True
	itemNo = 0
	for item, data in items.items():
		query_start = f"id='{data['id']}', category='{data['category']}', icon='{data['icon'].replace('.', '/')}', name='{data['name']}', "
		query_mid1 = f"grade='{data['grade']}', level='{data['level']}', classes='{data['classes']}', races='{data['races']}', "
		query_mid2 = f"gender='{data['gender']}', obtainable='{data['obtainable']}', tradable='{data['tradable']}', dyeable='{data['dyeable']}', "
		query_end = f"period='0', periodByWebAdmin='0', name_de='{data['name_de']}', name_en='{data['name_en']}'"

		id = data['id']
		category = data['category']
		icon = data['icon'].replace('.', '/')
		name = data['name']
		grade = data['grade']
		level = data['level']
		classes = data['classes']
		races = data['races']
		gender = data['gender']
		obtainable = data['obtainable']
		tradable = data['tradable']
		dyeable = data['dyeable']
		name_de = data['name_de'].replace('"', "'")
		name_en = data['name_en'].replace('"', "'")

		query = "INSERT INTO items (id, category, icon, name, grade, level, classes, races, gender, obtainable, tradable, dyeable, period, periodByWebAdmin, name_de, name_en) "
		input = f'VALUES ("{id}", "{category}", "{icon}", "{name}", "{grade}", "{level}", "{classes}", "{races}", "{gender}", "{obtainable}", "{tradable}", "{dyeable}", "0", "0", "{name_de}", "{name_en}")'
		try:
			link.execute(query + input)
			conn.commit()
			itemNo = itemNo + 1
		except:
			save = False
			conn.rollback()
			print("Error while writing into Database!")

	if save: print(f"Inserting Items complete: {itemNo}")
	return save


# itemSearch = item.get('searchable')
# itemCombatType = item.get('combatItemType')
# itemCombatSubType = item.get('combatItemSubType')
# itemRank = item.get('rank')
# itemConversion = item.get('conversion')
# itemSortNumber = item.get('sortingNumber')
# itemDropType = item.get('dropType')
# itemBuyPrice = item.get('buyPrice')
# itemSellPrice = item.get('sellPrice')
# itemTerritory = item.get('useOnlyTerritory')
# itemDivide = item.get('divide')
# itemUseCount = item.get('itemUseCount')
# itemDropMax = item.get('maxDropUnit')
# itemStackMax = item.get('maxStack')
# itemSlotLimit = item.get('slotLimit')
# itemCooldownGroup = item.get('coolTimeGroup')
# itemCooldown = item.get('coolTime')
# itemStorable = item.get('warehouseStorable')
# itemStorableGuild = item.get('guildWarehouseStorable')
# itemBoundType = item.get('boundType')
# itemDestroy = item.get('destroyable')
# itemDismantle = item.get('dismantlable')
# itemSellMerchant = item.get('storeSellable')
# itemRelocate = item.get('relocatable')
# itemArtisan = item.get('artisanable')
# itemEnchant = item.get('enchantEnable')
# itemGradeUnknown = item.get('unidentifiedItemGrade')
# itemMasterpieceRate = item.get('masterpieceRate')
# itemLinkEquipId = item.get('linkEquipmentId')
# itemLinkLookId = item.get('linkLookInfoId')
# itemChangeLook = item.get('changeLook')
# itemExtractLook = item.get('extractLook')
