import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Speed':10} {'MTU':6}")
print("-" * 80)

for item in data["imdata"]:
    att = item["l1PhysIf"]["attributes"]
    dn = att["dn"]
    speed = att["speed"]
    mtu = att["mtu"]

    print(f"{dn:50} {speed:10} {mtu:6}")


