# Tera Europe DB Parser | ..a project by VALKYTEQ


Tera Datacenter Parser to create Database Tables  
Project: **_tera-db-parser_**

### Contact:
You can reach out to us over...  
[E-Mail](mailto:admin@valkyteq.com?Subject=Github)   |    [Website](https://tera-europe.net/)   |    [Twitch](https://www.twitch.tv/valkyfischer)   |    [Discord](https://vteq.cc/discord/)

<br><br>

## DB Parser Content
- Read ItemTemplate.xml
- Read StrSheet_Item.xml
- Insert Item Info into DB

<br><br>

## DB Parser Requirements
- Tera Server Datacenter Files
- Tera Client Datacenter Files
- My SQL Database Table

<br><br>

## DB Parser Configuration

### Database Table
Import the ```items.sql``` template into your database  


### Parser Files
Put all ```ItemTemplate``` server xml files into ```/data/Item```  
Put all ```StrSheet_Item``` client xml files into ```/data/StrSheet```  


### Parser Setup
Open ```config.ini``` and adjust:  
```
[Parser]
debug = False           // Verbose output
db_host = 127.0.0.1     // IP for My SQL Server
db_user = root          // User for My SQL Server
db_pass = 12345         // Password for My SQL Server
db_base = tera          // Database for My SQL Server
```
