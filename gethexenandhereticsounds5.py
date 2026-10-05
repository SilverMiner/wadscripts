import omg
from datetime import datetime
ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

#src = omg.WAD("HEXEN.WAD")
heretic = omg.WAD("HERETIC.WAD")
hexen   = omg.WAD("HEXEN.WAD")


#src = wad_clone(heretic + hexen)
src = omg.WAD()
for w in (heretic, hexen):
    for group in w.groups:
        dst_g = getattr(src, group._name)
        for name, lump in group.items():
            dst_g[name] = lump
#src = (heretic + hexen).copy()
# Список нужных lump'ов
wanted = ["BSTSIT",
"BELLRNG",
"AMB6",
"BIRD",
"INSECTS1",
"CHAINS",
"BOUNCE",
"CRKETS1",
"CRKETS",
"AMB7",
"AMB3",
"FROGS",
"GONG",
"AMB5",
"AMB1",
"KATYDID",
"KGTSIT",
"SHLURP",
"OWL",
"RAMRAIN",
"BROOK1",
"ROCKS",
"AMB2",
"STEEL1",
"STEEL2",
"AMB4",
"THNDR1",
"WATERFL",
"AMB8",
"WIND",
"WIND3"]


# Создаём новый (пустой) WAD
dst = omg.WAD()

# Переносим только нужное

for name in wanted:
    naiden = False
    #for gname, group in src.groups.items():
    for group in src.groups:
        if name in group:
            gname = group._name
            getattr(dst, gname)[name] = group[name]
            naiden = True
            break
    if naiden:
        print(f"[+] {name} добавлен")
    else:
        print(f"[-] {name} не найден")

dst.to_file(f"out{ts}.wad")
print(f"Готово: out{ts}.wad")
