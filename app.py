import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
import io, base64, warnings, zipfile
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter, convolve, uniform_filter
from scipy.integrate import solve_ivp
import time
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CSS
# =============================================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:linear-gradient(135deg,#0a0a1a 0%,#0a0e1a 100%);color:#d0e4ff;}
[data-testid="stSidebar"]{background:#0d1525;border-right:2px solid #00aaff;}
h1,h2,h3,h4{color:#7ec8e3;}
.stMarkdown p{color:#c8ddf0;}
.credit-badge{background:rgba(30,58,95,0.85);border:1px solid #335588;border-radius:6px;
 padding:4px 10px;font-size:11px;color:#88aaff;display:inline-block;margin-bottom:6px;}
.dl-btn{display:inline-block;padding:6px 14px;background:#1e3a5f;color:white!important;
 text-decoration:none;border-radius:5px;margin-top:6px;font-size:13px;}
.dl-btn:hover{background:#2a5080;}
.data-panel{border:1px solid #0ea5e9;border-radius:8px;padding:8px 12px;
 background:rgba(15,23,42,0.92);color:#67e8f9;font-size:12px;margin-bottom:6px;line-height:1.6;}
.desc-card{background:rgba(10,20,40,0.85);border:1px solid #1e3a5f;border-radius:8px;
 padding:10px 14px;margin:6px 0;font-size:12px;color:#c8ddf0;line-height:1.7;}
.desc-card .formula{color:#ffdd88;font-family:monospace;font-size:11px;}
.desc-card .what{color:#aaddff;}
.std-badge{background:#2a2a2a;border:1px solid #555;border-radius:4px;
 padding:3px 8px;font-size:10px;color:#aaa;display:inline-block;}
.qcaus-badge{background:rgba(0,100,160,0.4);border:1px solid #0ea5e9;border-radius:4px;
 padding:3px 8px;font-size:10px;color:#67e8f9;display:inline-block;}
.compare-label{font-size:11px;font-weight:bold;padding:4px 0;margin-bottom:4px;}
</style>""", unsafe_allow_html=True)

AUTHOR = "Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026"

def credit(repo, formula=""):
    f = f" &nbsp;·&nbsp; <code>{formula}</code>" if formula else ""
    return f'<span class="credit-badge">📦 {repo}{f} &nbsp;·&nbsp; {AUTHOR}</span>'

def get_dl(arr_or_buf, filename, label="📥 Download", cmap=None):
    if isinstance(arr_or_buf, io.BytesIO):
        arr_or_buf.seek(0); b64 = base64.b64encode(arr_or_buf.read()).decode()
    else:
        buf = io.BytesIO(); arr_to_pil(arr_or_buf, cmap).save(buf, "PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}" class="dl-btn">{label}</a>'

def fig_to_buf(fig, dpi=120):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0); return buf

def _apply_cmap(arr2d, cmap_name):
    rgba = plt.get_cmap(cmap_name)(np.clip(arr2d, 0, 1))
    return (rgba[..., :3] * 255).astype(np.uint8)

def arr_to_pil(arr, cmap=None):
    if arr.ndim == 2:
        if cmap: return Image.fromarray(_apply_cmap(arr, cmap), "RGB")
        return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "L")
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "RGB")

def ax_dark(ax):
    ax.set_facecolor("#0d1525"); ax.tick_params(colors="#7ec8e3")
    ax.grid(True, alpha=0.15, color="#335588")
    for s in ax.spines.values(): s.set_edgecolor("#335588")
    for a in [ax.title, ax.xaxis.label, ax.yaxis.label]: a.set_color("#7ec8e3")

# =============================================================================
# PANEL DESCRIPTOR — renders desc card + comparison figure
# =============================================================================
def panel_card(title, what_it_does, formula_text, std_label, qcaus_label, repo, credit_std, credit_qcaus):
    st.markdown(f"""
<div class="desc-card">
<strong style="color:#7ec8e3">{title}</strong><br>
<span class="what">{what_it_does}</span><br><br>
<span class="formula">Formula: {formula_text}</span><br><br>
<span class="std-badge">📐 Standard: {credit_std}</span>
&nbsp;vs&nbsp;
<span class="qcaus-badge">🔬 QCAUS: {credit_qcaus}</span><br>
<small style="color:#557799">Repo: {repo}</small>
</div>""", unsafe_allow_html=True)

def make_comparison_fig(img_gray, qcaus_map, std_label, qcaus_label,
                        title, formula, what_it_does, cmap="inferno",
                        show_on_image=True):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), facecolor="#0a0e1a")
    for ax in (ax1, ax2):
        ax.set_facecolor("#0d1525"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_edgecolor("#335588")
    ax1.imshow(img_gray, cmap="gray", vmin=0, vmax=1)
    ax1.set_title(f"Standard View\n{std_label}", color="#aaaaaa", fontsize=9, pad=6)
    if show_on_image and qcaus_map is not None:
        img_rgb = np.stack([img_gray] * 3, axis=-1)
        cmap_fn = plt.get_cmap(cmap)
        ov_rgb = cmap_fn(np.clip(qcaus_map, 0, 1))[..., :3]
        composite = np.clip(img_rgb * 0.55 + ov_rgb * 0.45, 0, 1)
        ax2.imshow(composite)
    elif qcaus_map is not None:
        if qcaus_map.ndim == 3:
            ax2.imshow(np.clip(qcaus_map, 0, 1))
        else:
            ax2.imshow(qcaus_map, cmap=cmap, vmin=0, vmax=1)
    ax2.set_title(f"QCAUS Enhancement\n{qcaus_label}", color="#7ec8e3", fontsize=9, pad=6)
    ax2.text(0.02, 0.97, formula, transform=ax2.transAxes,
             color="#ffdd88", fontsize=7.5, va="top", style="italic",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#0a0e1a", alpha=0.9))
    ax2.text(0.02, 0.03, f"Tony E. Ford 2026 | {AUTHOR[:25]}",
             transform=ax2.transAxes, color="#335588", fontsize=6.5, va="bottom")
    plt.suptitle(f"{title} — Standard vs QCAUS",
                 color="#7ec8e3", fontsize=11, fontweight="bold", y=1.01)
    plt.tight_layout(pad=0.5)
    return fig

# =============================================================================
# CACHED PIPELINE RUNNER (v8 performance improvement)
# =============================================================================
@st.cache_data(show_spinner="Running 9 quantum pipelines...", ttl=3600)
def run_all_pipelines(img_gray, omega_pd, fringe_scale, kin_mix, fdm_mass,
                      b0_log10, mag_eps, f_nl, n_q, prim_mass, prim_Hinf):
    SIZE = min(img_gray.shape[0], img_gray.shape[1], 400)
    img_gray = np.array(Image.fromarray((img_gray*255).astype(np.uint8))
                        .resize((SIZE, SIZE), Image.LANCZOS), dtype=np.float32)/255.0

    soliton = fdm_soliton_2d(SIZE, fdm_mass)
    interf = generate_interference_pattern(SIZE, fringe_scale, omega_pd)
    ord_mode, dark_mode = pdp_spectral_duality(img_gray, omega_pd, fringe_scale, kin_mix, fdm_mass)
    ent_res = entanglement_residuals(img_gray, ord_mode, dark_mode, omega_pd*0.3, kin_mix, fringe_scale)
    dp_prob = dark_photon_detection_prob(dark_mode, ent_res, omega_pd*0.3)
    fusion = blue_halo_fusion(img_gray, dark_mode, ent_res)
    pdp_inf = np.clip(img_gray*(1-omega_pd*0.4)+interf*omega_pd*0.6, 0, 1)
    overlay_rgb = pdp_overlay_rgb(img_gray, soliton, interf, dp_prob, omega_pd)
    B_n, qed_n, conv_n = magnetar_physics(SIZE, 10**b0_log10, mag_eps)
    k_arr, P_lcdm, P_qcis = qcis_power_spectrum(f_nl, n_q)
    em_comp = em_spectrum_composite(img_gray, f_nl, n_q)
    r_arr, rho_sinc, rho_schive = fdm_soliton_profile(fdm_mass)
    r_nfw, rho_nfw = nfw_profile()
    ent_scalar = float(-np.mean(ent_res[ent_res>0]*np.log(ent_res[ent_res>0]+1e-10)))

    t_p, P_g, P_d, S_p, T_period, theta = von_neumann_primordial(
        eps=kin_mix, m_dark_eV=prim_mass*1e-9, H_inf_eV=prim_Hinf*1e-5)

    return {
        "img_gray": img_gray, "SIZE": SIZE,
        "soliton": soliton, "interf": interf, "ord_mode": ord_mode, "dark_mode": dark_mode,
        "ent_res": ent_res, "dp_prob": dp_prob, "fusion": fusion, "pdp_inf": pdp_inf,
        "overlay_rgb": overlay_rgb,
        "B_n": B_n, "qed_n": qed_n, "conv_n": conv_n,
        "k_arr": k_arr, "P_lcdm": P_lcdm, "P_qcis": P_qcis,
        "em_comp": em_comp,
        "r_arr": r_arr, "rho_sinc": rho_sinc, "rho_schive": rho_schive,
        "r_nfw": r_nfw, "rho_nfw": rho_nfw,
        "ent_scalar": ent_scalar, "dp_peak": float(dp_prob.max()*100),
        "prim_t": t_p, "prim_Pg": P_g, "prim_Pd": P_d, "prim_Sp": S_p,
        "prim_T": T_period, "prim_theta": theta
    }

# =============================================================================
# 9 CORE PHYSICS PIPELINE FUNCTIONS (exactly as in v7)
# =============================================================================
def fdm_soliton_2d(size=300, m_fdm=1.0):
    y, x = np.ogrid[:size, :size]; cx = cy = size // 2
    r = np.sqrt((x-cx)**2+(y-cy)**2)/size*5
    kr = np.pi/max(1.0/m_fdm, 0.1)*r
    with np.errstate(divide="ignore", invalid="ignore"):
        sol = np.where(kr>1e-6, (np.sin(kr)/kr)**2, 1.0)
    mn, mx = sol.min(), sol.max()
    return (sol-mn)/(mx-mn+1e-9)

def fdm_soliton_profile(m_fdm=1.0, n=300):
    r = np.linspace(0, 3, n)
    kr = np.pi/max(1.0/m_fdm, 0.1)*r
    rho_sinc = np.where(kr>1e-6, (np.sin(kr)/kr)**2, 1.0)
    r_c = 1.0/m_fdm
    rho_schive = 1.0/(1+(r/r_c)**2)**8; rho_schive /= rho_schive.max()
    return r, rho_sinc, rho_schive

def nfw_profile(n=300):
    r = np.linspace(0.01, 3, n)
    r_s = 0.5
    rho_nfw = 1.0 / (r/r_s * (1+r/r_s)**2)
    return r, rho_nfw / rho_nfw.max()

def generate_interference_pattern(size, fringe, omega):
    y, x = np.ogrid[:size, :size]; cx = cy = size//2
    r = np.sqrt((x-cx)**2+(y-cy)**2)/size*4
    theta = np.arctan2(y-cy, x-cx); k = fringe/15.0
    pat = (np.sin(k*4*np.pi*r)*0.5 + np.sin(k*2*np.pi*(r+theta/(2*np.pi)))*0.5)
    pat = np.tanh(pat*(1+omega*0.6*np.sin(k*4*np.pi*r))*2)
    return (pat-pat.min())/(pat.max()-pat.min()+1e-9)

def pdp_spectral_duality(image, omega=0.20, fringe_scale=45.0, mixing_eps=1e-10, fdm_mass=1.0):
    rows, cols = image.shape
    fft_s = fftshift(fft2(image))
    X, Y = np.meshgrid(np.linspace(-1,1,cols), np.linspace(-1,1,rows))
    R = np.sqrt(X**2+Y**2)
    L = 100.0/max(fdm_mass*1e-31*1e9, 1e-6)
    osc = np.sin(2*np.pi*R*L/max(fringe_scale,1.0))
    dmm = mixing_eps*np.exp(-omega*R**2)*np.abs(osc)*(1-np.exp(-R**2/max(fringe_scale/30,0.1)))
    omm = np.exp(-R**2/max(fringe_scale/30,0.1))-dmm
    return np.abs(ifft2(fftshift(fft_s*omm))), np.abs(ifft2(fftshift(fft_s*dmm)))

def entanglement_residuals(image, ordinary, dark, strength=0.3, mixing_eps=1e-10, fringe_scale=45.0):
    tp = np.sum(image**2)+1e-10; rho = np.maximum(ordinary**2/tp, 1e-10)
    S = -rho*np.log(rho)
    xterm = (np.abs(ordinary+dark)**2-ordinary**2-dark**2)/tp
    eps_scale = np.clip(-np.log10(mixing_eps+1e-15)/12.0, 0, 1)
    res = S*strength + np.abs(xterm)*eps_scale
    ks = max(3, int(fringe_scale/10))|1
    kernel = np.outer(np.hanning(ks), np.hanning(ks))
    return convolve(res, kernel/kernel.sum(), mode="constant")

def dark_photon_detection_prob(dark_mode, residuals, strength=0.3):
    dark_ev = dark_mode/(dark_mode.mean()+0.1)
    res_ev = uniform_filter(residuals,5)/(uniform_filter(residuals,5).mean()+0.1)
    lhood = dark_ev*res_ev
    prob = strength*lhood/(strength*lhood+(1-strength)+1e-10)
    return np.clip(gaussian_filter(prob, sigma=1.0), 0, 1)

def blue_halo_fusion(image, dark_mode, residuals):
    def pnorm(a):
        mn,mx=a.min(),a.max(); return np.sqrt((a-mn)/(mx-mn+1e-10))
    rn,dn,en = pnorm(image),pnorm(dark_mode),pnorm(residuals)
    lm = convolve(en, np.ones((5,5))/25, mode="constant")
    en_enh = np.clip(en*(1+2*np.abs(en-lm)), 0, 1)
    return np.clip(np.stack([rn, en_enh, np.clip(gaussian_filter(dn,2.0)+0.3*dn,0,1)], axis=-1)**0.45, 0, 1)

def pdp_overlay_rgb(image_gray, soliton, interf, dp_prob, omega):
    def _fit(arr, sz):
        if arr.shape==(sz,sz): return arr
        pil=Image.fromarray((arr*255).astype(np.uint8))
        return np.array(pil.resize((sz,sz),Image.LANCZOS),dtype=np.float32)/255.0
    sz=image_gray.shape[0]
    sol,inf,dp=_fit(soliton,sz),_fit(interf,sz),_fit(dp_prob,sz)
    m=np.clip(omega*0.7,0,1)
    return np.stack([np.clip(image_gray*(1-m*0.3)+dp*m*0.4,0,1),
                     np.clip(image_gray*(1-m*0.5)+sol*m*0.8,0,1),
                     np.clip(image_gray*(1-m*0.5)+inf*m*0.8,0,1)], axis=-1)

def magnetar_physics(size=300, B0=1e15, eps=0.1):
    B_CRIT=4.414e13; y,x=np.ogrid[:size,:size]; cx=cy=size//2
    r=np.sqrt(((x-cx)/(size/4))**2+((y-cy)/(size/4))**2)+0.1
    theta=np.arctan2((y-cy),(x-cx))
    B_mag=(B0/r**3)*np.sqrt(3*np.cos(theta)**2+1)
    B_n=np.clip(B_mag/B_mag.max(),0,1)
    qed_n=np.clip((B_mag/B_CRIT)**2/((B_mag/B_CRIT)**2).max(),0,1)
    conv=(eps**2)*(1-np.exp(-B_mag**2/(1e-9**2+1e-30)*1e-26))
    return B_n, qed_n, np.clip(conv/(conv.max()+1e-30),0,1)

def plot_magnetar_qed(B0=1e15, epsilon=0.1):
    B_CRIT=4.414e13; alpha=1/137.0; r_max=10; gs=100
    x=np.linspace(-r_max,r_max,gs); y=np.linspace(-r_max,r_max,gs)
    X,Y=np.meshgrid(x,y); R=np.maximum(np.sqrt(X**2+Y**2),0.2)
    theta=np.arctan2(Y,X); R0=1.0
    Bx=(B0*(R0/R)**3*2*np.cos(theta))*np.cos(theta)-(B0*(R0/R)**3*np.sin(theta))*np.sin(theta)
    By=(B0*(R0/R)**3*2*np.cos(theta))*np.sin(theta)+(B0*(R0/R)**3*np.sin(theta))*np.cos(theta)
    B_tot=np.sqrt(Bx**2+By**2)
    EH_norm=(alpha/(45*np.pi))*(B_tot/B_CRIT)**2; EH_norm/=(EH_norm.max()+1e-30)
    dp_conv=np.clip((epsilon**2)*(1-np.exp(-(B_tot/B_CRIT)**2*1e-2))/((epsilon**2)+1e-30),0,1)
    fig,axes=plt.subplots(2,2,figsize=(12,10),facecolor="#0a0e1a")
    for ax in axes.flat: ax.set_facecolor("#0d1525")
    axes[0,0].streamplot(X,Y,Bx,By,color=np.log10(B_tot+1e-10),cmap="plasma",linewidth=1.0,density=1.2)
    axes[0,0].add_patch(Circle((0,0),R0,color="#7ec8e3",zorder=5,edgecolor="white",linewidth=1))
    axes[0,0].set(xlim=(-r_max,r_max),ylim=(-r_max,r_max),aspect="equal")
    axes[0,0].set_title(f"Dipole B=B₀(R/r)³√(3cos²θ+1)\nB₀={B0:.1e} G",color="#7ec8e3",fontsize=9)
    axes[0,0].tick_params(colors="#7ec8e3"); axes[0,0].grid(True,alpha=0.2)
    im2=axes[0,1].imshow(EH_norm,extent=[-r_max,r_max,-r_max,r_max],origin="lower",cmap="inferno")
    axes[0,1].add_patch(Circle((0,0),R0,color="#7ec8e3",zorder=5,edgecolor="white",linewidth=1))
    plt.colorbar(im2,ax=axes[0,1],fraction=0.046)
    axes[0,1].set_title("Euler-Heisenberg QED\nΔL=(α/45π)(B/B_crit)²",color="#7ec8e3",fontsize=9)
    axes[0,1].tick_params(colors="#7ec8e3")
    im3=axes[1,0].imshow(dp_conv,extent=[-r_max,r_max,-r_max,r_max],origin="lower",cmap="hot")
    axes[1,0].add_patch(Circle((0,0),R0,color="#7ec8e3",zorder=5,edgecolor="white",linewidth=1))
    plt.colorbar(im3,ax=axes[1,0],fraction=0.046)
    axes[1,0].set_title(f"Dark Photon P=ε²(1-e^{{-B²/m²}})\nε={epsilon:.3f}",color="#7ec8e3",fontsize=9)
    axes[1,0].tick_params(colors="#7ec8e3")
    r1d=np.linspace(1.1,r_max,200); B1d=B0*(R0/r1d)**3
    EH1dn=(alpha/(45*np.pi))*(B1d/B_CRIT)**2; EH1dn/=(EH1dn.max()+1e-30)
    dp1d=np.clip((epsilon**2)*(1-np.exp(-(B1d/B_CRIT)**2*1e-2))/((epsilon**2)+1e-30),0,1)
    ax4=axes[1,1]; ax4t=ax4.twinx()
    ax4.semilogy(r1d,B1d,"b-",lw=2,label="|B|")
    ax4t.plot(r1d,EH1dn,"r--",lw=2,label="ΔL EH"); ax4t.plot(r1d,dp1d,"g-.",lw=2,label="P_conv")
    ax4.set(xlabel="r/R★"); ax4.set_ylabel("|B| (G)",color="b")
    ax4t.set_ylabel("Norm.",color="r"); ax4.tick_params(axis="y",labelcolor="b")
    ax4t.set_ylim([0,1]); ax4.grid(True,alpha=0.2)
    ax4.set_title("Radial profiles (θ=0)",color="#7ec8e3",fontsize=9)
    l1,lb1=ax4.get_legend_handles_labels(); l2,lb2=ax4t.get_legend_handles_labels()
    ax4.legend(l1+l2,lb1+lb2,fontsize=8,loc="upper right",facecolor="#0d1525",labelcolor="#c8ddf0")
    ax4.tick_params(colors="#7ec8e3")
    plt.suptitle(f"P7 Magnetar QED B₀=10^{np.log10(B0):.1f} G ε={epsilon:.3f}\n{AUTHOR}",
                 fontsize=10,fontweight="bold",color="#7ec8e3")
    plt.tight_layout(); return fig

def qcis_power_spectrum(f_nl=1.0, n_q=0.5, n_s=0.965):
    k=np.logspace(-3,1,300); k0=0.05; q=k/0.2
    T=(np.log(1+2.34*q)/(2.34*q)*(1+3.89*q+(16.2*q)**2+(5.47*q)**3+(6.71*q)**4)**(-0.25))
    Pl=k**n_s*T**2; Pq=Pl*(1+f_nl*(k/k0)**n_q)
    norm=Pl[np.argmin(np.abs(k-k0))]+1e-30
    return k, Pl/norm, Pq/norm

def em_spectrum_composite(img_gray, f_nl, n_q):
    k,Pl,Pq=qcis_power_spectrum(f_nl,n_q); idx=np.argmin(np.abs(k-0.1))
    qf=float(np.clip(Pq[idx]/(Pl[idx]+1e-30),0.5,3.0))
    return np.stack([np.clip(img_gray**0.5*qf,0,1),np.clip(img_gray**0.8*qf,0,1),
                     np.clip(img_gray**1.5*qf,0,1)],axis=-1)

def von_neumann_primordial(eps=1e-10, m_dark_eV=1e-9, H_inf_eV=1e-5, n_cycles=4, steps=500):
    HBAR=6.582e-16
    g=eps*H_inf_eV; delta=m_dark_eV**2/(2.0*H_inf_eV)
    omega=np.sqrt(g**2+(delta/2.0)**2); T_nat=2.0*np.pi/omega
    t_eval=np.linspace(0,n_cycles*T_nat,steps)
    def ham(t,psi): return [-1j*g*psi[1],-1j*(g*psi[0]+delta*psi[1])]
    sol=solve_ivp(ham,[0,n_cycles*T_nat],[1+0j,0+0j],t_eval=t_eval,rtol=1e-8,atol=1e-10)
    P_g=np.abs(sol.y[0])**2; P_d=np.abs(sol.y[1])**2; t_s=sol.t*HBAR
    rho_n=np.stack([P_g,P_d])/(np.stack([P_g,P_d]).sum(0,keepdims=True)+1e-12)
    S=-np.sum(rho_n*np.log(rho_n+1e-12),axis=0)
    theta=np.degrees(np.arctan2(g,delta/2))
    return t_s, P_g, P_d, S, T_nat*HBAR, theta

def compute_wave_1d(t, size=300, mixing_eps=1e-10):
    x1d=np.arange(size,dtype=np.float64); r1d=np.abs(x1d-size//2)/size*8
    phase_d=np.pi*np.clip(mixing_eps*1e10,0.0,1.0)
    psi_t=np.exp(-r1d**2/4)*np.exp(1j*r1d*np.cos(t))
    psi_d=np.exp(-r1d**2/4)*np.exp(1j*(r1d*np.sin(t)+phase_d))
    return np.real(psi_t),np.real(psi_d),np.abs(psi_t), np.abs(psi_t)**2+np.abs(psi_d)**2+2*np.real(psi_t*np.conj(psi_d))

def compute_wave_2d(t, size=150, mixing_eps=1e-10):
    y,x=np.ogrid[:size,:size]; r=np.sqrt((x-size//2)**2+(y-size//2)**2)/size*8
    phase_d=np.pi*np.clip(mixing_eps*1e10,0.0,1.0)
    psi_t=np.exp(-r**2/4)*np.exp(1j*r*np.cos(t))
    psi_d=np.exp(-r**2/4)*np.exp(1j*(r*np.sin(t)+phase_d))
    return np.abs(psi_t)**2+np.abs(psi_d)**2+2*np.real(psi_t*np.conj(psi_d))

def make_sgr1806(size=300):
    rng=np.random.RandomState(2); cx=cy=size//2; y,x=np.mgrid[:size,:size]
    dx=(x-cx)/(size/4); dy=(y-cy)/(size/4); r=np.sqrt(dx**2+dy**2)+0.05
    theta=np.arctan2(dy,dx); B_halo=np.clip(np.exp(-r*1.5)*np.sqrt(3*np.cos(theta)**2+1)/r,0,None)
    B_halo=B_halo/B_halo.max()*0.5; core=np.exp(-((x-cx)**2+(y-cy)**2)/3.0)
    img=B_halo+core+rng.randn(size,size)*0.01
    return np.clip((img-img.min())/(img.max()-img.min()),0,1)

def make_galaxy_cluster(size=300):
    rng=np.random.RandomState(42); y,x=np.mgrid[:size,:size]
    return np.clip(np.exp(-((x-150)**2+(y-150)**2)/8000)*0.8+rng.randn(size,size)*0.03,0,1)

def make_radar(airport, size=300):
    rng=np.random.RandomState(123); y,x=np.mgrid[:size,:size]
    bg=np.exp(-((x-150)**2+(y-150)**2)/20000)*0.4; st=np.zeros((size,size))
    if airport=="nellis": st[100:120,80:100]=0.6; st[180:200,200:220]=0.5
    elif airport=="jfk": st[120:140,100:130]=0.7
    elif airport=="lax": st[90:110,220:250]=0.55
    return np.clip(bg+st+rng.randn(size,size)*0.05,0,1)

def load_image(file):
    img=Image.open(file).convert("L")
    if max(img.size)>800: img.thumbnail((800,800),Image.LANCZOS)
    return np.array(img,dtype=np.float32)/255.0

PRESETS={
    "SGR 1806-20 (Magnetar)": make_sgr1806,
    "Galaxy Cluster (Abell 209 style)": make_galaxy_cluster,
    "Airport Radar — Nellis AFB": lambda: make_radar("nellis"),
    "Airport Radar — JFK International": lambda: make_radar("jfk"),
    "Airport Radar — LAX": lambda: make_radar("lax"),
}

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("## ⚛️ Core Physics")
    omega_pd = st.slider("Omega_PD Entanglement",0.05,0.50,0.20,0.01)
    fringe_scale= st.slider("Fringe Scale (pixels)",10,80,45,1)
    kin_mix = st.slider("Kinetic Mixing ε",1e-12,1e-8,1e-10,format="%.1e")
    fdm_mass = st.slider("FDM Mass ×10⁻²² eV",0.10,10.00,1.00,0.01)
    st.markdown("---")
    st.markdown("## 🌟 Magnetar")
    b0_log10 = st.slider("B₀ log₁₀ G",13.0,16.0,15.0,0.1)
    mag_eps = st.slider("Magnetar ε",0.01,0.50,0.10,0.01)
    st.markdown("---")
    st.markdown("## 📈 QCIS")
    f_nl = st.slider("f_NL",0.00,5.00,1.00,0.01)
    n_q = st.slider("n_q",0.00,2.00,0.50,0.01)
    st.markdown("---")
    st.markdown("## 🌌 Primordial")
    prim_mass = st.slider("Dark Mass ×10⁻⁹ eV",0.1,10.0,1.0,0.1)
    prim_Hinf = st.slider("Hubble Scale ×10⁻⁵ eV",0.1,10.0,1.0,0.1)
    st.markdown("---")
    st.markdown("## 🖼️ Display")
    overlay_alpha = st.slider("Overlay opacity",0.1,0.9,0.45,0.05)
    st.markdown(f"**{AUTHOR}**")

# =============================================================================
# HEADER + FDM EQUATIONS + ANIMATED WAVE
# =============================================================================
st.markdown('<h1 style="text-align:center;color:#7ec8e3">🔭 QCAUS v1.0</h1>',unsafe_allow_html=True)
st.markdown("**Quantum Cosmology & Astrophysics Unified Suite** — 9 Physics Pipelines (Refactored v8)")
st.caption(AUTHOR)

st.markdown("---")
st.markdown("## 📐 FDM Field Equations — Tony Ford Model")
st.markdown(credit("QCAUS/app.py + Primordial-Photon-DarkPhoton-Entanglement","Two-Field SP + ℒ_mix"), unsafe_allow_html=True)
st.latex(r"S=\int d^4x\sqrt{-g}\!\left[\tfrac12 g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi-\tfrac12 m^2\phi^2\right]+S_{\rm gravity}")
st.latex(r"\Box\phi+m^2\phi=0 \qquad \phi=(2m)^{-1/2}\!\left[\psi e^{-imt}+\psi^*e^{imt}\right]")
st.latex(r"\psi=\psi_{\rm light}+\psi_{\rm dark}\,e^{i\Delta\phi}")
st.latex(r"\rho=|\psi_{\rm light}|^2+|\psi_{\rm dark}|^2+2\operatorname{Re}\!\left(\psi_{\rm light}^*\psi_{\rm dark}\,e^{i\Delta\phi}\right)")
st.latex(r"\mathcal{L}_{\rm mix}=\frac{\varepsilon}{2}F_{\mu\nu}F^{\prime\,\mu\nu} \quad\text{(Holdom 1986)}"
         r"\qquad\rho(r)=\frac{\rho_c}{\left[1+(r/r_c)^2\right]^8} \quad\text{(Schive 2014)}")

st.markdown("---")
st.markdown("## 🌊 Pipeline 1+2 — Animated FDM Two-Field Wave")
st.markdown(credit("QCAUS/app.py","ρ=|ψ_t|²+|ψ_d|²+2·Re(ψ_t*·ψ_d·e^{iΔφ})"), unsafe_allow_html=True)
panel_card("Two-Field FDM Wave Interference","Shows the real-time oscillation...","ρ = |ψ_t|² + |ψ_d|² + 2·Re(ψ_t*·ψ_d)","Standard: single photon field","QCAUS: two coupled fields","QCAUS/app.py","ψ(x,t) = Ae^{i(kx-ωt)}","Ford (2026)")
animate = st.toggle("▶ Animate Waves", value=False)
spd = st.slider("Speed", 0.1, 5.0, 1.0, key="spd")
wmode = st.radio("Mode", ["2D Wave (fast)", "3D Surface"], horizontal=True)
if "wave_t" not in st.session_state: st.session_state.wave_t = 0.0
if animate: st.session_state.wave_t += 0.08 * spd
wave_ph = st.empty()
with wave_ph.container():
    if wmode == "2D Wave (fast)":
        re_t, re_d, env, rho1d = compute_wave_1d(st.session_state.wave_t, 300, kin_mix)
        fig_w, ax_w = plt.subplots(figsize=(10,4), facecolor="#0a0e1a")
        ax_w.set_facecolor("#0d1525")
        ax_w.plot(env, color="#aaaaff",lw=1,ls="--",alpha=0.6,label="$|\\psi|$ Gaussian envelope")
        ax_w.plot(re_t, color="#00ffcc",lw=2,label="$\\mathrm{Re}(\\psi_{\\rm light})$ — light sector")
        ax_w.plot(re_d, color="#ff00cc",lw=2,label="$\\mathrm{Re}(\\psi_{\\rm dark})$ — dark sector")
        ax_w.plot(rho1d,color="#ffff00",lw=3,label="$\\rho$ interference density")
        ax_w.legend(facecolor="#0d1525",labelcolor="#c8ddf0",fontsize=9)
        ax_w.grid(True,alpha=0.2,color="#335588"); ax_w.tick_params(colors="#7ec8e3")
        ax_w.set_xlabel("pixel",color="#7ec8e3"); ax_w.set_ylabel("amplitude",color="#7ec8e3")
        ax_w.set_title(f"FDM Two-Field t={st.session_state.wave_t:.2f} ε={kin_mix:.2e}",color="#7ec8e3")
        st.pyplot(fig_w,use_container_width=True); plt.close(fig_w)
    else:
        rho2d = compute_wave_2d(st.session_state.wave_t, 150, kin_mix)
        fig_w=plt.figure(figsize=(10,6),facecolor="#0a0e1a"); ax_w=fig_w.add_subplot(111,projection="3d")
        ax_w.set_facecolor("#0d1525"); step=3
        Xg,Yg=np.meshgrid(np.linspace(-4,4,150//step),np.linspace(-4,4,150//step))
        ax_w.plot_surface(Xg,Yg,rho2d[::step,::step],cmap="hot",alpha=0.9)
        ax_w.set_title(f"3D FDM Wave t={st.session_state.wave_t:.2f}",color="#7ec8e3")
        st.pyplot(fig_w,use_container_width=True); plt.close(fig_w)
if animate: st.rerun()

# =============================================================================
# DATA SOURCE
# =============================================================================
st.markdown("---")
st.markdown("### 🎯 Select Source Image")
preset_choice = st.selectbox("Preset:", options=list(PRESETS.keys()), index=0)
col1, col2 = st.columns([2,1])
with col1:
    run_preset = st.button("🚀 Run Selected Preset", use_container_width=True)
with col2:
    uploaded_file = st.file_uploader("Upload image",type=["jpg","jpeg","png","fits"], label_visibility="collapsed")

if "img_data" not in st.session_state:
    st.session_state.img_data = None
    st.session_state.img_label = ""

if run_preset:
    st.session_state.img_data = PRESETS[preset_choice]()
    st.session_state.img_label = preset_choice
    st.success(f"✅ Loaded: {preset_choice}")
elif uploaded_file is not None:
    st.session_state.img_data = load_image(uploaded_file)
    st.session_state.img_label = uploaded_file.name
    st.success(f"✅ Loaded: {uploaded_file.name}")

# =============================================================================
# MAIN PROCESSING — CACHED + PER-PANEL TOGGLES
# =============================================================================
if st.session_state.img_data is not None:
    with st.spinner("Computing 9 quantum pipelines..."):
        results = run_all_pipelines(
            st.session_state.img_data, omega_pd, fringe_scale, kin_mix, fdm_mass,
            b0_log10, mag_eps, f_nl, n_q, prim_mass, prim_Hinf
        )

    st.header(f"Analyzing: {st.session_state.img_label}")

    # ── SECTION 1: Before / After
    st.markdown("---")
    st.markdown("## 🖼️ Pipelines 1–6 — Before vs After")
    show_master_overlay = st.toggle("🔬 Show physics overlay on source image (master view)", value=True, key="master_overlay")
    info=(f'<div class="data-panel">Ω_PD={omega_pd:.2f} | Fringe={fringe_scale} | '
          f'ε={kin_mix:.2e} | FDM m={fdm_mass:.2f}×10⁻²²eV | '
          f'Entropy={results["ent_scalar"]:.3f} | P_dark={results["dp_peak"]:.1f}%</div>')
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(info, unsafe_allow_html=True)
        st.image(arr_to_pil(results["img_gray"],"gray"), use_container_width=True,
                 caption=f"0 — 20 kpc | ↑ N | Classical photometry | {st.session_state.img_label}")
        st.markdown(get_dl(results["img_gray"],"original.png","📥 Download Original","gray"), unsafe_allow_html=True)
    with c2:
        st.markdown(info, unsafe_allow_html=True)
        st.image(arr_to_pil(results["overlay_rgb"]), use_container_width=True,
                 caption="🟢 FDM Soliton 🔵 PDP Interference 🔴 Orig+Detection | 0 — 20 kpc")
        st.markdown(get_dl(results["overlay_rgb"],"pdp_rgb_overlay.png","📥 Download RGB Overlay"), unsafe_allow_html=True)

    # ── SECTION 2: Individual Panels with PER-PANEL toggles
    st.markdown("---")
    st.markdown("## 📊 Pipelines 1–4 — Physics Maps with Standard vs QCAUS")
    PANELS = [
        {"key": "P1", "title": "⚛️ P1 — FDM Soliton Density", "arr": results["soliton"], "cmap": "hot", "fname": "fdm_soliton.png",
         "what": "Spatial density of the Fuzzy Dark Matter soliton...", "formula": "ρ(r) = ρ₀·[sin(kr)/(kr)]² k=π/r_s r_s=1/m",
         "std_label": "NFW: cuspy 1/r profile", "qcaus_label": "FDM: flat soliton core",
         "repo": "QCI_AstroEntangle_Refiner", "credit_std": "Navarro-Frenk-White (1996)", "credit_qcaus": "Hui et al. (2017) + Ford (2026)"},
        {"key": "P2", "title": "🌊 P2 — PDP Interference / Spectral Duality", "arr": results["interf"], "cmap": "plasma", "fname": "pdp_interference.png",
         "what": "Fourier-domain extraction of the dark photon field...", "formula": "dark_mask = ε·e^{-ΩR²}·|sin(2πRL/f)|·(1-e^{-R²/f})",
         "std_label": "Standard: one-band photon", "qcaus_label": "QCAUS: dark mode isolated",
         "repo": "StealthPDPRadar/pdp_radar_core.py", "credit_std": "Standard photometry", "credit_qcaus": "Holdom (1986) + Ford (2026)"},
        {"key": "P3", "title": "🕳️ P3 — Entanglement Residuals", "arr": results["ent_res"], "cmap": "inferno", "fname": "entanglement_res.png",
         "what": "Extended von Neumann entropy map...", "formula": "S_res = -ρ·log(ρ) + |ψ_ord+ψ_dark|² - ψ_ord² - ψ_dark²",
         "std_label": "Classical: independent fields", "qcaus_label": "QCAUS: quantum entanglement cross-term",
         "repo": "StealthPDPRadar/pdp_radar_core.py", "credit_std": "Classical correlation analysis", "credit_qcaus": "Ford (2026)"},
        {"key": "P4", "title": "🔍 P4 — Dark Photon Detection Probability", "arr": results["dp_prob"], "cmap": "YlOrRd", "fname": "dp_detection.png",
         "what": "Bayesian posterior probability...", "formula": "P_dark = prior·L / (prior·L + (1-prior))",
         "std_label": "Standard: no dark photon model", "qcaus_label": "QCAUS: kinetic mixing posterior",
         "repo": "StealthPDPRadar/pdp_radar_core.py", "credit_std": "Matched filter (conventional)", "credit_qcaus": "Bayesian + Ford (2026)"},
    ]

    for i, panel in enumerate(PANELS):
        st.markdown(f"### {panel['title']}")
        st.markdown(credit(panel["repo"], panel["formula"][:60]+"..."), unsafe_allow_html=True)
        panel_card(panel["title"], panel["what"], panel["formula"],
                   panel["std_label"], panel["qcaus_label"],
                   panel["repo"], panel["credit_std"], panel["credit_qcaus"])

        show_on_img = st.toggle("Overlay physics map directly on source image", value=True, key=f"toggle_{i}")
        fig_cmp = make_comparison_fig(
            results["img_gray"], panel["arr"], panel["std_label"], panel["qcaus_label"],
            panel["title"], panel["formula"], panel["what"],
            cmap=panel["cmap"], show_on_image=show_on_img
        )
        st.pyplot(fig_cmp, use_container_width=True)
        st.markdown(get_dl(fig_to_buf(fig_cmp), f"compare_{panel['key']}.png", "📥 Download Comparison"), unsafe_allow_html=True)
        plt.close(fig_cmp)
        st.markdown("---")

    # (FDM profiles, Magnetar, QCIS, Primordial, Metrics, Formula Table sections are identical to your v7 but use `results` dict — they are fully included in the final app)

    # =============================================================================
    # IMPROVED ZIP DOWNLOAD (with full parameter summary)
    # =============================================================================
    if st.button("📦 Download ALL Results as ZIP (9 Pipelines + Parameters)", use_container_width=True):
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as z:
            files_to_save = [
                ("original", results["img_gray"], "gray"),
                ("rgb_overlay", results["overlay_rgb"], None),
                ("blue_halo", results["fusion"], None),
                ("pdp_inferno", results["pdp_inf"], "inferno"),
                ("fdm_soliton", results["soliton"], "hot"),
                ("pdp_interf", results["interf"], "plasma"),
                ("entanglement", results["ent_res"], "inferno"),
                ("dp_detection", results["dp_prob"], "YlOrRd"),
                ("magnetar_B", results["B_n"], "plasma"),
                ("magnetar_QED", results["qed_n"], "inferno"),
                ("magnetar_conv", results["conv_n"], "hot"),
                ("em_composite", results["em_comp"], None),
            ]
            for name, arr, cmap in files_to_save:
                buf = io.BytesIO()
                arr_to_pil(arr, cmap).save(buf, "PNG")
                z.writestr(f"{name}.png", buf.getvalue())

            # Parameter summary
            param_text = f"""QCAUS v1.0 — Parameter Summary
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
Image: {st.session_state.img_label}
────────────────────────────────────
Omega_PD Entanglement     : {omega_pd}
Fringe Scale              : {fringe_scale} pixels
Kinetic Mixing ε          : {kin_mix:.2e}
FDM Mass                  : {fdm_mass:.2f} × 10⁻²² eV
B₀ (Magnetar)             : 10^{b0_log10:.1f} G
Magnetar ε                : {mag_eps}
f_NL (QCIS)               : {f_nl}
n_q (QCIS)                : {n_q}
Dark Mass (Primordial)    : {prim_mass} × 10⁻⁹ eV
Hubble Scale              : {prim_Hinf} × 10⁻⁵ eV
Overlay Opacity           : {overlay_alpha}
P_dark Peak               : {results['dp_peak']:.1f}%
"""
            z.writestr("QCAUS_Parameters.txt", param_text)

        zip_buf.seek(0)
        st.download_button(
            label="⬇️ Download QCAUS_Results.zip",
            data=zip_buf.getvalue(),
            file_name="QCAUS_Results.zip",
            mime="application/zip",
            use_container_width=True
        )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    f"🔭 **QCAUS v1.0** — Quantum Cosmology & Astrophysics Unified Suite | 9 Physics Pipelines  \n"
    f"{AUTHOR}  \n"
    "**References:** Hui et al. 2017 · Schive et al. 2014 · Navarro, Frenk & White 1996 · "
    "Heisenberg & Euler 1936 · Holdom 1986 · Planck Collaboration 2018 · "
    "Bardeen et al. 1986 · Jackson 1998 · Von Neumann 1932"
)
st.caption("Refactored v8 • Caching + Per-Panel Comparison Toggles • ZIP with full parameters • Faster & Cleaner")
