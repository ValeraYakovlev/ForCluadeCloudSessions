import pymol
from pymol import cmd
pymol.finish_launching(['pymol','-cq'])
ECD_RES="29-137"
C_ECD="0xcde2fb"; C_ECDDARK="0x86b6ef"; C_TMD="0xe3e1dc"; C_ORANGE="0xeb6834"; C_BLUE="0x2a78d6"; C_GRAY="0x9a9893"; C_GREEN="0x1baf7a"; C_VIOLET="0x6250d6"; C_MAG="0xe87ba4"
def base(width=2000,height=1500):
    cmd.bg_color("white")
    cmd.set("ray_opaque_background",1)
    cmd.set("antialias",2); cmd.set("ray_shadow",0); cmd.set("depth_cue",0)
    cmd.set("cartoon_fancy_helices",1); cmd.set("cartoon_smooth_loops",1)
    cmd.set("cartoon_loop_radius",0.25); cmd.set("cartoon_oval_length",1.1)
    cmd.set("stick_radius",0.22); cmd.set("sphere_scale",0.25)
    cmd.set("label_font_id",7); cmd.set("label_size",-0.9); cmd.set("label_color","black")
    cmd.set("label_outline_color","white"); cmd.set("label_shadow_mode",0)
    cmd.set("ray_trace_mode",0); cmd.set("specular",0.2); cmd.set("light_count",2)
    cmd.set("cartoon_transparency",0.0); cmd.set("orthoscopic",1)
def lab(sel, text, color="black", pos=None, size=None):
    cmd.label(sel, f'"{text}"')
def save(name,w=2000,h=1500,ray=True):
    cmd.png(f"renders/{name}.png",width=w,height=h,dpi=200,ray=1 if ray else 0)
