from py2neo import Relationship, Node, Graph
import re
import csv

graph = Graph('http://localhost:7474/db/data', user='neo4j', password='gbpltwdctve')

datasPC_AMD = graph.data('MATCH (r:Memorys)-[:RAM]->(m:Motherboards{manufacturer:"AMD"})<-[:CPU]-(c:CPU) return r.name as Memory, '
                     'r.type_ram as Type_RAM, r.volume as Volume_Gb, r.price as Price_Mem, r.capacity as Capacity, '
                     'm.name as Motherboards, m.socket as Socket, m.manufacturer as manufacturer, m.price as Price_Mather, m.form_factor as Form_factor, '
                     'c.name as CPU, c.core_num as Core_Number, c.cpu_frequency as Frequency, c.price as Price_CPU LIMIT 10')
datasPC_Intel = graph.data('MATCH (r:Memorys)-[:RAM]->(m:Motherboards{manufacturer:"Intel"})<-[:CPU]-(c:CPU) return r.name as Memory, '
                     'r.type_ram as Type_RAM, r.volume as Volume_Gb, r.price as Price_Mem, r.capacity as Capacity, '
                     'm.name as Motherboards, m.socket as Socket, m.manufacturer as manufacturer, m.price as Price_Mather, m.form_factor as Form_factor, '
                     'c.name as CPU, c.core_num as Core_Number, c.cpu_frequency as Frequency, c.price as Price_CPU LIMIT 10')
datasVideo = graph.data('MATCH (n:VideoCards) RETURN n.volume as volume_video, n.shina as Shina, n.price as Price_Video LIMIT 25')
datasHDD = graph.data('MATCH (n:HDD{type_hdd:"Твердотельный накопитель"}) RETURN n.volume_hdd as volume_hdd, n.price as Price_HDD LIMIT 25')
datasPS = graph.data('MATCH (r:PS) RETURN r.col_power as col_power, r.price as price LIMIT 25')

def write_cvs(datas):
    with open('data/System_unit.cvs', 'a') as f:
        for data in datas:
            writer = csv.writer(f)
            writer.writerow((data['core_number'],
                             data['socket'],
                             data['frequency'],
                             data['form_factor'],
                             data['value_mem'],
                             data['type_memory'],
                             data['capacity_memory'],
                             data['value_video'],
                             data['volume_hdd'],
                             data['col_power'],
                             data['price']))

datas = []

for dataPC in datasPC_AMD:
    for dataVideo in datasVideo:
        for dataHDD in datasHDD:
            for dataPS in datasPS:
                value = re.findall(r'\d+',dataPC["Volume_Gb"])
                capacity = dataPC["Capacity"]
                capacity = capacity.split()
                value = value[0]
                value_video = re.findall(r'\d+',dataVideo["volume_video"])
                value_video = value_video[0]
                if value_video == "512":
                    value_video = 512 / 1024
                price = float(dataPC['Price_Mem']) + float(dataPC['Price_Mather']) + float(dataPC['Price_CPU']) +float(dataHDD['Price_HDD']) + float(dataVideo['Price_Video']) + float(dataPS['price'])
                data = {
                    'core_number': dataPC["Core_Number"],
                    'socket': dataPC["Socket"],
                    'frequency': dataPC["Frequency"],
                    'form_factor': dataPC["Form_factor"],
                    'value_mem': value,
                    'type_memory': dataPC["Type_RAM"],
                    'capacity_memory': capacity[0],
                    'value_video': value_video,
                    'volume_hdd': dataHDD["volume_hdd"],
                    'col_power': dataPS["col_power"],
                    'price': price
                }
                datas.append(data)
                print("count: %s" % len(datas))
for dataPC in datasPC_Intel:
    for dataVideo in datasVideo:
        for dataHDD in datasHDD:
            for dataPS in datasPS:
                value = re.findall(r'\d+',dataPC["Volume_Gb"])
                capacity = dataPC["Capacity"]
                capacity = capacity.split()
                value = value[0]
                value_video = re.findall(r'\d+',dataVideo["volume_video"])
                value_video = value_video[0]
                if value_video == "512":
                    value_video = 512 / 1024
                price = float(dataPC['Price_Mem']) + float(dataPC['Price_Mather']) + float(dataPC['Price_CPU']) + float(
                    dataHDD['Price_HDD']) + float(dataVideo['Price_Video']) + float(dataPS['price'])
                data = {
                    'core_number': dataPC["Core_Number"],
                    'socket': dataPC["Socket"],
                    'frequency': dataPC["Frequency"],
                    'form_factor': dataPC["Form_factor"],
                    'value_mem': value,
                    'type_memory': dataPC["Type_RAM"],
                    'capacity_memory': dataPC["Capacity"],
                    'value_video': value_video,
                    'volume_hdd': dataHDD["volume_hdd"],
                    'col_power': dataPS["col_power"],
                    'price': price
                }
                datas.append(data)
                print("count: %s" % len(datas))
write_cvs(datas)