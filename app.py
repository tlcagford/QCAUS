"""
QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite
Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026
"""

import streamlit as st
import numpy as np"""
QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite
Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026
"""

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as mcm
from matplotlib.patches import Circle
from PIL import Image, ImageDraw, ImageFont
import io, base64, zipfile, warnings
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter, convolve, uniform_filter

warnings.filterwarnings("ignore")
matplotlib.rcParams["text.usetex"]       = False
matplotlib.rcParams["mathtext.default"]  = "regular"

st.set_page_config(page_title="QCAUS v1.0", page_icon="🔭",
                   layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#0d0f1a;color:#e0e0f0}
[data-testid="stSidebar"]{background:#111320;border-right:1px solid #2a2d4a}
h1,h2,h3,h4{color:#7eb8ff}
[data-testid="stMetricValue"]{color:#00ffaa}
.dl-btn{display:inline-block;padding:6px 14px;background:#1e3a5f;color:white!important;
text-decoration:none;border-radius:5px;margin-top:5px;font-size:13px;border:1px solid #3a6aaf}
.zip-btn{display:inline-block;padding:10px 24px;background:#006633;color:white!important;
text-decoration:none;border-radius:6px;font-size:15px;font-weight:bold;
border:1px solid #00cc66;margin:8px 0}
</style>""", unsafe_allow_html=True)

# ===========================================================================
#  PHYSICS — all formulas verified against repos
# ===========================================================================

def fdm_soliton_2d(size, m_fdm=1.0):
    y,x=np.ogrid[:size,:size]; cx,cy=size//2,size//2
    r=np.sqrt((x-cx)**2+(y-cy)**2)/size*5
    k=np.pi/max(1.0/m_fdm,0.1); kr=k*r
    with np.errstate(divide="ignore",invalid="ignore"):
        sol=np.where(kr>1e-6,(np.sin(kr)/kr)**2,1.0)
    mn,mx=sol.min(),sol.max(); return (sol-mn)/(mx-mn+1e-9)

def fdm_soliton_profile(m_fdm=1.0,n=300):
    r=np.linspace(0,3,n); k=np.pi/max(1.0/m_fdm,0.1); kr=k*r
    return r,np.where(kr>1e-6,(np.sin(kr)/kr)**2,1.0)

def pdp_spectral_duality(image,omega=0.20,fringe=45.0,mixing_angle=0.1,dark_photon_mass=1e-9):
    rows,cols=image.shape; fft_s=fftshift(fft2(image))
    x=np.linspace(-1,1,cols); y=np.linspace(-1,1,rows)
    X,Y=np.meshgrid(x,y); R=np.sqrt(X**2+Y**2)
    L=100.0/max(dark_photon_mass*1e9,1e-6)
    osc=np.sin(2*np.pi*R*L/max(fringe,1.0))
    dmm=(mixing_angle*np.exp(-omega*R**2)*np.abs(osc)*(1-np.exp(-R**2/max(fringe/30,0.1))))
    omm=np.exp(-R**2/max(fringe/30,0.1))-dmm
    return (np.abs(ifft2(fftshift(fft_s*omm))),np.abs(ifft2(fftshift(fft_s*dmm))))

def entanglement_residuals(image,ordinary,dark,strength=0.3,mixing_angle=0.1,fringe=45.0):
    eps=1e-10; tp=np.sum(image**2)+eps
    rho=np.maximum(ordinary**2/tp,eps); S=-rho*np.log(rho)
    xt=(np.abs(ordinary+dark)**2-ordinary**2-dark**2)/tp
    res=S*strength+np.abs(xt)*mixing_angle
    ks=max(3,int(fringe/10)); ks+=ks%2==0
    k=np.outer(np.hanning(ks),np.hanning(ks))
    return convolve(res,k/k.sum(),mode="constant")

def pdp_entanglement_overlay(image,interference,soliton,omega):
    m=omega*0.6
    return np.clip(image*(1-m*0.4)+interference*m*0.5+soliton*m*0.4,0,1)

def generate_interference_pattern(size,fringe,omega):
    y,x=np.ogrid[:size,:size]; cx,cy=size//2,size//2
    r=np.sqrt((x-cx)**2+(y-cy)**2)/size*4; theta=np.arctan2(y-cy,x-cx)
    k=fringe/15.0
    pat=(np.sin(k*4*np.pi*r)*0.5+np.sin(k*2*np.pi*(r+theta/(2*np.pi)))*0.5)
    pat=pat*(1+omega*0.6*np.sin(k*4*np.pi*r)); pat=np.tanh(pat*2)
    return (pat-pat.min())/(pat.max()-pat.min()+1e-9)

def dark_photon_detection_prob(dark_mode,residuals,strength=0.3):
    de=dark_mode/(dark_mode.mean()+0.1)
    lm=uniform_filter(residuals,size=5); re=lm/(lm.mean()+0.1)
    pr=strength; lh=de*re
    return np.clip(gaussian_filter(pr*lh/(pr*lh+(1-pr)+1e-10),sigma=1.0),0,1)

def blue_halo_fusion(image,dark_mode,residuals):
    def pn(a): mn,mx=a.min(),a.max(); return np.sqrt((a-mn)/(mx-mn+1e-10))
    rn,dn,en=pn(image),pn(dark_mode),pn(residuals)
    k=np.ones((5,5))/25; lm=convolve(en,k,mode="constant")
    enh=np.clip(en*(1+2*np.abs(en-lm)),0,1)
    rgb=np.stack([rn,enh,np.clip(gaussian_filter(dn,2.0)+0.3*dn,0,1)],axis=-1)
    return np.clip(rgb**0.45,0,1)

def magnetar_physics(size,B0=1e15,mixing_angle=0.1):
    B_CRIT=4.414e13; alpha=1/137.0
    y,x=np.ogrid[:size,:size]; cx,cy=size//2,size//2
    dx=(x-cx)/(size/4); dy=(y-cy)/(size/4)
    r=np.sqrt(dx**2+dy**2)+0.1; theta=np.arctan2(dy,dx)
    B=(B0/r**3)*np.sqrt(3*np.cos(theta)**2+1)
    Bn=np.clip(B/B.max(),0,1)
    qed=(alpha/(45*np.pi))*(B/B_CRIT)**2; qn=np.clip(qed/(qed.max()+1e-30),0,1)
    conv=(mixing_angle**2)*(1-np.exp(-(B/B_CRIT)**2)); cn=np.clip(conv/(conv.max()+1e-30),0,1)
    return Bn,qn,cn

def qcis_power_spectrum(f_nl=1.0,n_q=0.5,n_s=0.965):
    k=np.logspace(-3,1,300); k0=0.05; q=k/0.2
    T=(np.log(1+2.34*q)/(2.34*q)*(1+3.89*q+(16.2*q)**2+(5.47*q)**3+(6.71*q)**4)**(-0.25))
    Pl=k**n_s*T**2; Pq=Pl*(1+f_nl*(k/k0)**n_q)
    norm=Pl[np.argmin(np.abs(k-k0))]+1e-30
    return k,Pl/norm,Pq/norm

# ===========================================================================
#  PRESETS
# ===========================================================================

def preset_sgr1806(size=400):
    rng=np.random.RandomState(2); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]; dx=(x-cx)/(size/4); dy=(y-cy)/(size/4)
    r=np.sqrt(dx**2+dy**2)+0.05; theta=np.arctan2(dy,dx)
    halo=np.exp(-r*1.5)*np.sqrt(3*np.cos(theta)**2+1)/r
    halo=np.clip(halo/halo.max(),0,1)*0.5
    rc=np.sqrt((x-cx)**2+(y-cy)**2)
    img=halo+np.exp(-rc**2/3.0)+rng.randn(size,size)*0.01
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_crab(size=400):
    rng=np.random.RandomState(1); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]
    dx=(x-cx)/(size*0.22); dy=(y-cy)/(size*0.14); r_ell=np.sqrt(dx**2+dy**2)
    neb=np.exp(-r_ell**2/0.8)*0.7+np.exp(-np.abs(r_ell-0.45)**2/0.015)*0.4
    rc=np.sqrt((x-cx)**2+(y-cy)**2)
    neb+=np.exp(-rc**2/4.0)*0.9+rng.randn(size,size)*0.015
    return np.clip((neb-neb.min())/(neb.max()-neb.min()),0,1)

def preset_galaxy_cluster(size=400):
    rng=np.random.RandomState(4); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]
    dx=(x-cx)/(size*0.15); dy=(y-cy)/(size*0.10); r=np.sqrt(dx**2+dy**2)
    img=np.exp(-7.669*((r/1.0)**0.25-1))
    for ox,oy,rad,amp in [(-0.5,0.3,0.12,0.3),(0.4,-0.4,0.09,0.2),
                           (-0.3,-0.5,0.07,0.15),(0.6,0.2,0.06,0.12)]:
        rs=np.sqrt(((x-cx)/size*2-ox)**2+((y-cy)/size*2-oy)**2)
        img+=amp*np.exp(-rs**2/rad**2)
    img+=rng.randn(size,size)*0.01
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_bullet(size=400):
    rng=np.random.RandomState(7); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]
    r1=np.sqrt(((x-cx-60)/80)**2+((y-cy)/90)**2)
    r2=np.sqrt(((x-cx+80)/50)**2+((y-cy+10)/55)**2)
    theta=np.arctan2(y-cy,x-cx-60); r_arc=np.sqrt((x-cx+20)**2+(y-cy)**2)
    shock=np.exp(-((r_arc-size*0.28)/12)**2)*np.clip(np.cos(theta),0,1)*0.5
    img=np.exp(-r1**2*1.5)+np.exp(-r2**2*2.0)*0.7+shock+rng.randn(size,size)*0.012
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_radar_ppi(size=400):
    rng=np.random.RandomState(10); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]; r=np.sqrt((x-cx)**2+(y-cy)**2)
    img=np.zeros((size,size))
    for rk,amp in [(80,0.9),(140,0.6),(200,0.4),(260,0.25)]:
        img+=amp*np.exp(-((r-rk/400*size/2)**2)/60)
    for ang,rk,amp in [(0.3,100,0.8),(1.1,160,0.6),(-0.8,200,0.7),(2.5,140,0.5)]:
        tx=cx+rk/400*size/2*np.cos(ang); ty=cy+rk/400*size/2*np.sin(ang)
        img+=amp*np.exp(-((x-tx)**2+(y-ty)**2)/25)
    img+=rng.randn(size,size)*0.05
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_radar_sector(size=400):
    rng=np.random.RandomState(11); cx,cy=size-80,size//2
    y,x=np.mgrid[:size,:size]; r=np.sqrt((x-cx)**2+(y-cy)**2)
    theta=np.arctan2(y-cy,x-cx); mask=(theta>-0.52)&(theta<0.52)
    img=np.zeros((size,size))
    for rk,amp in [(100,0.7),(200,0.5),(300,0.3)]:
        img+=amp*np.exp(-((r-rk/400*size)**2)/80)*mask
    for ang,rk,amp in [(0.1,120,1.0),(-0.2,200,0.8),(0.3,280,0.6)]:
        tx=cx+rk/400*size*np.cos(ang); ty=cy+rk/400*size*np.sin(ang)
        img+=amp*np.exp(-((x-tx)**2+(y-ty)**2)/18)
    img+=rng.randn(size,size)*0.04
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_radar_sar(size=400):
    rng=np.random.RandomState(12); img=np.zeros((size,size))
    for freq in [0.02,0.05,0.1,0.2]:
        img+=rng.randn(size,size)*0.3/freq*0.01
    img=gaussian_filter(img,sigma=3)
    img[size//3:size//3+4,:]=0.8; img[2*size//3:2*size//3+4,:]=0.6
    img[:,size//4:size//4+4]=0.7
    for bx,by,bw,bh,amp in [(80,80,30,30,1.0),(200,150,25,20,0.9),
                              (320,100,20,35,0.95),(100,300,40,15,0.85),(280,280,20,20,0.9)]:
        img[by:by+bh,bx:bx+bw]+=amp
    img=gaussian_filter(img,sigma=0.5)+rng.randn(size,size)*0.03
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

PRESETS = {
    "🌌 SGR 1806-20 (Magnetar)":       ("sgr",     preset_sgr1806,        "Magnetar",       0.70,65,"2.5 kpc"),
    "🦀 Crab Nebula M1":                ("crab",    preset_crab,           "Pulsar nebula",  0.60,50,"1.0 kpc"),
    "🌐 Galaxy Cluster (Abell-type)":   ("abell",   preset_galaxy_cluster, "Grav lens",      0.70,65,"50 kpc"),
    "💥 Bullet Cluster 1E0657":         ("bullet",  preset_bullet,         "Merging cluster",0.65,55,"80 kpc"),
    "📡 Radar PPI Scan (Historical)":   ("ppi",     preset_radar_ppi,      "PPI sweep",      0.50,40,"N/A"),
    "📡 Radar Sector Scan (Historical)":("sector",  preset_radar_sector,   "Sector scan",    0.50,40,"N/A"),
    "🛰️ SAR Ground Mapping":            ("sar",     preset_radar_sar,      "SAR terrain",    0.55,45,"N/A"),
}

# ===========================================================================
#  ANNOTATED COMPOSITE — matches reference image
# ===========================================================================

def _font(sz):
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","arial.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]:
        try: return ImageFont.truetype(path,sz)
        except: pass
    return ImageFont.load_default()

def build_annotated_composite(before_gray,after_rgb,omega,fringe,
                               mixing,entropy,r_fdm,source_label,scale_label):
    H,W=before_gray.shape
    bef=Image.fromarray(np.clip(before_gray*255,0,255).astype(np.uint8)).convert("RGB")
    aft=Image.fromarray(np.clip(after_rgb*255,0,255).astype(np.uint8))
    gap=10; bar=40
    comp=Image.new("RGB",(W*2+gap,H+bar),(5,5,15))
    comp.paste(bef,(0,0)); comp.paste(aft,(W+gap,0))
    draw=ImageDraw.Draw(comp)
    fb,fs,ft=_font(14),_font(12),_font(11)

    def annotate(ox,title_main,title_sub):
        lines=[f"Ω = {omega:.2f}  |  Fringe = {fringe}",
               f"Mixing = {mixing:.3f}  |  Entropy = {entropy:.3f}",
               f"ρ_FDM = {r_fdm}"]
        cols=["#00ffcc","#44ddff","#55eeaa"]
        for i,(ln,col) in enumerate(zip(lines,cols)):
            draw.text((ox+8,6+i*17),ln,fill=col,font=fs)
        bw,bh=220,48; bx=ox+W-bw-8
        draw.rectangle([bx,4,bx+bw,4+bh],fill=(0,0,0),outline=(200,200,200),width=1)
        draw.text((bx+7,8),title_main,fill="white",font=ft)
        draw.text((bx+7,24),title_sub,fill="#aaccff",font=ft)
        ax2,ay2=ox+W-22,13
        draw.line([(ax2,ay2+20),(ax2,ay2)],fill="white",width=2)
        draw.polygon([(ax2,ay2),(ax2-4,ay2+8),(ax2+4,ay2+8)],fill="white")
        draw.text((ax2-3,ay2+21),"N",fill="white",font=_font(10))
        bar_px=80; by=H-28
        draw.line([(ox+18,by),(ox+18+bar_px,by)],fill="white",width=3)
        draw.line([(ox+18,by-4),(ox+18,by+4)],fill="white",width=2)
        draw.line([(ox+18+bar_px,by-4),(ox+18+bar_px,by+4)],fill="white",width=2)
        draw.text((ox+22,by+4),scale_label,fill="white",font=fs)

    annotate(0,"Before: Standard View",f"({source_label})")
    annotate(W+gap,"After: Photon-Dark-Photon Entangled","FDM Overlays (Tony Ford Model)")
    draw.rectangle([0,H,W*2+gap,H+bar],fill=(10,10,25))
    draw.text((10,H+12),"QCAUS v1.0  |  Tony E. Ford  |  tlcagford@gmail.com  |  Patent Pending  |  2026",
              fill="#445577",font=ft)
    return comp

# ===========================================================================
#  VISUAL OVERLAY — green FDM rings, orange speckles, blue halo
# ===========================================================================

def build_after_rgb(img_gray,soliton,interf,dark_mode,ent_res):
    H,W=img_gray.shape; out=np.zeros((H,W,3),dtype=np.float32)
    out[...,0]=img_gray*0.5; out[...,1]=img_gray*0.2; out[...,2]=img_gray*0.15
    fdm_g=soliton*interf
    fdm_n=(fdm_g-fdm_g.min())/(fdm_g.max()-fdm_g.min()+1e-9)
    rings=np.clip(fdm_n*2.5,0,1)
    out[...,1]+=rings*0.85
    ent_n=(ent_res-ent_res.min())/(ent_res.max()-ent_res.min()+1e-9)
    sp=gaussian_filter(ent_n,sigma=1.5)*(1-rings*0.7)
    out[...,0]+=sp*0.8; out[...,1]+=sp*0.3
    dm_n=(dark_mode-dark_mode.min())/(dark_mode.max()-dark_mode.min()+1e-9)
    dm_b=gaussian_filter(dm_n,sigma=4)
    out[...,2]+=dm_b*0.9; out[...,1]+=dm_b*0.2
    bright=img_gray>0.85
    out[bright,0]=np.clip(out[bright,0]+0.8,0,1)
    out[bright,1]=np.clip(out[bright,1]+0.6,0,1)
    out[bright,2]=np.clip(out[bright,2]+0.3,0,1)
    return np.clip(out,0,1)

# ===========================================================================
#  UTILITIES
# ===========================================================================

def load_and_square(file,mx=400):
    img=Image.open(file).convert("L")
    if max(img.size)>mx: img.thumbnail((mx,mx),Image.LANCZOS)
    w,h=img.size; s=min(w,h)
    img=img.crop(((w-s)//2,(h-s)//2,(w+s)//2,(h+s)//2))
    return np.array(img,dtype=np.float32)/255.0

def _cmap(arr,name):
    return (mcm.get_cmap(name)(np.clip(arr,0,1))[...,:3]*255).astype(np.uint8)

def to_pil(arr,cmap=None):
    if arr.ndim==2:
        if cmap: return Image.fromarray(_cmap(arr,cmap),"RGB")
        return Image.fromarray(np.clip(arr*255,0,255).astype(np.uint8),"L")
    return Image.fromarray(np.clip(arr*255,0,255).astype(np.uint8),"RGB")

def b64png(pil_img):
    buf=io.BytesIO(); pil_img.save(buf,format="PNG"); return base64.b64encode(buf.getvalue()).decode()

def dl(arr,fname,label="📥 Download",cmap=None,cls="dl-btn"):
    b=b64png(to_pil(arr,cmap))
    return f'<a href="data:image/png;base64,{b}" download="{fname}" class="{cls}">{label}</a>'

def make_zip(files):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as zf:
        for fname,obj in files.items():
            if isinstance(obj,np.ndarray): obj=to_pil(obj)
            if isinstance(obj,Image.Image):
                ib=io.BytesIO(); obj.save(ib,format="PNG"); ib.seek(0); zf.writestr(fname,ib.getvalue())
            elif isinstance(obj,bytes): zf.writestr(fname,obj)
    buf.seek(0); return buf.getvalue()

def fig_bytes(fig):
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); buf.seek(0); return buf.getvalue()

# ===========================================================================
#  SIDEBAR
# ===========================================================================
with st.sidebar:
    st.markdown("## ⚛️ Core Physics")
    omega_pd    =st.slider("Omega_PD Entanglement",0.05,0.70,0.20,0.01)
    fringe_scale=st.slider("Fringe Scale (pixels)",10,80,65,1)
    kin_mix     =st.slider("Kinetic Mixing eps",1e-12,1e-8,1e-10,format="%.1e")
    fdm_mass    =st.slider("FDM Mass x10^-22 eV",0.10,10.00,1.00,0.01)
    st.markdown("---")
    st.markdown("## 🌟 Magnetar")
    b0_log10   =st.slider("B0 log10 G",13.0,16.0,15.0,0.1)
    magnetar_eps=st.slider("Magnetar eps",0.01,0.50,0.10,0.01)
    st.markdown("---")
    st.markdown("## 📈 QCIS")
    f_nl=st.slider("f_NL",0.00,5.00,1.00,0.01)
    n_q =st.slider("n_q",0.00,2.00,0.50,0.01)
    st.markdown("---")
    st.markdown("**Tony Ford | tlcagford@gmail.com**\n\n**Patent Pending | 2026**")

# ===========================================================================
#  MAIN UI
# ===========================================================================
st.markdown('<h1 style="text-align:center;color:#7eb8ff">🔭 QCAUS v1.0</h1>',unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#8899bb">FDM · PDP · Magnetar · QCIS · EM Spectrum · Historical Radar</p>',unsafe_allow_html=True)

st.markdown("### Preset Data — click any to run instantly")
cols=st.columns(len(PRESETS))
chosen=None
for col,(label,meta) in zip(cols,PRESETS.items()):
    with col:
        if st.button(label,use_container_width=True): chosen=label

st.markdown("### — OR upload your own —")
uploaded=st.file_uploader("Drag & drop FITS / JPG / PNG",
                           type=["jpg","jpeg","png","fits"],label_visibility="collapsed")

img_data=None; source_name="Public HST/JWST Data"; scale_label="20 kpc"

if uploaded is not None:
    img_data=load_and_square(uploaded); source_name=uploaded.name
    st.success(f"✅ Loaded: {source_name}")
elif chosen and chosen in PRESETS:
    key,fn,desc,d_om,d_fr,d_sc=PRESETS[chosen]
    img_data=fn(); source_name=f"{chosen.split('(')[0].strip()} — {desc}"
    scale_label=d_sc; st.info(f"📁 {chosen}")
else:
    st.markdown("""
### 🔭 QCAUS v1.0 — Verified Physics Formulas

| Module | Formula | Source |
|--------|---------|--------|
| **FDM Soliton** | ρ(r)=ρ₀[sin(kr)/(kr)]²  k=π/r_s | QCAUS/app.py |
| **PDP Spectral Duality** | FFT dark_mask  osc_len=100/(m·1e9) | pdp_radar_core.py |
| **Entanglement Residuals** | S=−ρ·log(ρ)+cross-term | pdp_radar_core.py |
| **Dark Photon Detection** | Bayesian P_dark=prior·L/(prior·L+(1-prior)) | pdp_radar_core.py |
| **Blue-Halo Fusion** | R=orig G=residuals B=dark γ=0.45 | pdp_radar_core.py |
| **Magnetar Dipole** | B=B₀(R/r)³√(3cos²θ+1) B_crit=4.414×10¹³G | Magnetar repo |
| **Euler-Heisenberg QED** | ΔL=(α/45π)(B/B_crit)² α=1/137 | Magnetar repo |
| **Dark Photon Conversion** | P_conv=ε²(1−exp(−(B/B_crit)²)) | Magnetar repo |
| **QCIS Power Spectrum** | P(k)=P_ΛCDM(k)×(1+f_NL(k/k₀)^n_q) BBKS n_s=0.965 | QCIS repo |
""")

# ===========================================================================
#  PROCESSING
# ===========================================================================
if img_data is not None:
    B0=10**b0_log10; B_CRIT=4.414e13
    if img_data.ndim==3: ig=np.mean(img_data,axis=-1).astype(np.float32)
    else: ig=img_data.astype(np.float32)
    h,w=ig.shape; SIZE=min(h,w)
    if h!=w:
        p=Image.fromarray((ig*255).astype(np.uint8))
        ig=np.array(p.resize((SIZE,SIZE),Image.LANCZOS),dtype=np.float32)/255.0

    sol  =fdm_soliton_2d(SIZE,fdm_mass)
    intr =generate_interference_pattern(SIZE,fringe_scale,omega_pd)
    orm,dm=pdp_spectral_duality(ig,omega_pd,fringe_scale,kin_mix*1e9,1e-9)
    eres =entanglement_residuals(ig,orm,dm,omega_pd*0.3,kin_mix*1e9,fringe_scale)
    pdpo =pdp_entanglement_overlay(ig,intr,sol,omega_pd)
    fus  =blue_halo_fusion(ig,dm,eres)
    dpp  =dark_photon_detection_prob(dm,eres,omega_pd*0.3)
    dp_pk=float(dpp.max()*100)
    Bn,qn,cn=magnetar_physics(SIZE,B0,magnetar_eps)
    k_a,Pl,Pq=qcis_power_spectrum(f_nl,n_q)
    ra,rha=fdm_soliton_profile(fdm_mass)

    mix_v =float(omega_pd*0.6)
    ent_v =float(-np.mean(eres[eres>0]*np.log(eres[eres>0]+1e-10))) if eres.max()>0 else 0.0
    rfdm_s=f"{1/fdm_mass:.1f} kpc"

    after_rgb=build_after_rgb(ig,sol,intr,dm,eres)
    comp=build_annotated_composite(ig,after_rgb,omega_pd,fringe_scale,
                                   mix_v,ent_v,rfdm_s,source_name,scale_label)

    # HERO
    st.markdown("---")
    st.markdown("## 🖼️ Annotated Before vs After")
    st.image(comp,use_container_width=True)

    # Build all plot bytes
    def make_mag_plot():
        Bc=4.414e13; al=1/137.0; rm=10; gs=100
        xg=np.linspace(-rm,rm,gs); yg=np.linspace(-rm,rm,gs)
        Xg,Yg=np.meshgrid(xg,yg); Rg=np.maximum(np.sqrt(Xg**2+Yg**2),0.2); thg=np.arctan2(Yg,Xg)
        Br2=B0*(1/Rg)**3*2*np.cos(thg); Bt2=B0*(1/Rg)**3*np.sin(thg)
        Bx2=Br2*np.cos(thg)-Bt2*np.sin(thg); By2=Br2*np.sin(thg)+Bt2*np.cos(thg)
        Bt=np.sqrt(Bx2**2+By2**2)
        EHg=(al/(45*np.pi))*(Bt/Bc)**2
        dpc=(magnetar_eps**2)*(1-np.exp(-(Bt/Bc)**2))
        fig2,axs=plt.subplots(2,2,figsize=(12,10),facecolor="#0d0f1a")
        for ax in axs.flat: ax.set_facecolor("#111320"); ax.tick_params(colors="white"); ax.grid(True,alpha=0.2)
        axs[0,0].streamplot(Xg,Yg,Bx2,By2,color=np.log10(Bt+1e-10),cmap="plasma",density=1.2)
        axs[0,0].add_patch(Circle((0,0),1,color="white",zorder=5))
        axs[0,0].set_title(f"B=B0(R/r)^3 sqrt(3cos2th+1)  B0={B0:.2e}G",color="white",fontsize=10)
        im2=axs[0,1].imshow(EHg/(EHg.max()+1e-30),extent=[-rm,rm,-rm,rm],origin="lower",cmap="inferno")
        axs[0,1].set_title("Euler-Heisenberg  dL=(a/45pi)(B/Bc)^2  a=1/137",color="white",fontsize=10)
        plt.colorbar(im2,ax=axs[0,1])
        im3=axs[1,0].imshow(dpc/(dpc.max()+1e-30),extent=[-rm,rm,-rm,rm],origin="lower",cmap="hot")
        axs[1,0].set_title(f"P_conv=e^2*(1-exp(-(B/Bc)^2))  e={magnetar_eps:.3f}",color="white",fontsize=10)
        plt.colorbar(im3,ax=axs[1,0])
        r1=np.linspace(1.1,rm,200); B1=B0*(1/r1)**3*2
        EH1=(al/(45*np.pi))*(B1/Bc)**2; dp1=(magnetar_eps**2)*(1-np.exp(-(B1/Bc)**2))
        axs[1,1].semilogy(r1,B1,"b-",lw=2,label="|B| on-axis")
        axs[1,1].set_ylabel("|B| (G)",color="b"); axs[1,1].tick_params(axis="y",labelcolor="b")
        ax2t=axs[1,1].twinx()
        ax2t.plot(r1,EH1/(EH1.max()+1e-30),"r--",lw=2,label="dL norm.")
        ax2t.plot(r1,dp1/(dp1.max()+1e-30),"g-.",lw=2,label="P_conv norm.")
        ax2t.set_ylim(0,1); ax2t.set_ylabel("Normalised",color="r")
        axs[1,1].set_title("Radial Profiles on-axis",color="white",fontsize=10)
        l1,lb1=axs[1,1].get_legend_handles_labels(); l2,lb2=ax2t.get_legend_handles_labels()
        axs[1,1].legend(l1+l2,lb1+lb2,fontsize=9)
        plt.suptitle(f"Magnetar QED  B0=10^{b0_log10:.1f}G  eps={magnetar_eps:.3f}  Bcrit=4.414e13G",color="white",fontsize=12)
        plt.tight_layout(); b=fig_bytes(fig2); plt.close(fig2); return b

    def make_ps_plot():
        fig3,ax3=plt.subplots(figsize=(10,4),facecolor="#0d0f1a")
        ax3.set_facecolor("#111320"); ax3.tick_params(colors="white")
        ax3.loglog(k_a,Pl,"b-",lw=2,label="ΛCDM baseline")
        ax3.loglog(k_a,Pq,"r--",lw=2,label=f"Quantum f_NL={f_nl:.1f} n_q={n_q:.1f}")
        ax3.axvline(0.05,color="gray",ls=":",alpha=0.5)
        ax3.set_xlabel("k (h/Mpc)",color="white"); ax3.set_ylabel("P(k)/P(k0)",color="white")
        ax3.set_title("QCIS Power Spectrum  BBKS T(k)  n_s=0.965",color="white")
        ax3.legend(labelcolor="white"); ax3.grid(True,alpha=0.3,which="both")
        plt.tight_layout(); b=fig_bytes(fig3); plt.close(fig3); return b

    def make_fdm_plot():
        fig4,ax4=plt.subplots(figsize=(9,3),facecolor="#0d0f1a")
        ax4.set_facecolor("#111320"); ax4.tick_params(colors="white")
        ax4.plot(ra,rha,"r-",lw=2.5,label=f"rho(r)=rho0[sin(kr)/(kr)]^2  m={fdm_mass:.1f}x10^-22 eV")
        ax4.set_xlabel("r (kpc)",color="white"); ax4.set_ylabel("rho(r)/rho0",color="white")
        ax4.set_title("FDM Soliton — Schrödinger-Poisson ground state",color="white")
        ax4.legend(labelcolor="white"); ax4.grid(True,alpha=0.3)
        plt.tight_layout(); b=fig_bytes(fig4); plt.close(fig4); return b

    mag_b=make_mag_plot(); ps_b=make_ps_plot(); fdm_b=make_fdm_plot()

    # ZIP ALL
    st.markdown("---")
    st.markdown("## 📦 Download All Results")
    zfiles={
        "01_annotated_comparison.png": comp,
        "02_original.png":             to_pil(ig,"gray"),
        "03_after_visual_overlay.png": to_pil(after_rgb),
        "04_fdm_soliton.png":          to_pil(sol,"hot"),
        "05_pdp_interference.png":     to_pil(intr,"plasma"),
        "06_entanglement_residuals.png":to_pil(eres,"inferno"),
        "07_pdp_entangled.png":        to_pil(pdpo,"inferno"),
        "08_dark_photon_detection.png":to_pil(dpp,"YlOrRd"),
        "09_blue_halo_fusion.png":     to_pil(fus),
        "10_magnetar_Bfield.png":      to_pil(Bn,"plasma"),
        "11_magnetar_QED.png":         to_pil(qn,"inferno"),
        "12_magnetar_darkconv.png":    to_pil(cn,"hot"),
        "13_magnetar_qed_plot.png":    mag_b,
        "14_qcis_power_spectrum.png":  ps_b,
        "15_fdm_soliton_profile.png":  fdm_b,
    }
    zb=make_zip(zfiles); zb64=base64.b64encode(zb).decode()
    st.markdown(f'<a href="data:application/zip;base64,{zb64}" download="QCAUS_all_results.zip" class="zip-btn">📦 Download ALL {len(zfiles)} Results as ZIP</a>',unsafe_allow_html=True)
    st.markdown(dl(comp,"annotated_comparison.png","📥 Download Annotated Composite"),unsafe_allow_html=True)

    # METRICS
    st.markdown("---")
    m1,m2,m3,m4,m5=st.columns(5)
    m1.metric("P_dark Peak",f"{dp_pk:.1f}%",delta=f"eps={kin_mix:.1e}")
    m2.metric("FDM Soliton Peak",f"{float(sol.max()):.3f}",delta=f"m={fdm_mass:.1f}")
    m3.metric("Fringe Contrast",f"{float(intr.std()):.3f}",delta=f"f={fringe_scale}")
    m4.metric("PDP Mixing Ω·0.6",f"{omega_pd*0.6:.3f}",delta=f"Ω={omega_pd:.2f}")
    m5.metric("B/B_crit",f"{B0/B_CRIT:.2e}",delta=f"10^{b0_log10:.1f}")
    if dp_pk>50: st.error(f"STRONG DARK PHOTON SIGNAL — P_dark={dp_pk:.0f}%")
    elif dp_pk>20: st.warning(f"DARK PHOTON SIGNAL — P_dark={dp_pk:.0f}%")
    else: st.success(f"CLEAR — P_dark={dp_pk:.0f}%")

    # INDIVIDUAL PANELS
    st.markdown("---")
    st.markdown("## 📊 Individual Physics Maps")
    st.markdown("### FDM · PDP · Residuals")
    c1,c2,c3=st.columns(3)
    for col,(arr,cmap,title,fname) in zip([c1,c2,c3],[
        (sol,"hot","⚛️ FDM Soliton  ρ(r)=ρ₀[sin(kr)/(kr)]²","fdm_soliton.png"),
        (intr,"plasma","🌊 PDP Interference  osc_len=100/(m·1e9)","pdp_interference.png"),
        (eres,"inferno","🕳️ Entanglement Residuals  S=−ρlogρ+xt","ent_residuals.png"),
    ]):
        with col:
            st.markdown(f"**{title}**"); st.image(to_pil(arr,cmap),use_container_width=True)
            st.markdown(dl(arr,fname,cmap=cmap),unsafe_allow_html=True)

    st.markdown("### Dark Photon · Blue-Halo · Visual Overlay")
    c1,c2,c3=st.columns(3)
    for col,(arr,cmap,title,fname) in zip([c1,c2,c3],[
        (dpp,"YlOrRd","🔵 Dark Photon Detection  Bayesian P_dark","dp_detection.png"),
        (fus,None,"💙 Blue-Halo Fusion  R=orig G=res B=dark γ=0.45","blue_halo.png"),
        (after_rgb,None,"🎨 Visual Overlay (FDM rings + PDP halo)","after_overlay.png"),
    ]):
        with col:
            st.markdown(f"**{title}**"); st.image(to_pil(arr,cmap),use_container_width=True)
            st.markdown(dl(arr,fname,cmap=cmap),unsafe_allow_html=True)

    st.markdown("### Magnetar QED Maps")
    cA,cB,cC=st.columns(3)
    for col,(arr,cmap,title,fname) in zip([cA,cB,cC],[
        (Bn,"plasma","B=B₀(R/r)³√(3cos²θ+1)","magnetar_B.png"),
        (qn,"inferno","Euler-Heisenberg ΔL=(α/45π)(B/Bc)²","magnetar_QED.png"),
        (cn,"hot","P_conv=ε²(1−e^{−(B/Bc)²})","magnetar_darkconv.png"),
    ]):
        with col:
            st.markdown(f"**{title}**"); st.image(to_pil(arr,cmap),use_container_width=True)
            st.markdown(dl(arr,fname,cmap=cmap),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## ⚡ Magnetar QED — 4-Panel")
    st.image(mag_b,use_container_width=True)
    mb64=base64.b64encode(mag_b).decode()
    st.markdown(f'<a href="data:image/png;base64,{mb64}" download="magnetar_qed.png" class="dl-btn">📥 Download Magnetar Plot</a>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## ⚛️ FDM Soliton Radial Profile")
    st.image(fdm_b,use_container_width=True)
    fb64=base64.b64encode(fdm_b).decode()
    st.markdown(f'<a href="data:image/png;base64,{fb64}" download="fdm_profile.png" class="dl-btn">📥 Download FDM Profile</a>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📈 QCIS Power Spectrum")
    st.image(ps_b,use_container_width=True)
    pb64=base64.b64encode(ps_b).decode()
    st.markdown(f'<a href="data:image/png;base64,{pb64}" download="qcis_spectrum.png" class="dl-btn">📥 Download QCIS Spectrum</a>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🌈 EM Spectrum Mapping")
    k2,Pl2,Pq2=qcis_power_spectrum(f_nl,n_q)
    qf=np.clip(float(Pq2[np.argmin(np.abs(k2-0.1))]/(Pl2[np.argmin(np.abs(k2-0.1))]+1e-30)),0.5,3.0)
    ir2=np.clip(ig**0.5*qf,0,1); vi2=np.clip(ig**0.8*qf,0,1); xr2=np.clip(ig**1.5*qf,0,1)
    em2=np.stack([ir2,vi2,xr2],axis=-1)
    ce1,ce2=st.columns(2)
    with ce1:
        st.markdown("**🎨 EM Composite**"); st.image(to_pil(em2),use_container_width=True)
        st.markdown(dl(em2,"em_composite.png"),unsafe_allow_html=True)
    with ce2:
        st.markdown("**📊 EM Bands**")
        t1,t2,t3=st.tabs(["🔴 Infrared","🟢 Visible","🔵 X-ray"])
        with t1:
            st.image(_cmap(ir2,"hot"),use_container_width=True)
            st.markdown("*λ~10-1000 μm*")
            st.markdown(dl(ir2,"infrared.png",cmap="hot"),unsafe_allow_html=True)
        with t2:
            st.image(_cmap(vi2,"viridis"),use_container_width=True)
            st.markdown("*λ~400-700 nm*")
            st.markdown(dl(vi2,"visible.png",cmap="viridis"),unsafe_allow_html=True)
        with t3:
            st.image(_cmap(xr2,"plasma"),use_container_width=True)
            st.markdown("*λ~0.01-10 nm*")
            st.markdown(dl(xr2,"xray.png",cmap="plasma"),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📡 Verified Physics Formulas")
    st.markdown("""
| Module | Formula | Source |
|--------|---------|--------|
| **FDM Soliton** | ρ(r)=ρ₀[sin(kr)/(kr)]²  k=π/r_s | QCAUS/app.py |
| **PDP Spectral Duality** | FFT dark_mask=ε·exp(-ΩR²)·abs(sin(2πRL/f))·(1-exp(-R²/f)) | pdp_radar_core.py |
| **Entanglement Residuals** | S=-ρ·log(ρ)+abs(ψ_ord+ψ_dark)²-ψ_ord²-ψ_dark² | pdp_radar_core.py |
| **Dark Photon Detection** | P_dark=prior·L/(prior·L+(1-prior)) Bayesian | pdp_radar_core.py |
| **Blue-Halo Fusion** | R=original G=residuals B=dark γ=0.45 | pdp_radar_core.py |
| **Magnetar Dipole** | B=B₀(R/r)³√(3cos²θ+1) B_crit=4.414×10¹³G | Magnetar repo |
| **Euler-Heisenberg QED** | ΔL=(α/45π)(B/B_crit)² α=1/137 | Magnetar repo |
| **Dark Photon Conversion** | P_conv=ε²(1−exp(−(B/B_crit)²)) | Magnetar repo |
| **QCIS Power Spectrum** | P(k)=P_ΛCDM(k)×(1+f_NL(k/k₀)^n_q) BBKS n_s=0.965 | QCIS repo |
""")

st.markdown("---")
st.markdown('<p style="color:#445577;text-align:center">🔭 QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite | Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026</p>',unsafe_allow_html=True)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as mcm
from matplotlib.patches import Circle
from PIL import Image, ImageDraw, ImageFont
import io, base64, zipfile, warnings
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter, convolve, uniform_filter

warnings.filterwarnings("ignore")
matplotlib.rcParams["text.usetex"]       = False
matplotlib.rcParams["mathtext.default"]  = "regular"

st.set_page_config(page_title="QCAUS v1.0", page_icon="🔭",
                   layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#0d0f1a;color:#e0e0f0}
[data-testid="stSidebar"]{background:#111320;border-right:1px solid #2a2d4a}
h1,h2,h3,h4{color:#7eb8ff}
[data-testid="stMetricValue"]{color:#00ffaa}
.dl-btn{display:inline-block;padding:6px 14px;background:#1e3a5f;color:white!important;
text-decoration:none;border-radius:5px;margin-top:5px;font-size:13px;border:1px solid #3a6aaf}
.zip-btn{display:inline-block;padding:10px 24px;background:#006633;color:white!important;
text-decoration:none;border-radius:6px;font-size:15px;font-weight:bold;
border:1px solid #00cc66;margin:8px 0}
</style>""", unsafe_allow_html=True)

# ===========================================================================
#  PHYSICS — all formulas verified against repos
# ===========================================================================

def fdm_soliton_2d(size, m_fdm=1.0):
    y,x=np.ogrid[:size,:size]; cx,cy=size//2,size//2
    r=np.sqrt((x-cx)**2+(y-cy)**2)/size*5
    k=np.pi/max(1.0/m_fdm,0.1); kr=k*r
    with np.errstate(divide="ignore",invalid="ignore"):
        sol=np.where(kr>1e-6,(np.sin(kr)/kr)**2,1.0)
    mn,mx=sol.min(),sol.max(); return (sol-mn)/(mx-mn+1e-9)

def fdm_soliton_profile(m_fdm=1.0,n=300):
    r=np.linspace(0,3,n); k=np.pi/max(1.0/m_fdm,0.1); kr=k*r
    return r,np.where(kr>1e-6,(np.sin(kr)/kr)**2,1.0)

def pdp_spectral_duality(image,omega=0.20,fringe=45.0,mixing_angle=0.1,dark_photon_mass=1e-9):
    rows,cols=image.shape; fft_s=fftshift(fft2(image))
    x=np.linspace(-1,1,cols); y=np.linspace(-1,1,rows)
    X,Y=np.meshgrid(x,y); R=np.sqrt(X**2+Y**2)
    L=100.0/max(dark_photon_mass*1e9,1e-6)
    osc=np.sin(2*np.pi*R*L/max(fringe,1.0))
    dmm=(mixing_angle*np.exp(-omega*R**2)*np.abs(osc)*(1-np.exp(-R**2/max(fringe/30,0.1))))
    omm=np.exp(-R**2/max(fringe/30,0.1))-dmm
    return (np.abs(ifft2(fftshift(fft_s*omm))),np.abs(ifft2(fftshift(fft_s*dmm))))

def entanglement_residuals(image,ordinary,dark,strength=0.3,mixing_angle=0.1,fringe=45.0):
    eps=1e-10; tp=np.sum(image**2)+eps
    rho=np.maximum(ordinary**2/tp,eps); S=-rho*np.log(rho)
    xt=(np.abs(ordinary+dark)**2-ordinary**2-dark**2)/tp
    res=S*strength+np.abs(xt)*mixing_angle
    ks=max(3,int(fringe/10)); ks+=ks%2==0
    k=np.outer(np.hanning(ks),np.hanning(ks))
    return convolve(res,k/k.sum(),mode="constant")

def pdp_entanglement_overlay(image,interference,soliton,omega):
    m=omega*0.6
    return np.clip(image*(1-m*0.4)+interference*m*0.5+soliton*m*0.4,0,1)

def generate_interference_pattern(size,fringe,omega):
    y,x=np.ogrid[:size,:size]; cx,cy=size//2,size//2
    r=np.sqrt((x-cx)**2+(y-cy)**2)/size*4; theta=np.arctan2(y-cy,x-cx)
    k=fringe/15.0
    pat=(np.sin(k*4*np.pi*r)*0.5+np.sin(k*2*np.pi*(r+theta/(2*np.pi)))*0.5)
    pat=pat*(1+omega*0.6*np.sin(k*4*np.pi*r)); pat=np.tanh(pat*2)
    return (pat-pat.min())/(pat.max()-pat.min()+1e-9)

def dark_photon_detection_prob(dark_mode,residuals,strength=0.3):
    de=dark_mode/(dark_mode.mean()+0.1)
    lm=uniform_filter(residuals,size=5); re=lm/(lm.mean()+0.1)
    pr=strength; lh=de*re
    return np.clip(gaussian_filter(pr*lh/(pr*lh+(1-pr)+1e-10),sigma=1.0),0,1)

def blue_halo_fusion(image,dark_mode,residuals):
    def pn(a): mn,mx=a.min(),a.max(); return np.sqrt((a-mn)/(mx-mn+1e-10))
    rn,dn,en=pn(image),pn(dark_mode),pn(residuals)
    k=np.ones((5,5))/25; lm=convolve(en,k,mode="constant")
    enh=np.clip(en*(1+2*np.abs(en-lm)),0,1)
    rgb=np.stack([rn,enh,np.clip(gaussian_filter(dn,2.0)+0.3*dn,0,1)],axis=-1)
    return np.clip(rgb**0.45,0,1)

def magnetar_physics(size,B0=1e15,mixing_angle=0.1):
    B_CRIT=4.414e13; alpha=1/137.0
    y,x=np.ogrid[:size,:size]; cx,cy=size//2,size//2
    dx=(x-cx)/(size/4); dy=(y-cy)/(size/4)
    r=np.sqrt(dx**2+dy**2)+0.1; theta=np.arctan2(dy,dx)
    B=(B0/r**3)*np.sqrt(3*np.cos(theta)**2+1)
    Bn=np.clip(B/B.max(),0,1)
    qed=(alpha/(45*np.pi))*(B/B_CRIT)**2; qn=np.clip(qed/(qed.max()+1e-30),0,1)
    conv=(mixing_angle**2)*(1-np.exp(-(B/B_CRIT)**2)); cn=np.clip(conv/(conv.max()+1e-30),0,1)
    return Bn,qn,cn

def qcis_power_spectrum(f_nl=1.0,n_q=0.5,n_s=0.965):
    k=np.logspace(-3,1,300); k0=0.05; q=k/0.2
    T=(np.log(1+2.34*q)/(2.34*q)*(1+3.89*q+(16.2*q)**2+(5.47*q)**3+(6.71*q)**4)**(-0.25))
    Pl=k**n_s*T**2; Pq=Pl*(1+f_nl*(k/k0)**n_q)
    norm=Pl[np.argmin(np.abs(k-k0))]+1e-30
    return k,Pl/norm,Pq/norm

# ===========================================================================
#  PRESETS
# ===========================================================================

def preset_sgr1806(size=400):
    rng=np.random.RandomState(2); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]; dx=(x-cx)/(size/4); dy=(y-cy)/(size/4)
    r=np.sqrt(dx**2+dy**2)+0.05; theta=np.arctan2(dy,dx)
    halo=np.exp(-r*1.5)*np.sqrt(3*np.cos(theta)**2+1)/r
    halo=np.clip(halo/halo.max(),0,1)*0.5
    rc=np.sqrt((x-cx)**2+(y-cy)**2)
    img=halo+np.exp(-rc**2/3.0)+rng.randn(size,size)*0.01
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_crab(size=400):
    rng=np.random.RandomState(1); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]
    dx=(x-cx)/(size*0.22); dy=(y-cy)/(size*0.14); r_ell=np.sqrt(dx**2+dy**2)
    neb=np.exp(-r_ell**2/0.8)*0.7+np.exp(-np.abs(r_ell-0.45)**2/0.015)*0.4
    rc=np.sqrt((x-cx)**2+(y-cy)**2)
    neb+=np.exp(-rc**2/4.0)*0.9+rng.randn(size,size)*0.015
    return np.clip((neb-neb.min())/(neb.max()-neb.min()),0,1)

def preset_galaxy_cluster(size=400):
    rng=np.random.RandomState(4); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]
    dx=(x-cx)/(size*0.15); dy=(y-cy)/(size*0.10); r=np.sqrt(dx**2+dy**2)
    img=np.exp(-7.669*((r/1.0)**0.25-1))
    for ox,oy,rad,amp in [(-0.5,0.3,0.12,0.3),(0.4,-0.4,0.09,0.2),
                           (-0.3,-0.5,0.07,0.15),(0.6,0.2,0.06,0.12)]:
        rs=np.sqrt(((x-cx)/size*2-ox)**2+((y-cy)/size*2-oy)**2)
        img+=amp*np.exp(-rs**2/rad**2)
    img+=rng.randn(size,size)*0.01
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_bullet(size=400):
    rng=np.random.RandomState(7); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]
    r1=np.sqrt(((x-cx-60)/80)**2+((y-cy)/90)**2)
    r2=np.sqrt(((x-cx+80)/50)**2+((y-cy+10)/55)**2)
    theta=np.arctan2(y-cy,x-cx-60); r_arc=np.sqrt((x-cx+20)**2+(y-cy)**2)
    shock=np.exp(-((r_arc-size*0.28)/12)**2)*np.clip(np.cos(theta),0,1)*0.5
    img=np.exp(-r1**2*1.5)+np.exp(-r2**2*2.0)*0.7+shock+rng.randn(size,size)*0.012
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_radar_ppi(size=400):
    rng=np.random.RandomState(10); cx,cy=size//2,size//2
    y,x=np.mgrid[:size,:size]; r=np.sqrt((x-cx)**2+(y-cy)**2)
    img=np.zeros((size,size))
    for rk,amp in [(80,0.9),(140,0.6),(200,0.4),(260,0.25)]:
        img+=amp*np.exp(-((r-rk/400*size/2)**2)/60)
    for ang,rk,amp in [(0.3,100,0.8),(1.1,160,0.6),(-0.8,200,0.7),(2.5,140,0.5)]:
        tx=cx+rk/400*size/2*np.cos(ang); ty=cy+rk/400*size/2*np.sin(ang)
        img+=amp*np.exp(-((x-tx)**2+(y-ty)**2)/25)
    img+=rng.randn(size,size)*0.05
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_radar_sector(size=400):
    rng=np.random.RandomState(11); cx,cy=size-80,size//2
    y,x=np.mgrid[:size,:size]; r=np.sqrt((x-cx)**2+(y-cy)**2)
    theta=np.arctan2(y-cy,x-cx); mask=(theta>-0.52)&(theta<0.52)
    img=np.zeros((size,size))
    for rk,amp in [(100,0.7),(200,0.5),(300,0.3)]:
        img+=amp*np.exp(-((r-rk/400*size)**2)/80)*mask
    for ang,rk,amp in [(0.1,120,1.0),(-0.2,200,0.8),(0.3,280,0.6)]:
        tx=cx+rk/400*size*np.cos(ang); ty=cy+rk/400*size*np.sin(ang)
        img+=amp*np.exp(-((x-tx)**2+(y-ty)**2)/18)
    img+=rng.randn(size,size)*0.04
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def preset_radar_sar(size=400):
    rng=np.random.RandomState(12); img=np.zeros((size,size))
    for freq in [0.02,0.05,0.1,0.2]:
        img+=rng.randn(size,size)*0.3/freq*0.01
    img=gaussian_filter(img,sigma=3)
    img[size//3:size//3+4,:]=0.8; img[2*size//3:2*size//3+4,:]=0.6
    img[:,size//4:size//4+4]=0.7
    for bx,by,bw,bh,amp in [(80,80,30,30,1.0),(200,150,25,20,0.9),
                              (320,100,20,35,0.95),(100,300,40,15,0.85),(280,280,20,20,0.9)]:
        img[by:by+bh,bx:bx+bw]+=amp
    img=gaussian_filter(img,sigma=0.5)+rng.randn(size,size)*0.03
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

PRESETS = {
    "🌌 SGR 1806-20 (Magnetar)":       ("sgr",     preset_sgr1806,        "Magnetar",       0.70,65,"2.5 kpc"),
    "🦀 Crab Nebula M1":                ("crab",    preset_crab,           "Pulsar nebula",  0.60,50,"1.0 kpc"),
    "🌐 Galaxy Cluster (Abell-type)":   ("abell",   preset_galaxy_cluster, "Grav lens",      0.70,65,"50 kpc"),
    "💥 Bullet Cluster 1E0657":         ("bullet",  preset_bullet,         "Merging cluster",0.65,55,"80 kpc"),
    "📡 Radar PPI Scan (Historical)":   ("ppi",     preset_radar_ppi,      "PPI sweep",      0.50,40,"N/A"),
    "📡 Radar Sector Scan (Historical)":("sector",  preset_radar_sector,   "Sector scan",    0.50,40,"N/A"),
    "🛰️ SAR Ground Mapping":            ("sar",     preset_radar_sar,      "SAR terrain",    0.55,45,"N/A"),
}

# ===========================================================================
#  ANNOTATED COMPOSITE — matches reference image
# ===========================================================================

def _font(sz):
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","arial.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]:
        try: return ImageFont.truetype(path,sz)
        except: pass
    return ImageFont.load_default()

def build_annotated_composite(before_gray,after_rgb,omega,fringe,
                               mixing,entropy,r_fdm,source_label,scale_label):
    H,W=before_gray.shape
    bef=Image.fromarray(np.clip(before_gray*255,0,255).astype(np.uint8)).convert("RGB")
    aft=Image.fromarray(np.clip(after_rgb*255,0,255).astype(np.uint8))
    gap=10; bar=40
    comp=Image.new("RGB",(W*2+gap,H+bar),(5,5,15))
    comp.paste(bef,(0,0)); comp.paste(aft,(W+gap,0))
    draw=ImageDraw.Draw(comp)
    fb,fs,ft=_font(14),_font(12),_font(11)

    def annotate(ox,title_main,title_sub):
        lines=[f"Ω = {omega:.2f}  |  Fringe = {fringe}",
               f"Mixing = {mixing:.3f}  |  Entropy = {entropy:.3f}",
               f"ρ_FDM = {r_fdm}"]
        cols=["#00ffcc","#44ddff","#55eeaa"]
        for i,(ln,col) in enumerate(zip(lines,cols)):
            draw.text((ox+8,6+i*17),ln,fill=col,font=fs)
        bw,bh=220,48; bx=ox+W-bw-8
        draw.rectangle([bx,4,bx+bw,4+bh],fill=(0,0,0),outline=(200,200,200),width=1)
        draw.text((bx+7,8),title_main,fill="white",font=ft)
        draw.text((bx+7,24),title_sub,fill="#aaccff",font=ft)
        ax2,ay2=ox+W-22,13
        draw.line([(ax2,ay2+20),(ax2,ay2)],fill="white",width=2)
        draw.polygon([(ax2,ay2),(ax2-4,ay2+8),(ax2+4,ay2+8)],fill="white")
        draw.text((ax2-3,ay2+21),"N",fill="white",font=_font(10))
        bar_px=80; by=H-28
        draw.line([(ox+18,by),(ox+18+bar_px,by)],fill="white",width=3)
        draw.line([(ox+18,by-4),(ox+18,by+4)],fill="white",width=2)
        draw.line([(ox+18+bar_px,by-4),(ox+18+bar_px,by+4)],fill="white",width=2)
        draw.text((ox+22,by+4),scale_label,fill="white",font=fs)

    annotate(0,"Before: Standard View",f"({source_label})")
    annotate(W+gap,"After: Photon-Dark-Photon Entangled","FDM Overlays (Tony Ford Model)")
    draw.rectangle([0,H,W*2+gap,H+bar],fill=(10,10,25))
    draw.text((10,H+12),"QCAUS v1.0  |  Tony E. Ford  |  tlcagford@gmail.com  |  Patent Pending  |  2026",
              fill="#445577",font=ft)
    return comp

# ===========================================================================
#  VISUAL OVERLAY — green FDM rings, orange speckles, blue halo
# ===========================================================================

def build_after_rgb(img_gray,soliton,interf,dark_mode,ent_res):
    H,W=img_gray.shape; out=np.zeros((H,W,3),dtype=np.float32)
    out[...,0]=img_gray*0.5; out[...,1]=img_gray*0.2; out[...,2]=img_gray*0.15
    fdm_g=soliton*interf
    fdm_n=(fdm_g-fdm_g.min())/(fdm_g.max()-fdm_g.min()+1e-9)
    rings=np.clip(fdm_n*2.5,0,1)
    out[...,1]+=rings*0.85
    ent_n=(ent_res-ent_res.min())/(ent_res.max()-ent_res.min()+1e-9)
    sp=gaussian_filter(ent_n,sigma=1.5)*(1-rings*0.7)
    out[...,0]+=sp*0.8; out[...,1]+=sp*0.3
    dm_n=(dark_mode-dark_mode.min())/(dark_mode.max()-dark_mode.min()+1e-9)
    dm_b=gaussian_filter(dm_n,sigma=4)
    out[...,2]+=dm_b*0.9; out[...,1]+=dm_b*0.2
    bright=img_gray>0.85
    out[bright,0]=np.clip(out[bright,0]+0.8,0,1)
    out[bright,1]=np.clip(out[bright,1]+0.6,0,1)
    out[bright,2]=np.clip(out[bright,2]+0.3,0,1)
    return np.clip(out,0,1)

# ===========================================================================
#  UTILITIES
# ===========================================================================

def load_and_square(file,mx=400):
    img=Image.open(file).convert("L")
    if max(img.size)>mx: img.thumbnail((mx,mx),Image.LANCZOS)
    w,h=img.size; s=min(w,h)
    img=img.crop(((w-s)//2,(h-s)//2,(w+s)//2,(h+s)//2))
    return np.array(img,dtype=np.float32)/255.0

def _cmap(arr,name):
    return (mcm.get_cmap(name)(np.clip(arr,0,1))[...,:3]*255).astype(np.uint8)

def to_pil(arr,cmap=None):
    if arr.ndim==2:
        if cmap: return Image.fromarray(_cmap(arr,cmap),"RGB")
        return Image.fromarray(np.clip(arr*255,0,255).astype(np.uint8),"L")
    return Image.fromarray(np.clip(arr*255,0,255).astype(np.uint8),"RGB")

def b64png(pil_img):
    buf=io.BytesIO(); pil_img.save(buf,format="PNG"); return base64.b64encode(buf.getvalue()).decode()

def dl(arr,fname,label="📥 Download",cmap=None,cls="dl-btn"):
    b=b64png(to_pil(arr,cmap))
    return f'<a href="data:image/png;base64,{b}" download="{fname}" class="{cls}">{label}</a>'

def make_zip(files):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as zf:
        for fname,obj in files.items():
            if isinstance(obj,np.ndarray): obj=to_pil(obj)
            if isinstance(obj,Image.Image):
                ib=io.BytesIO(); obj.save(ib,format="PNG"); ib.seek(0); zf.writestr(fname,ib.getvalue())
            elif isinstance(obj,bytes): zf.writestr(fname,obj)
    buf.seek(0); return buf.getvalue()

def fig_bytes(fig):
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); buf.seek(0); return buf.getvalue()

# ===========================================================================
#  SIDEBAR
# ===========================================================================
with st.sidebar:
    st.markdown("## ⚛️ Core Physics")
    omega_pd    =st.slider("Omega_PD Entanglement",0.05,0.70,0.20,0.01)
    fringe_scale=st.slider("Fringe Scale (pixels)",10,80,65,1)
    kin_mix     =st.slider("Kinetic Mixing eps",1e-12,1e-8,1e-10,format="%.1e")
    fdm_mass    =st.slider("FDM Mass x10^-22 eV",0.10,10.00,1.00,0.01)
    st.markdown("---")
    st.markdown("## 🌟 Magnetar")
    b0_log10   =st.slider("B0 log10 G",13.0,16.0,15.0,0.1)
    magnetar_eps=st.slider("Magnetar eps",0.01,0.50,0.10,0.01)
    st.markdown("---")
    st.markdown("## 📈 QCIS")
    f_nl=st.slider("f_NL",0.00,5.00,1.00,0.01)
    n_q =st.slider("n_q",0.00,2.00,0.50,0.01)
    st.markdown("---")
    st.markdown("**Tony Ford | tlcagford@gmail.com**\n\n**Patent Pending | 2026**")

# ===========================================================================
#  MAIN UI
# ===========================================================================
st.markdown('<h1 style="text-align:center;color:#7eb8ff">🔭 QCAUS v1.0</h1>',unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#8899bb">FDM · PDP · Magnetar · QCIS · EM Spectrum · Historical Radar</p>',unsafe_allow_html=True)

st.markdown("### Preset Data — click any to run instantly")
cols=st.columns(len(PRESETS))
chosen=None
for col,(label,meta) in zip(cols,PRESETS.items()):
    with col:
        if st.button(label,use_container_width=True): chosen=label

st.markdown("### — OR upload your own —")
uploaded=st.file_uploader("Drag & drop FITS / JPG / PNG",
                           type=["jpg","jpeg","png","fits"],label_visibility="collapsed")

img_data=None; source_name="Public HST/JWST Data"; scale_label="20 kpc"

if uploaded is not None:
    img_data=load_and_square(uploaded); source_name=uploaded.name
    st.success(f"✅ Loaded: {source_name}")
elif chosen and chosen in PRESETS:
    key,fn,desc,d_om,d_fr,d_sc=PRESETS[chosen]
    img_data=fn(); source_name=f"{chosen.split('(')[0].strip()} — {desc}"
    scale_label=d_sc; st.info(f"📁 {chosen}")
else:
    st.markdown("""
### 🔭 QCAUS v1.0 — Verified Physics Formulas

| Module | Formula | Source |
|--------|---------|--------|
| **FDM Soliton** | ρ(r)=ρ₀[sin(kr)/(kr)]²  k=π/r_s | QCAUS/app.py |
| **PDP Spectral Duality** | FFT dark_mask  osc_len=100/(m·1e9) | pdp_radar_core.py |
| **Entanglement Residuals** | S=−ρ·log(ρ)+cross-term | pdp_radar_core.py |
| **Dark Photon Detection** | Bayesian P_dark=prior·L/(prior·L+(1-prior)) | pdp_radar_core.py |
| **Blue-Halo Fusion** | R=orig G=residuals B=dark γ=0.45 | pdp_radar_core.py |
| **Magnetar Dipole** | B=B₀(R/r)³√(3cos²θ+1) B_crit=4.414×10¹³G | Magnetar repo |
| **Euler-Heisenberg QED** | ΔL=(α/45π)(B/B_crit)² α=1/137 | Magnetar repo |
| **Dark Photon Conversion** | P_conv=ε²(1−exp(−(B/B_crit)²)) | Magnetar repo |
| **QCIS Power Spectrum** | P(k)=P_ΛCDM(k)×(1+f_NL(k/k₀)^n_q) BBKS n_s=0.965 | QCIS repo |
""")

# ===========================================================================
#  PROCESSING
# ===========================================================================
if img_data is not None:
    B0=10**b0_log10; B_CRIT=4.414e13
    if img_data.ndim==3: ig=np.mean(img_data,axis=-1).astype(np.float32)
    else: ig=img_data.astype(np.float32)
    h,w=ig.shape; SIZE=min(h,w)
    if h!=w:
        p=Image.fromarray((ig*255).astype(np.uint8))
        ig=np.array(p.resize((SIZE,SIZE),Image.LANCZOS),dtype=np.float32)/255.0

    sol  =fdm_soliton_2d(SIZE,fdm_mass)
    intr =generate_interference_pattern(SIZE,fringe_scale,omega_pd)
    orm,dm=pdp_spectral_duality(ig,omega_pd,fringe_scale,kin_mix*1e9,1e-9)
    eres =entanglement_residuals(ig,orm,dm,omega_pd*0.3,kin_mix*1e9,fringe_scale)
    pdpo =pdp_entanglement_overlay(ig,intr,sol,omega_pd)
    fus  =blue_halo_fusion(ig,dm,eres)
    dpp  =dark_photon_detection_prob(dm,eres,omega_pd*0.3)
    dp_pk=float(dpp.max()*100)
    Bn,qn,cn=magnetar_physics(SIZE,B0,magnetar_eps)
    k_a,Pl,Pq=qcis_power_spectrum(f_nl,n_q)
    ra,rha=fdm_soliton_profile(fdm_mass)

    mix_v =float(omega_pd*0.6)
    ent_v =float(-np.mean(eres[eres>0]*np.log(eres[eres>0]+1e-10))) if eres.max()>0 else 0.0
    rfdm_s=f"{1/fdm_mass:.1f} kpc"

    after_rgb=build_after_rgb(ig,sol,intr,dm,eres)
    comp=build_annotated_composite(ig,after_rgb,omega_pd,fringe_scale,
                                   mix_v,ent_v,rfdm_s,source_name,scale_label)

    # HERO
    st.markdown("---")
    st.markdown("## 🖼️ Annotated Before vs After")
    st.image(comp,use_container_width=True)

    # Build all plot bytes
    def make_mag_plot():
        Bc=4.414e13; al=1/137.0; rm=10; gs=100
        xg=np.linspace(-rm,rm,gs); yg=np.linspace(-rm,rm,gs)
        Xg,Yg=np.meshgrid(xg,yg); Rg=np.maximum(np.sqrt(Xg**2+Yg**2),0.2); thg=np.arctan2(Yg,Xg)
        Br2=B0*(1/Rg)**3*2*np.cos(thg); Bt2=B0*(1/Rg)**3*np.sin(thg)
        Bx2=Br2*np.cos(thg)-Bt2*np.sin(thg); By2=Br2*np.sin(thg)+Bt2*np.cos(thg)
        Bt=np.sqrt(Bx2**2+By2**2)
        EHg=(al/(45*np.pi))*(Bt/Bc)**2
        dpc=(magnetar_eps**2)*(1-np.exp(-(Bt/Bc)**2))
        fig2,axs=plt.subplots(2,2,figsize=(12,10),facecolor="#0d0f1a")
        for ax in axs.flat: ax.set_facecolor("#111320"); ax.tick_params(colors="white"); ax.grid(True,alpha=0.2)
        axs[0,0].streamplot(Xg,Yg,Bx2,By2,color=np.log10(Bt+1e-10),cmap="plasma",density=1.2)
        axs[0,0].add_patch(Circle((0,0),1,color="white",zorder=5))
        axs[0,0].set_title(f"B=B0(R/r)^3 sqrt(3cos2th+1)  B0={B0:.2e}G",color="white",fontsize=10)
        im2=axs[0,1].imshow(EHg/(EHg.max()+1e-30),extent=[-rm,rm,-rm,rm],origin="lower",cmap="inferno")
        axs[0,1].set_title("Euler-Heisenberg  dL=(a/45pi)(B/Bc)^2  a=1/137",color="white",fontsize=10)
        plt.colorbar(im2,ax=axs[0,1])
        im3=axs[1,0].imshow(dpc/(dpc.max()+1e-30),extent=[-rm,rm,-rm,rm],origin="lower",cmap="hot")
        axs[1,0].set_title(f"P_conv=e^2*(1-exp(-(B/Bc)^2))  e={magnetar_eps:.3f}",color="white",fontsize=10)
        plt.colorbar(im3,ax=axs[1,0])
        r1=np.linspace(1.1,rm,200); B1=B0*(1/r1)**3*2
        EH1=(al/(45*np.pi))*(B1/Bc)**2; dp1=(magnetar_eps**2)*(1-np.exp(-(B1/Bc)**2))
        axs[1,1].semilogy(r1,B1,"b-",lw=2,label="|B| on-axis")
        axs[1,1].set_ylabel("|B| (G)",color="b"); axs[1,1].tick_params(axis="y",labelcolor="b")
        ax2t=axs[1,1].twinx()
        ax2t.plot(r1,EH1/(EH1.max()+1e-30),"r--",lw=2,label="dL norm.")
        ax2t.plot(r1,dp1/(dp1.max()+1e-30),"g-.",lw=2,label="P_conv norm.")
        ax2t.set_ylim(0,1); ax2t.set_ylabel("Normalised",color="r")
        axs[1,1].set_title("Radial Profiles on-axis",color="white",fontsize=10)
        l1,lb1=axs[1,1].get_legend_handles_labels(); l2,lb2=ax2t.get_legend_handles_labels()
        axs[1,1].legend(l1+l2,lb1+lb2,fontsize=9)
        plt.suptitle(f"Magnetar QED  B0=10^{b0_log10:.1f}G  eps={magnetar_eps:.3f}  Bcrit=4.414e13G",color="white",fontsize=12)
        plt.tight_layout(); b=fig_bytes(fig2); plt.close(fig2); return b

    def make_ps_plot():
        fig3,ax3=plt.subplots(figsize=(10,4),facecolor="#0d0f1a")
        ax3.set_facecolor("#111320"); ax3.tick_params(colors="white")
        ax3.loglog(k_a,Pl,"b-",lw=2,label="ΛCDM baseline")
        ax3.loglog(k_a,Pq,"r--",lw=2,label=f"Quantum f_NL={f_nl:.1f} n_q={n_q:.1f}")
        ax3.axvline(0.05,color="gray",ls=":",alpha=0.5)
        ax3.set_xlabel("k (h/Mpc)",color="white"); ax3.set_ylabel("P(k)/P(k0)",color="white")
        ax3.set_title("QCIS Power Spectrum  BBKS T(k)  n_s=0.965",color="white")
        ax3.legend(labelcolor="white"); ax3.grid(True,alpha=0.3,which="both")
        plt.tight_layout(); b=fig_bytes(fig3); plt.close(fig3); return b

    def make_fdm_plot():
        fig4,ax4=plt.subplots(figsize=(9,3),facecolor="#0d0f1a")
        ax4.set_facecolor("#111320"); ax4.tick_params(colors="white")
        ax4.plot(ra,rha,"r-",lw=2.5,label=f"rho(r)=rho0[sin(kr)/(kr)]^2  m={fdm_mass:.1f}x10^-22 eV")
        ax4.set_xlabel("r (kpc)",color="white"); ax4.set_ylabel("rho(r)/rho0",color="white")
        ax4.set_title("FDM Soliton — Schrödinger-Poisson ground state",color="white")
        ax4.legend(labelcolor="white"); ax4.grid(True,alpha=0.3)
        plt.tight_layout(); b=fig_bytes(fig4); plt.close(fig4); return b

    mag_b=make_mag_plot(); ps_b=make_ps_plot(); fdm_b=make_fdm_plot()

    # ZIP ALL
    st.markdown("---")
    st.markdown("## 📦 Download All Results")
    zfiles={
        "01_annotated_comparison.png": comp,
        "02_original.png":             to_pil(ig,"gray"),
        "03_after_visual_overlay.png": to_pil(after_rgb),
        "04_fdm_soliton.png":          to_pil(sol,"hot"),
        "05_pdp_interference.png":     to_pil(intr,"plasma"),
        "06_entanglement_residuals.png":to_pil(eres,"inferno"),
        "07_pdp_entangled.png":        to_pil(pdpo,"inferno"),
        "08_dark_photon_detection.png":to_pil(dpp,"YlOrRd"),
        "09_blue_halo_fusion.png":     to_pil(fus),
        "10_magnetar_Bfield.png":      to_pil(Bn,"plasma"),
        "11_magnetar_QED.png":         to_pil(qn,"inferno"),
        "12_magnetar_darkconv.png":    to_pil(cn,"hot"),
        "13_magnetar_qed_plot.png":    mag_b,
        "14_qcis_power_spectrum.png":  ps_b,
        "15_fdm_soliton_profile.png":  fdm_b,
    }
    zb=make_zip(zfiles); zb64=base64.b64encode(zb).decode()
    st.markdown(f'<a href="data:application/zip;base64,{zb64}" download="QCAUS_all_results.zip" class="zip-btn">📦 Download ALL {len(zfiles)} Results as ZIP</a>',unsafe_allow_html=True)
    st.markdown(dl(comp,"annotated_comparison.png","📥 Download Annotated Composite"),unsafe_allow_html=True)

    # METRICS
    st.markdown("---")
    m1,m2,m3,m4,m5=st.columns(5)
    m1.metric("P_dark Peak",f"{dp_pk:.1f}%",delta=f"eps={kin_mix:.1e}")
    m2.metric("FDM Soliton Peak",f"{float(sol.max()):.3f}",delta=f"m={fdm_mass:.1f}")
    m3.metric("Fringe Contrast",f"{float(intr.std()):.3f}",delta=f"f={fringe_scale}")
    m4.metric("PDP Mixing Ω·0.6",f"{omega_pd*0.6:.3f}",delta=f"Ω={omega_pd:.2f}")
    m5.metric("B/B_crit",f"{B0/B_CRIT:.2e}",delta=f"10^{b0_log10:.1f}")
    if dp_pk>50: st.error(f"STRONG DARK PHOTON SIGNAL — P_dark={dp_pk:.0f}%")
    elif dp_pk>20: st.warning(f"DARK PHOTON SIGNAL — P_dark={dp_pk:.0f}%")
    else: st.success(f"CLEAR — P_dark={dp_pk:.0f}%")

    # INDIVIDUAL PANELS
    st.markdown("---")
    st.markdown("## 📊 Individual Physics Maps")
    st.markdown("### FDM · PDP · Residuals")
    c1,c2,c3=st.columns(3)
    for col,(arr,cmap,title,fname) in zip([c1,c2,c3],[
        (sol,"hot","⚛️ FDM Soliton  ρ(r)=ρ₀[sin(kr)/(kr)]²","fdm_soliton.png"),
        (intr,"plasma","🌊 PDP Interference  osc_len=100/(m·1e9)","pdp_interference.png"),
        (eres,"inferno","🕳️ Entanglement Residuals  S=−ρlogρ+xt","ent_residuals.png"),
    ]):
        with col:
            st.markdown(f"**{title}**"); st.image(to_pil(arr,cmap),use_container_width=True)
            st.markdown(dl(arr,fname,cmap=cmap),unsafe_allow_html=True)

    st.markdown("### Dark Photon · Blue-Halo · Visual Overlay")
    c1,c2,c3=st.columns(3)
    for col,(arr,cmap,title,fname) in zip([c1,c2,c3],[
        (dpp,"YlOrRd","🔵 Dark Photon Detection  Bayesian P_dark","dp_detection.png"),
        (fus,None,"💙 Blue-Halo Fusion  R=orig G=res B=dark γ=0.45","blue_halo.png"),
        (after_rgb,None,"🎨 Visual Overlay (FDM rings + PDP halo)","after_overlay.png"),
    ]):
        with col:
            st.markdown(f"**{title}**"); st.image(to_pil(arr,cmap),use_container_width=True)
            st.markdown(dl(arr,fname,cmap=cmap),unsafe_allow_html=True)

    st.markdown("### Magnetar QED Maps")
    cA,cB,cC=st.columns(3)
    for col,(arr,cmap,title,fname) in zip([cA,cB,cC],[
        (Bn,"plasma","B=B₀(R/r)³√(3cos²θ+1)","magnetar_B.png"),
        (qn,"inferno","Euler-Heisenberg ΔL=(α/45π)(B/Bc)²","magnetar_QED.png"),
        (cn,"hot","P_conv=ε²(1−e^{−(B/Bc)²})","magnetar_darkconv.png"),
    ]):
        with col:
            st.markdown(f"**{title}**"); st.image(to_pil(arr,cmap),use_container_width=True)
            st.markdown(dl(arr,fname,cmap=cmap),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## ⚡ Magnetar QED — 4-Panel")
    st.image(mag_b,use_container_width=True)
    mb64=base64.b64encode(mag_b).decode()
    st.markdown(f'<a href="data:image/png;base64,{mb64}" download="magnetar_qed.png" class="dl-btn">📥 Download Magnetar Plot</a>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## ⚛️ FDM Soliton Radial Profile")
    st.image(fdm_b,use_container_width=True)
    fb64=base64.b64encode(fdm_b).decode()
    st.markdown(f'<a href="data:image/png;base64,{fb64}" download="fdm_profile.png" class="dl-btn">📥 Download FDM Profile</a>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📈 QCIS Power Spectrum")
    st.image(ps_b,use_container_width=True)
    pb64=base64.b64encode(ps_b).decode()
    st.markdown(f'<a href="data:image/png;base64,{pb64}" download="qcis_spectrum.png" class="dl-btn">📥 Download QCIS Spectrum</a>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🌈 EM Spectrum Mapping")
    k2,Pl2,Pq2=qcis_power_spectrum(f_nl,n_q)
    qf=np.clip(float(Pq2[np.argmin(np.abs(k2-0.1))]/(Pl2[np.argmin(np.abs(k2-0.1))]+1e-30)),0.5,3.0)
    ir2=np.clip(ig**0.5*qf,0,1); vi2=np.clip(ig**0.8*qf,0,1); xr2=np.clip(ig**1.5*qf,0,1)
    em2=np.stack([ir2,vi2,xr2],axis=-1)
    ce1,ce2=st.columns(2)
    with ce1:
        st.markdown("**🎨 EM Composite**"); st.image(to_pil(em2),use_container_width=True)
        st.markdown(dl(em2,"em_composite.png"),unsafe_allow_html=True)
    with ce2:
        st.markdown("**📊 EM Bands**")
        t1,t2,t3=st.tabs(["🔴 Infrared","🟢 Visible","🔵 X-ray"])
        with t1:
            st.image(_cmap(ir2,"hot"),use_container_width=True)
            st.markdown("*λ~10-1000 μm*")
            st.markdown(dl(ir2,"infrared.png",cmap="hot"),unsafe_allow_html=True)
        with t2:
            st.image(_cmap(vi2,"viridis"),use_container_width=True)
            st.markdown("*λ~400-700 nm*")
            st.markdown(dl(vi2,"visible.png",cmap="viridis"),unsafe_allow_html=True)
        with t3:
            st.image(_cmap(xr2,"plasma"),use_container_width=True)
            st.markdown("*λ~0.01-10 nm*")
            st.markdown(dl(xr2,"xray.png",cmap="plasma"),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📡 Verified Physics Formulas")
    st.markdown("""
| Module | Formula | Source |
|--------|---------|--------|
| **FDM Soliton** | ρ(r)=ρ₀[sin(kr)/(kr)]²  k=π/r_s | QCAUS/app.py |
| **PDP Spectral Duality** | FFT dark_mask=ε·exp(-ΩR²)·abs(sin(2πRL/f))·(1-exp(-R²/f)) | pdp_radar_core.py |
| **Entanglement Residuals** | S=-ρ·log(ρ)+abs(ψ_ord+ψ_dark)²-ψ_ord²-ψ_dark² | pdp_radar_core.py |
| **Dark Photon Detection** | P_dark=prior·L/(prior·L+(1-prior)) Bayesian | pdp_radar_core.py |
| **Blue-Halo Fusion** | R=original G=residuals B=dark γ=0.45 | pdp_radar_core.py |
| **Magnetar Dipole** | B=B₀(R/r)³√(3cos²θ+1) B_crit=4.414×10¹³G | Magnetar repo |
| **Euler-Heisenberg QED** | ΔL=(α/45π)(B/B_crit)² α=1/137 | Magnetar repo |
| **Dark Photon Conversion** | P_conv=ε²(1−exp(−(B/B_crit)²)) | Magnetar repo |
| **QCIS Power Spectrum** | P(k)=P_ΛCDM(k)×(1+f_NL(k/k₀)^n_q) BBKS n_s=0.965 | QCIS repo |
""")

st.markdown("---")
st.markdown('<p style="color:#445577;text-align:center">🔭 QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite | Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026</p>',unsafe_allow_html=True)
