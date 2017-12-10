import csv
from py2neo import Graph
from json_saver import JsonSaver

computers = "data\computers.csv"

def main():
    graph = Graph('http://localhost:7474/db/data', user='neo4j', password='gbpltwdctve')

    datas_csv = []

    with open(computers, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            count = row[0]
            class_comp = row[12]
            datas_csv.append((count, class_comp))

    datas = []

    datasPC_AMD = graph.data('MATCH (r:Memorys)-[:RAM]->(m:Motherboards{manufacturer:"AMD"})<-[:CPU]-(c:CPU) return r.name as Memory, '
                     'r.type_ram as Type_RAM, r.volume as Volume_Gb, r.price as Price_Mem, r.capacity as Capacity, '
                     'm.name as Motherboards, m.socket as Socket, m.manufacturer as manufacturer, m.price as Price_Mather, m.form_factor as Form_factor, '
                     'c.name as CPU, c.core_num as Core_Number, c.cpu_frequency as Frequency, c.price as Price_CPU ORDER BY rand() LIMIT 10')
    datasPC_Intel = graph.data('MATCH (r:Memorys)-[:RAM]->(m:Motherboards{manufacturer:"Intel"})<-[:CPU]-(c:CPU) return r.name as Memory, '
                     'r.type_ram as Type_RAM, r.volume as Volume_Gb, r.price as Price_Mem, r.capacity as Capacity, '
                     'm.name as Motherboards, m.socket as Socket, m.manufacturer as manufacturer, m.price as Price_Mather, m.form_factor as Form_factor, '
                     'c.name as CPU, c.core_num as Core_Number, c.cpu_frequency as Frequency, c.price as Price_CPU ORDER BY rand() LIMIT 10')
    datasVideo = graph.data('MATCH (n:VideoCards) RETURN n.name as video, n.volume as volume_video, n.shina as Shina, n.price as Price_Video LIMIT 25')
    datasHDD = graph.data('MATCH (n:HDD{type_hdd:"Твердотельный накопитель"}) RETURN n.name as HDD,  n.volume_hdd as volume_hdd, n.price as Price_HDD LIMIT 25')
    datasPS = graph.data('MATCH (r:PS) RETURN r.name as Power, r.col_power as col_power, r.price as price LIMIT 25')

    for dataPC in datasPC_AMD:
        for dataVideo in datasVideo:
            for dataHDD in datasHDD:
                for dataPS in datasPS:
                        price = float(dataPC['Price_Mem']) + float(dataPC['Price_Mather']) + float(
                            dataPC['Price_CPU']) + float(dataHDD['Price_HDD']) + float(
                            dataVideo['Price_Video']) + float(
                            dataPS['price'])
                        Motherboards = dataPC["Motherboards"].split(" ")
                        Motherboards = Motherboards[0] + Motherboards[1]
                        capacity_memory = dataPC["Capacity"].split(" ")
                        capacity_memory = capacity_memory[0] + capacity_memory[1]
                        HDD = dataHDD["HDD"].split(",")
                        HDD = HDD[0] + HDD[-1]
                        data = {
                                #'type_computers': class_computer,
                                'price': int(price),
                                'characteristics':
                                    {
                                        'name_proc': dataPC["CPU"],
                                        'core_number': dataPC["Core_Number"],
                                        'frequency': dataPC["Frequency"],
                                        'Motherboards': Motherboards,
                                        'socket': dataPC["Socket"],
                                        'form_factor': dataPC["Form_factor"],
                                        'Memory': dataPC["Memory"],
                                        'capacity_memory': capacity_memory,
                                        'video': dataVideo["video"],
                                        'shina_video': dataVideo["Shina"],
                                        'HDD': HDD,
                                        'power': dataPS["Power"],
                                    }
                                }
                        datas.append(data)
    JsonSaver.save('data\computers.json', datas)

if __name__ == '__main__':
    print("Start save file...")
    main()




