s = """BcraSBNZ.LNZY

`vsbnz` vf gur Clguba vagresnpr gb BcraSBNZ hfvat LNZY pbasvthengvba, gur vavgvny qrirybczrag unf orra pbzcyrgrq, naq V jvyy bcra fbhepr vg nsgre nccylvat sbe gur fbsgjner pbclevtug."""

d = {}
for c in (65, 97):
    for i in range(26):
        d[chr(i+c)] = chr((i+13) % 26 + c)

print("".join([d.get(c, c) for c in s]))
