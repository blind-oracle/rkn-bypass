#!/usr/bin/python3

import json, urllib.request, ipaddress as ipa

url = 'https://api.reserve-rbl.ru/api/v2/ips/json'
pfx = '24'

dont_summarize = {
    # ipa.IPv4Network('1.1.1.0/24'),
}

dont_add = {
    # ipa.IPv4Address('1.1.1.1'),
}

req = urllib.request.Request(
    url,
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

f = urllib.request.urlopen(req)
ips = json.loads(f.read().decode('utf-8'))

prefix32 = ipa.IPv4Address('255.255.255.255')

r = {}
for i in ips:
    ip = ipa.ip_network(i)
    if not isinstance(ip, ipa.IPv4Network):
        continue

    addr = ip.network_address

    if addr in dont_add:
        continue

    m = ip.netmask
    if m != prefix32:
        r[m] = [addr, 1]
        continue

    sn = ipa.IPv4Network(str(addr) + '/' + pfx, strict=False)

    if sn in dont_summarize:
        tgt = addr
    else:
        tgt = sn

    if not sn in r:
        r[tgt] = [addr, 1]
    else:
        r[tgt][1] += 1

o = []
for n, v in r.items():
    if v[1] == 1:
        o.append(str(v[0]) + '/32')
    else:
        o.append(n)

for k in o:
    print(k)
