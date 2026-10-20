# GLP-1R (6X18) key residues by class. Usage: pymol show_hotspots.pml   (run from this folder)
# B-factor column of 6X18_GLP1R_hotspots.pdb = class code (not crystallographic B):
#   receptor: 10 ECD groove (shared) | 20 TMD shared | 30 TMD agonist-selective | 40 structural contact
#   peptide : 50 residues 7-17 (N-terminal module) | 60 residues 18-23 | 70 residues 24-36 (ECD groove helix)
load 6X18_GLP1R_hotspots.pdb, g
bg_color white
hide everything
show cartoon, g
set cartoon_transparency, 0.5, chain R
color grey90, chain R
color 0xcde2fb, chain R and resi 24-137
color 0xeb6834, chain P and b=50
color grey60,   chain P and b=60
color 0x2a78d6, chain P and b=70
select groove,   chain R and b=10
select shared,   chain R and b=20
select agonist,  chain R and b=30
select struct,   chain R and b=40
show sticks, groove or shared or agonist or struct or (chain P and resi 7-15)
color 0x2a78d6, groove and elem C
color 0x1baf7a, shared and elem C
color 0xe87ba4, agonist and elem C
color 0x6b6a66, struct and elem C
color 0xeb6834, chain P and resi 7-15 and elem C
util.cnc
set label_size, -0.7
set label_color, black
label (groove or shared or agonist or struct) and name CA, "%s%s" % (resn, resi)
orient chain R
turn z, 90
