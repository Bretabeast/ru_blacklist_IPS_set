#!/usr/bin/env python3
import ipaddress
import requests

url = "https://reestr.rublacklist.net/api/v3/ips/"
raw_file = "rublacklist_ipv4_raw.txt"
aggregated_file = "rublacklist_ipv4_aggregated24.txt"

# Скачиваем JSON
print("Скачиваем список IP ...")
resp = requests.get(url, timeout=30)
resp.raise_for_status()
data = resp.json()

# Берём массив IP
if isinstance(data, dict) and "data" in data:
    items = data["data"]
elif isinstance(data, list):
    items = data
else:
    raise ValueError("Неизвестный формат ответа API")

# Фильтруем только IPv4
ipv4_list = []
for item in items:
    ip_str = str(item).strip('"')
    if ip_str.count('.') == 3:
        # убираем CIDR, если есть
        ip_str = ip_str.split('/')[0]
        ipv4_list.append(ip_str)

print(f"Всего IPv4: {len(ipv4_list)}")

# Сохраняем сырой список
with open(raw_file, "w") as f:
    for ip in ipv4_list:
        f.write(ip + "\n")

# Агрегируем в /24
networks = set()
for ip in ipv4_list:
    net = ipaddress.IPv4Network(ip + '/24', strict=False)
    networks.add(str(net))

aggregated = sorted(networks)
with open(aggregated_file, "w") as f:
    for net in aggregated:
        f.write(net + "\n")

print(f"Агрегировано в /24: {len(aggregated)} сетей. Файл {aggregated_file} готов")
