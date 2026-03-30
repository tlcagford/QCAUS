<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>QCAUS v21.0</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<style>
:root{--bg:#0a0b10;--fg:#e8e6e3;--mt:#6b6878;--ac:#00ff8c;--cd:#111219;--bd:#1e1f2e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'JetBrains Mono',monospace;background:var(--bg);color:var(--fg);font-size:11px}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--bd);border-radius:3px}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 10% 15%,rgba(0,255,140,.03) 0%,transparent 50%),radial-gradient(ellipse at 90% 85%,rgba(255,107,53,.02) 0%,transparent 50%);pointer-events:none}
body::after{content:'';position:fixed;inset:0;background-image:radial-gradient(rgba(255,255,255,.012) 1px,transparent 1px);background-size:26px 26px;pointer-events:none}
.pn{background:var(--cd);border:1px solid var(--bd);border-radius:6px;overflow:hidden;position:relative}
.pn canvas{display:block;width:100%;height:auto}
.pn:hover{border-color:rgba(0,255,140,.2)}
input[type=range]{-webkit-appearance:none;width:100%;height:3px;background:var(--bd);border-radius:2px;outline:none;cursor:pointer}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:10px;height:10px;border-radius:50%;background:var(--ac);cursor:pointer;box-shadow:0 0 6px rgba(0,255,140,.4)}
.sg{margin-bottom:8px}.sl{display:flex;justify-content:space-between;margin-bottom:2px}
.sl span:first-child{font-size:8.5px;color:var(--mt);text-transform:uppercase;letter-spacing:.3px}
.sl .v{font-size:9.5px;color:var(--ac)}
.bt{width:100%;padding:7px;background:rgba(0,255,140,.07);border:1px solid rgba(0,255,140,.2);border-radius:4px;color:var(--ac);font-family:inherit;font-size:9px;cursor:pointer;letter-spacing:.6px;text-transform:uppercase;transition:all .2s}
.bt:hover{background:rgba(0,255,140,.14);border-color:var(--ac)}
.bt.on{background:rgba(0,255,140,.18);border-color:var(--ac);box-shadow:0 0 10px rgba(0,255,140,.08)}
.mc{background:var(--cd);border:1px solid var(--bd);border-radius:6px;padding:10px;text-align:center}
.mc .vl{font-size:18px;font-weight:700;color:var(--ac)}.mc .lb{font-size:8.5px;color:var(--mt);margin-top:3px}.mc .dt{font-size:8px;color:var(--mt);margin-top:1px}
.al{padding:8px 12px;border-radius:5px;margin-top:6px;font-size:10px}
.al-w{background:rgba(255,107,53,.08);border:1px solid rgba(255,107,53,.25);color:#ff6b35}
.al-e{background:rgba(255,51,85,.08);border:1px solid rgba(255,51,85,.25);color:#ff3355}
.al-g{background:rgba(0,255,140,.06);border:1px solid rgba(0,255,140,.2);color:var(--ac)}
.dh{position:absolute;top:0;bottom:0;width:3px;background:var(--ac);cursor:col-resize;z-index:5;box-shadow:0 0 8px rgba(0,255,140,.4)}
@keyframes sc{0%{top:-2px}100%{top:100%}}
.pn.sc::before{content:'';position:absolute;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--ac),transparent);z-index:10;animation:sc .6s ease-out forwards;pointer-events:none}
.sd{width:6px;height:6px;border-radius:50%;background:var(--ac);display:inline-block;animation:pu 2s infinite}
@keyframes pu{0%,100%{opacity:1;box-shadow:0 0 4px var(--ac)}50%{opacity:.3;box-shadow:none}}
.tag{font-size:7.5px;padding:2px 6px;border-radius:3px;color:var(--mt);background:rgba(255,255,255,.015);border:1px solid var(--bd);display:inline-block}
</style>
</head>
<body>
<header class="relative z-10 border-b border-[--bd]" style="background:linear-gradient(to bottom,rgba(17,18,25,.97),rgba(10,11,16,.99))">
<div class="max-w-[1700px] mx-auto px-3 py-2">
<div class="flex items-center justify-between flex-wrap gap-2">
<div class="flex items-center gap-2">
<div class="w-7 h-7 rounded flex items-center justify-center" style="background:linear-gradient(135deg,var(--ac),#00aa5c)"><i class="fa-solid fa-atom text-xs" style="color:var(--bg)"></i></div>
<div><div class="text-sm font-bold tracking-wider" style="color:var(--ac)">QCAUS v21.0</div><div style="font-size:8px;color:var(--mt)">Quantum Cosmology & Astrophysics Unified Suite</div></div>
</div>
<div class="flex items-center gap-3" style="font-size:8.5px;color:var(--mt)">
<span>Target: <b style="color:var(--fg)">Swift J1818.0-1607</b></span><span>d=6.5kpc</span><span>P=1.36s</span><span>B=2.7e14G</span>
</div>
<div class="flex items-center gap-2"><span class="sd"></span><span id="stT" style="font-size:8.5px;color:var(--ac)">READY</span></div>
</div>
<div class="flex items-center gap-1.5 mt-1 flex-wrap">
<span class="tag">[1] QCAUS/app.py</span><span class="tag">[2] StealthPDPRadar</span><span class="tag">[3] PDP Entanglement</span><span class="tag">[4] Magnetar QED</span><span class="tag">[5] QCIS</span><span class="tag">[6] WFC3 PSF</span><span class="tag">[7] JWST</span><span class="tag">[8] EDSR Refiner</span>
</div>
</div>
</header>

<div class="relative z-10 flex max-w-[1700px] mx-auto" style="min-height:calc(100vh - 64px)">
<aside id="sb" class="flex flex-col gap-0.5 p-2.5 border-r border-[--bd] overflow-y-auto" style="width:235px;min-width:235px;background:rgba(14,15,22,.7)">
<div class="font-bold tracking-widest mb-1.5" style="font-size:8.5px;color:var(--ac)">PRESET REAL DATA</div>
<div class="grid grid-cols-2 gap-1 mb-2" id="pBtns">
<button class="bt on" data-k="swift"><i class="fa-solid fa-bolt mr-1"></i>Swift J1818</button>
<button class="bt" data-k="crab"><i class="fa-solid fa-circle-dot mr-1"></i>Crab M1</button>
<button class="bt" data-k="sgr"><i class="fa-solid fa-star mr-1"></i>SGR 1806</button>
<button class="bt" data-k="galaxy"><i class="fa-solid fa-hurricane mr-1"></i>Galaxy</button>
<button class="bt" data-k="magnetar"><i class="fa-solid fa-magnet mr-1"></i>Magnetar</button>
</div>
<div style="font-size:8.5px;color:var(--mt);margin-bottom:6px">— OR —</div>
<label class="block p-2 rounded cursor-pointer border border-dashed border-[--bd] text-center mb-2" style="font-size:8.5px;color:var(--mt)">
<i class="fa-solid fa-upload mr-1"></i>Drop FITS/JPG/PNG
<input type="file" id="fIn" accept=".fits,.fit,.fz,.jpg,.jpeg,.png,.bmp" class="hidden">
</label>
<div class="font-bold tracking-widest mb-1" style="font-size:8.5px;color:var(--ac)">CORE PHYSICS [1][3][8]</div>
<div class="sg"><div class="sl"><span>Omega_PD [8] def 0.20</span><span class="v" id="vO">0.20</span></div><input type="range" id="sO" min="0.05" max="0.50" step="0.01" value="0.20"></div>
<div class="sg"><div class="sl"><span>Fringe Scale [8] def 45</span><span class="v" id="vFr">45</span></div><input type="range" id="sFr" min="10" max="80" step="1" value="45"></div>
<div class="sg"><div class="sl"><span>Kinetic Mixing eps</span><span class="v" id="vEp">1.0e-10</span></div><input type="range" id="sEp" min="-12" max="-7" step="0.1" value="-10"></div>
<div class="sg"><div class="sl"><span>FDM Mass x10^-22 eV</span><span class="v" id="vMf">1.0</span></div><input type="range" id="sMf" min="0.1" max="10" step="0.1" value="1.0"></div>
<div class="sg"><div class="sl"><span>Scale kpc/px</span><span class="v" id="vSk">0.42</span></div><input type="range" id="sSk" min="0.05" max="2" step="0.01" value="0.42"></div>
<div class="font-bold tracking-widest mb-1 mt-1" style="font-size:8.5px;color:var(--ac)">WFC3 PSF [6]</div>
<div class="sg"><div class="sl"><span>Focus um (-8.5..7.9)</span><span class="v" id="vFc">-0.2</span></div><input type="range" id="sFc" min="-8.5" max="7.9" step="0.1" value="-0.2"></div>
<div class="sg flex items-center gap-2"><label style="font-size:8.5px;color:var(--mt)"><input type="checkbox" id="ckP" checked class="mr-1"> Wiener Deconv [6]</label></div>
<div class="font-bold tracking-widest mb-1 mt-1" style="font-size:8.5px;color:var(--ac)">MAGNETAR [4]</div>
<div class="sg"><div class="sl"><span>B0 log10 G</span><span class="v" id="vB0">15.0</span></div><input type="range" id="sB0" min="13" max="16" step="0.1" value="15.0"></div>
<div class="sg"><div class="sl"><span>Magnetar eps</span><span class="v" id="vMe">0.10</span></div><input type="range" id="sMe" min="0.01" max="0.50" step="0.01" value="0.10"></div>
<div class="font-bold tracking-widest mb-1 mt-1" style="font-size:8.5px;color:var(--ac)">QCIS [5]</div>
<div class="sg"><div class="sl"><span>f_NL</span><span class="v" id="vFn">1.0</span></div><input type="range" id="sFn" min="0" max="5" step="0.1" value="1.0"></div>
<div class="sg"><div class="sl"><span>n_q</span><span class="v" id="vNq">0.50</span></div><input type="range" id="sNq" min="0" max="2" step="0.05" value="0.50"></div>
<button class="bt mt-2" id="bRun"><i class="fa-solid fa-play mr-1"></i>Run Full Pipeline</button>
<div class="mt-2 pt-2 border-t border-[--bd]" style="font-size:7.5px;color:var(--mt);line-height:1.5">
Tony E. Ford | tlcagford@gmail.com<br>Patent Pending | 2026<br><br>
FWHM=<span id="roF">1.921</span>px | sigma=<span id="roS">0.816</span>px<br>
qfit=<span id="roQ">—</span> | Stealth=<span id="roP">—</span>
</div>
</aside>

<main class="flex-1 p-2.5 space-y-3 overflow-y-auto">
<div id="iBar" style="font-size:9.5px;padding:6px 10px;border-radius:4px;background:rgba(0,255,140,.03);border:1px solid rgba(0,255,140,.1);color:var(--mt)">
Source: <b style="color:var(--fg)">Swift J1818.0-1607</b> | Instrument: <b style="color:var(--fg)">SYNTHETIC-SWIFT</b> | WFC3 FWHM: <b style="color:var(--ac)">1.921 px</b> at focus=-0.2um
</div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px">BEFORE VS AFTER — Clean Annotated Composite</div>
<div class="pn" id="cpP" style="aspect-ratio:2.2/1;cursor:col-resize"><canvas id="cCp" width="1024" height="465"></canvas><div class="dh" id="cDh" style="left:50%"></div></div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px;margin-top:8px">ANNOTATED PHYSICS MAPS</div>
<div class="grid grid-cols-3 gap-2">
<div class="pn"><canvas id="cSo" width="400" height="400"></canvas></div>
<div class="pn"><canvas id="cEn" width="400" height="400"></canvas></div>
<div class="pn"><canvas id="cSt" width="400" height="400"></canvas></div>
</div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px;margin-top:8px">BLUE-HALO FUSION & MAGNETAR QED [2][4]</div>
<div class="grid grid-cols-3 gap-2">
<div class="pn"><canvas id="cFu" width="400" height="400"></canvas></div>
<div class="pn"><canvas id="cMg" width="400" height="400"></canvas></div>
<div class="pn"><canvas id="cCv" width="400" height="400"></canvas></div>
</div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px;margin-top:8px">WFC3 PSF CHARACTERISATION — 13-Year Empirical Model [6]</div>
<div class="pn"><canvas id="cPF" width="1000" height="260"></canvas></div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px;margin-top:8px">WAVE INTERFERENCE — psi_light · psi_dark · |psi|^2</div>
<div class="pn"><canvas id="cWv" width="1000" height="160"></canvas></div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px;margin-top:8px">VON NEUMANN ENTROPY — i d/dt rho = [H_eff, rho] [3]</div>
<div class="grid grid-cols-2 gap-2">
<div class="pn"><canvas id="cV1" width="500" height="240"></canvas></div>
<div class="pn"><canvas id="cV2" width="500" height="240"></canvas></div>
</div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px;margin-top:8px">QCIS POWER SPECTRUM — P(k) = P_LCDM(k)*(1 + f_NL*(k/k0)^n_q) [5]</div>
<div class="pn"><canvas id="cQC" width="1000" height="260"></canvas></div>
<div style="font-size:10px;font-weight:600;color:var(--ac);letter-spacing:.3px;margin-top:8px">DETECTION METRICS</div>
<div class="grid grid-cols-6 gap-2">
<div class="mc"><div class="vl" id="m1">—</div><div class="lb">Dark Photon Conf</div><div class="dt" id="m1d"></div></div>
<div class="mc"><div class="vl" id="m2">—</div><div class="lb">Soliton Peak</div><div class="dt" id="m2d"></div></div>
<div class="mc"><div class="vl" id="m3">—</div><div class="lb">Fringe Contrast</div><div class="dt" id="m3d"></div></div>
<div class="mc"><div class="vl" id="m4">—</div><div class="lb">Mixing Omega*0.6</div><div class="dt" id="m4d"></div></div>
<div class="mc"><div class="vl" id="m5">—</div><div class="lb">Stealth P_peak</div><div class="dt" id="m5d"></div></div>
<div class="mc"><div class="vl" id="m6">—</div><div class="lb">WFC3 FWHM</div><div class="dt" id="m6d"></div></div>
</div>
<div id="sAl" class="al al-g" style="display:none"></div>
<div class="mt-3"><button class="bt" id="bZip" style="max-width:280px"><i class="fa-solid fa-download mr-1"></i>Download ALL Results (ZIP)</button></div>
<div style="font-size:7px;color:var(--mt);margin-top:8px;padding-bottom:12px">QCAUS v21.0 | Tony E. Ford | Patent Pending | Verified: QCAUS[1]·StealthPDPRadar[2]·PDP[3]·Magnetar-QED[4]·QCIS[5]·WFC3-PSF[6]·JWST[7]·EDSR[8]</div>
</main>
</div>

<script>
const N=256,NN=N*N;
const P={om:.20,fr:45,ep:1e-10,mf:1.0,sk:.42,fc:-0.2,psf:true,b0:15,me:.10,fn:1.0,nq:.50};
let curImg=null,R={},compP=.5,wT=0,curKey='swift';

function mkR(s){return()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function rn(r){let u,v,s;do{u=2*r()-1;v=2*r()-1;s=u*u+v*v}while(s>=1||s===0);return u*Math.sqrt(-2*Math.log(s)/s)}
const aN=()=>new Float64Array(NN);
function aMx(a){let m=-1e30;for(let i=0;i<NN;i++)if(a[i]>m)m=a[i];return m}
function aMn(a){let m=1e30;for(let i=0;i<NN;i++)if(a[i]<m)m=a[i];return m}
function aSm(a){let s=0;for(let i=0;i<NN;i++)s+=a[i];return s}
function aAv(a){return aSm(a)/NN}
function aSd(a){const m=aAv(a);let s=0;for(let i=0;i<NN;i++)s+=(a[i]-m)**2;return Math.sqrt(s/NN)}
function aNm(a){const m=aMx(a),o=aN();for(let i=0;i<NN;i++)o[i]=a[i]/(m+1e-30);return o}
function aCl(a){const o=aN();for(let i=0;i<NN;i++)o[i]=a[i]<0?0:a[i]>1?1:a[i];return o}
function aAb(a){const o=aN();for(let i=0;i<NN;i++)o[i]=a[i]<0?-a[i]:a[i];return o}
function aSc(a,s){const o=aN();for(let i=0;i<NN;i++)o[i]=a[i]*s;return o}

function bLUT(fn){const L=new Uint8Array(768);for(let i=0;i<256;i++){const c=fn(i/255);L[i*3]=c[0]|0;L[i*3+1]=c[1]|0;L[i*3+2]=c[2]|0}return L}
function lrp(a,b,t){return[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t]}
function mLUT(pts){return bLUT(t=>{for(let i=0;i<pts.length-1;i++)if(t<=pts[i+1][0]){const s=(t-pts[i][0])/(pts[i+1][0]-pts[i][0]);return lrp(pts[i],pts[i+1],s)}return pts[pts.length-1]})}
const CM={
gray:bLUT(t=>[t*255,t*255,t*255]),
hot:mLUT([[0,[0,0,0]],[.33,[255,0,0]],[.67,[255,255,0]],[1,[255,255,255]]]),
inferno:mLUT([[0,[0,0,4]],[.14,[40,11,84]],[.29,[101,21,110]],[.43,[159,42,99]],[.57,[212,72,66]],[.71,[245,125,21]],[.86,[250,193,39]],[1,[252,255,164]]]),
plasma:mLUT([[0,[13,8,135]],[.25,[126,3,168]],[.5,[203,70,121]],[.75,[248,148,65]],[1,[240,249,33]]]),
YlOrRd:mLUT([[0,[255,255,204]],[.25,[255,237,160]],[.5,[254,178,76]],[.75,[240,120,30]],[1,[180,20,10]]])
};

// Cooley-Tukey radix-2 FFT
function fft1(re,im,inv){const n=re.length;for(let i=1,j=0;i<n;i++){let b=n>>1;for(;j&b;b>>=1)j^=b;j^=b;if(i<j){[re[i],re[j]]=[re[j],re[i]];[im[i],im[j]]=[im[j],im[i]]}}for(let len=2;len<=n;len<<=1){const ang=2*Math.PI/len*(inv?-1:1),wR=Math.cos(ang),wI=Math.sin(ang);for(let i=0;i<n;i+=len){let cR=1,cI=0;for(let j=0;j<(len>>1);j++){const uR=re[i+j],uI=im[i+j],k=i+j+(len>>1),vR=re[k]*cR-im[k]*cI,vI=re[k]*cI+im[k]*cR;re[i+j]=uR+vR;im[i+j]=uI+vI;re[k]=uR-vR;im[k]=uI-vI;const t=cR*wR-cI*wI;cI=cR*wI+cI*wR;cR=t}}}if(inv)for(let i=0;i<n;i++){re[i]/=n;im[i]/=n}}
function fft2(re,im,inv){const tR=new Float64Array(N),tI=new Float64Array(N);for(let y=0;y<N;y++){const o=y*N;for(let x=0;x<N;x++){tR[x]=re[o+x];tI[x]=im[o+x]}fft1(tR,tI,inv);for(let x=0;x<N;x++){re[o+x]=tR[x];im[o+x]=tI[x]}}for(let x=0;x<N;x++){for(let y=0;y<N;y++){tR[y]=re[y*N+x];tI[y]=im[y*N+x]}fft1(tR,tI,inv);for(let y=0;y<N;y++){re[y*N+x]=tR[y];im[y*N+x]=tI[y]}}}
function fsh(a){const o=aN(),h=N>>1;for(let y=0;y<N;y++)for(let x=0;x<N;x++)o[((y+h)%N)*N+(x+h)%N]=a[y*N+x];return o}

function uFilt(a,sz){const o=aN(),r=(sz-1)>>1;for(let y=0;y<N;y++)for(let x=0;x<N;x++){let s=0,c=0;for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){const yy=y+dy,xx=x+dx;if(yy>=0&&yy<N&&xx>=0&&xx<N){s+=a[yy*N+xx];c++}}o[y*N+x]=s/c}return o}
function gFilt(a,sig){const rad=Math.ceil(sig*3),ks=rad*2+1,kn=new Float64Array(ks);let s=0;for(let i=0;i<ks;i++){kn[i]=Math.exp(-((i-rad)**2)/(2*sig*sig));s+=kn[i]}for(let i=0;i<ks;i++)kn[i]/=s;const tmp=aN(),o=aN();for(let y=0;y<N;y++)for(let x=0;x<N;x++){let v=0;for(let dx=-rad;dx<=rad;dx++){const xx=x+dx;if(xx>=0&&xx<N)v+=a[y*N+xx]*kn[dx+rad]}tmp[y*N+x]=v}for(let y=0;y<N;y++)for(let x=0;x<N;x++){let v=0;for(let dy=-rad;dy<=rad;dy++){const yy=y+dy;if(yy>=0&&yy<N)v+=tmp[yy*N+x]*kn[dy+rad]}o[y*N+x]=v}return o}
function hConv(a,ks){if(ks%2===0)ks++;const kn=new Float64Array(ks);let s=0;for(let i=0;i<ks;i++){kn[i]=.5*(1-Math.cos(2*Math.PI*i/(ks-1)));s+=kn[i]}for(let i=0;i<ks;i++)kn[i]/=s;const o=aN(),r=(ks-1)>>1;for(let y=0;y<N;y++)for(let x=0;x<N;x++){let v=0;for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){const yy=y+dy,xx=x+dx;if(yy>=0&&yy<N&&xx>=0&&xx<N)v+=a[yy*N+xx]*kn[dy+r]*kn[dx+r]}o[y*N+x]=v}return o}

// [6] FWHM = 1.92 + 0.031*focus^2, sigma = FWHM/2.355
function wFWHM(f){return 1.92+.031*f*f}
function wSig(f){return wFWHM(f)/2.355}
// Wiener deconvolution (v20 bug fixed)
function wienerDec(img,focus,snr){const sig=wSig(focus),hs=10,o=aN(),psf=aN();let ps=0;for(let y=0;y<=20;y++)for(let x=0;x<=20;x++){const dx=x-hs,dy=y-hs,v=Math.exp(-(dx*dx+dy*dy)/(2*sig*sig)),py=(y+N-hs)%N,px=(x+N-hs)%N;psf[py*N+px]=v;ps+=v}for(let i=0;i<NN;i++)psf[i]/=ps;const pR=aN(),pI=aN(),iR=aN(),iI=aN();pR.set(psf);iR.set(img);fft2(pR,pI,false);fft2(iR,iI,false);const oR=aN(),oI=aN(),inv2=1/(snr*snr);for(let i=0;i<NN;i++){const h2=pR[i]*pR[i]+pI[i]*pI[i],d=h2+inv2;oR[i]=(pR[i]*iR[i]+pI[i]*iI[i])/d;oI[i]=(pR[i]*iI[i]-pI[i]*iR[i])/d}fft2(oR,oI,true);return aCl(oR)}
function qfit(img){return aSd(img)/(aMx(img)+1e-10)<0.1}
function edsr(img){const bl=gFilt(img,.8),o=aN();for(let i=0;i<NN;i++)o[i]=Math.max(0,Math.min(1,img[i]+.3*(img[i]-bl[i])));return o}

// [1][3] rho(r) = rho0 * [sin(kr)/(kr)]^2, r_s = 1/m_fdm, k = pi/r_s
function fdmSol(mf){const rS=1/Math.max(mf,.01),k=Math.PI/Math.max(rS,.1),o=aN(),c=N/2;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=(x-c)/N*5,dy=(y-c)/N*5,r=Math.sqrt(dx*dx+dy*dy),kr=k*r;o[y*N+x]=kr>1e-6?Math.pow(Math.sin(kr)/kr,2):1}return aNm(o)}

// [1][2] L_mix = (eps/2) F_munu F'^munu
function pdpInterf(fringe,omega){const k=fringe/15,o=aN(),c=N/2;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=(x-c)/N*4,dy=(y-c)/N*4,r=Math.sqrt(dx*dx+dy*dy),th=Math.atan2(dy,dx);let p=Math.sin(k*4*Math.PI*r)*.5+Math.sin(k*2*Math.PI*(r+th/(2*Math.PI)))*.5;p=p*(1+omega*.6*Math.sin(k*4*Math.PI*r));p=Math.tanh(p*2);o[y*N+x]=p}const mn=aMx(o),mi=aMn(o);for(let i=0;i<NN;i++)o[i]=(o[i]-mi)/(mn-mi+1e-30);return o}

// [1][3] mixing = eps*B/m_dark
function darkSig(img,eps){const mix=eps*1e15/(1e-9+1e-12),ms=Math.min(mix*1e14,1),o=aN();for(let i=0;i<NN;i++)o[i]=Math.max(0,Math.min(1,img[i]*ms*5));return{sig:o,conf:+(aMx(o)*100).toFixed(1)}}

// [1][3] img*(1-w*0.4) + interf*w*0.5 + soliton*w*0.4
function pdpEnt(img,intf,sol,om){const m=om*.6,o=aN();for(let i=0;i<NN;i++)o[i]=Math.max(0,Math.min(1,img[i]*(1-m*.4)+intf[i]*m*.5+sol[i]*m*.4));return o}

// [2] oscillation_length = 100/(m_dark * 1e9)
function specDual(img,om,fs,ma,dpm){const fR=aN(),fI=aN();fR.set(img);fft2(fR,fI,false);const fsR=fsh(fR),fsI=fsh(fI),L=100/Math.max(dpm*1e9,1e-6),c=N/2,dm=aN(),omF=aN();for(let y=0;y<N;y++)for(let x=0;x<N;x++){const X=(x-c)/c,Y=(y-c)/c,Rv=Math.sqrt(X*X+Y*Y),osc=Math.sin(2*Math.PI*Rv*L/Math.max(fs,.1)),d=ma*Math.exp(-om*Rv*Rv)*Math.abs(osc)*(1-Math.exp(-Rv*Rv/Math.max(fs,.1)));dm[y*N+x]=d;omF[y*N+x]=Math.exp(-Rv*Rv/Math.max(fs,.1))-d}const dR=aN(),dI=aN(),oR=aN(),oI=aN();for(let i=0;i<NN;i++){dR[i]=fsR[i]*dm[i];dI[i]=fsI[i]*dm[i];oR[i]=fsR[i]*omF[i];oI[i]=fsI[i]*omF[i]}const dRs=fsh(dR),dIs=fsh(dI),oRs=fsh(oR),oIs=fsh(oI);fft2(dRs,dIs,true);fft2(oRs,oIs,true);const dk=aN(),or=aN();for(let i=0;i<NN;i++){dk[i]=Math.sqrt(dRs[i]*dRs[i]+dIs[i]*dIs[i]);or[i]=Math.sqrt(oRs[i]*oRs[i]+oIs[i]*oIs[i])}return{ord:aNm(or),dark:aNm(dk)}}

// [2] S = -rho*log(rho) + interference cross-term
function entRes(img,ord,dk,str,ma,fs){let tp=0;for(let i=0;i<NN;i++)tp+=img[i]*img[i];tp+=1e-10;const o=aN();for(let i=0;i<NN;i++){const rho=Math.max(ord[i]*ord[i]/tp,1e-10),S=-rho*Math.log(rho),od=ord[i]+dk[i],xt=(od*od-ord[i]*ord[i]-dk[i]*dk[i])/tp;o[i]=S*str+Math.abs(xt)*ma}return hConv(o,Math.max(3,Math.round(fs)))}

// [2] P_stealth = prior*lhood/(prior*lhood+(1-prior))
function stealthProb(dk,res,eStr){const dmM=aAv(dk)+.1,lm=uFilt(res,5),lmM=aAv(lm)+.1,o=aN();for(let i=0;i<NN;i++){const lh=dk[i]/dmM*lm[i]/lmM,p=eStr*lh/(eStr*lh+(1-eStr)+1e-10);o[i]=Math.max(0,Math.min(1,p))}return gFilt(o,1)}

// [2] R=original, G=residuals, B=dark; gamma=0.45
function pnrm(a){const mn=aMn(a),mx=aMx(a),o=aN();for(let i=0;i<NN;i++)o[i]=Math.sqrt(Math.max(0,(a[i]-mn)/(mx-mn+1e-10)));return o}
function blueHalo(img,dk,res){const rn=pnrm(img),dn=pnrm(dk),en=pnrm(res),lm=uFilt(en,5),eE=aN(),dSm=gFilt(dn,2);for(let i=0;i<NN;i++)eE[i]=Math.max(0,Math.min(1,en[i]*(1+2*Math.abs(en[i]-lm[i]))));const rgb=new Float64Array(NN*3);for(let i=0;i<NN;i++){const b=Math.max(0,Math.min(1,dSm[i]+.3*dn[i]));rgb[i*3]=Math.pow(rn[i],.45);rgb[i*3+1]=Math.pow(eE[i],.45);rgb[i*3+2]=Math.pow(b,.45)}return rgb}

// [4] B=B0(R/r)^3*sqrt(3cos^2th+1), B_crit=4.414e13, P_conv=eps^2*(1-exp(-B^2/m^2*1e-26))
function magFields(b0exp,ma){const B0=Math.pow(10,b0exp),BC=4.414e13,c=N/2,Bn=aN(),Qn=aN(),Cn=aN();let bx=0,qx=0,cx=0;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=(x-c)/(N/4),dy=(y-c)/(N/4),r=Math.sqrt(dx*dx+dy*dy)+.1,th=Math.atan2(dy,dx),Bm=(B0/Math.pow(r,3))*Math.sqrt(3*Math.cos(th)**2+1);if(Bm>bx)bx=Bm;const qd=Math.pow(Bm/BC,2);if(qd>qx)qx=qd;const cv=ma*ma*(1-Math.exp(-Bm*Bm/1e-18*1e-26));if(cv>cx)cx=cv;Bn[y*N+x]=Bm;Qn[y*N+x]=qd;Cn[y*N+x]=cv}for(let i=0;i<NN;i++){Bn[i]/=bx;Qn[i]/=qx;Cn[i]/=cx}return{B:Bn,Q:Qn,C:Cn}}

// [1] Presets — exact profiles from QCAUS/app.py v19
function preCrab(){const r=mkR(1),o=aN(),c=N/2;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=(x-c)/(N*.22),dy=(y-c)/(N*.14),rE=Math.sqrt(dx*dx+dy*dy);let v=Math.exp(-rE*rE/.8)*.7;v+=Math.exp(-(Math.abs(rE-.45))**2/.015)*.4;v+=Math.exp(-((x-c)**2+(y-c)**2)/4)*.9;o[y*N+x]=v+rn(r)*.015}return aNm(o)}
function preSGR(){const r=mkR(2),o=aN(),c=N/2;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=(x-c)/(N/4),dy=(y-c)/(N/4),rv=Math.sqrt(dx*dx+dy*dy)+.05,th=Math.atan2(dy,dx);let h=Math.exp(-rv*1.5)*Math.sqrt(3*Math.cos(th)**2+1)/rv*.5;h+=Math.exp(-((x-c)**2+(y-c)**2)/3);o[y*N+x]=h+rn(r)*.01}return aNm(o)}
function preSwift(){const r=mkR(3),o=aN(),c=N/2;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const rv=Math.sqrt((x-c)**2+(y-c)**2);o[y*N+x]=Math.exp(-rv*rv/6)+Math.exp(-rv/40)*.2+rn(r)*.008}return aNm(o)}
function preGal(){const r=mkR(4),o=aN(),c=N/2,b4=7.669;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=(x-c)/(N*.15),dy=(y-c)/(N*.1),rE=Math.sqrt(dx*dx+dy*dy);o[y*N+x]=Math.exp(-b4*(Math.pow(rE,.25)-1))+rn(r)*.012}return aNm(o)}
function preMag(){return magFields(15,.1).B}
const PRES={crab:preCrab,sgr:preSGR,swift:preSwift,galaxy:preGal,magnetar:preMag};

function rMap(id,data,lut,title,met,leg,skp){const cv=document.getElementById(id),ctx=cv.getContext('2d'),w=cv.width,h=cv.height,im=ctx.createImageData(w,h),px=im.data,sx=w/N,sy=h/N;for(let py=0;py<h;py++)for(let ppx=0;ppx<w;ppx++){const ix=Math.min(N-1,ppx/sx|0),iy=Math.min(N-1,py/sy|0),v=Math.max(0,Math.min(255,data[iy*N+ix]*255|0)),o=(py*w+ppx)*4;px[o]=lut[v*3];px[o+1]=lut[v*3+1];px[o+2]=lut[v*3+2];px[o+3]=255}ctx.putImageData(im,0,0);const fs=Math.max(9,w/42|0);ctx.fillStyle='rgba(0,0,0,.78)';ctx.fillRect(0,0,w,fs+14);ctx.font=`bold ${fs}px JetBrains Mono`;ctx.fillStyle='#fff';ctx.textBaseline='middle';ctx.textAlign='left';ctx.fillText(title,8,fs/2+7);const mt=Object.entries(met).slice(0,3).map(([k,v])=>`${k}: ${v}`).join('  '),tw=ctx.measureText(mt).width+16,mx=w-tw-8;ctx.fillStyle='rgba(0,0,0,.82)';ctx.strokeStyle='rgba(0,255,140,.7)';ctx.lineWidth=1.5;ctx.fillRect(mx,4,tw,fs+8);ctx.strokeRect(mx,4,tw,fs+8);ctx.fillStyle='#00ff8c';ctx.font=`${Math.max(8,fs-2)}px JetBrains Mono`;ctx.fillText(mt,mx+8,fs/2+8);if(skp){const bpx=w*.2|0,bkpc=(bpx/N)*skp;ctx.strokeStyle='rgba(255,255,255,.7)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(14,h-28);ctx.lineTo(14+bpx,h-28);ctx.stroke();ctx.fillStyle='rgba(255,255,255,.7)';ctx.font=`${Math.max(8,fs-3)}px JetBrains Mono`;ctx.textAlign='left';ctx.fillText(`${bkpc.toFixed(1)} kpc`,16,h-14)}if(leg){let ly=h-14-leg.length*15;ctx.font=`${Math.max(8,fs-3)}px JetBrains Mono`;leg.forEach(([c,l])=>{ctx.fillStyle=c;ctx.fillRect(w-175,ly,12,11);ctx.fillStyle='#fff';ctx.fillText(l,w-158,ly+9);ly+=15})}ctx.fillStyle='rgba(150,150,150,.5)';ctx.font=`${Math.max(7,fs-4)}px JetBrains Mono`;ctx.textAlign='right';ctx.fillText(`QCAUS v21.0 | ${new Date().toISOString().slice(0,16)}Z`,w-6,h-3);ctx.textAlign='left';ctx.textBaseline='alphabetic'}

function rRGB(id,rgb,title,met,skp){const cv=document.getElementById(id),ctx=cv.getContext('2d'),w=cv.width,h=cv.height,im=ctx.createImageData(w,h),px=im.data,sx=w/N,sy=h/N;for(let py=0;py<h;py++)for(let ppx=0;ppx<w;ppx++){const ix=Math.min(N-1,ppx/sx|0),iy=Math.min(N-1,py/sy|0),o=(py*w+ppx)*4;px[o]=Math.max(0,Math.min(255,rgb[iy*N+ix]*3*255|0));px[o+1]=Math.max(0,Math.min(255,rgb[iy*N+ix]*3+1*255|0));px[o+2]=Math.max(0,Math.min(255,rgb[iy*N+ix]*3+2*255|0));px[o+3]=255}ctx.putImageData(im,0,0);const fs=Math.max(9,w/42|0);ctx.fillStyle='rgba(0,0,0,.78)';ctx.fillRect(0,0,w,fs+14);ctx.font=`bold ${fs}px JetBrains Mono`;ctx.fillStyle='#fff';ctx.textBaseline='middle';ctx.textAlign='left';ctx.fillText(title,8,fs/2+7);const mt=Object.entries(met).slice(0,3).map(([k,v])=>`${k}: ${v}`).join('  '),tw=ctx.measureText(mt).width+16,mx=w-tw-8;ctx.fillStyle='rgba(0,0,0,.82)';ctx.strokeStyle='rgba(0,255,140,.7)';ctx.lineWidth=1.5;ctx.fillRect(mx,4,tw,fs+8);ctx.strokeRect(mx,4,tw,fs+8);ctx.fillStyle='#00ff8c';ctx.font=`${Math.max(8,fs-2)}px JetBrains Mono`;ctx.fillText(mt,mx+8,fs/2+8);if(skp){const bpx=w*.2|0,bkpc=(bpx/N)*skp;ctx.strokeStyle='rgba(255,255,255,.7)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(14,h-28);ctx.lineTo(14+bpx,h-28);ctx.stroke();ctx.fillStyle='rgba(255,255,255,.7)';ctx.font=`${Math.max(8,fs-3)}px JetBrains Mono`;ctx.fillText(`${bkpc.toFixed(1)} kpc`,16,h-14)}ctx.fillStyle='rgba(150,150,150,.5)';ctx.font=`${Math.max(7,fs-4)}px JetBrains Mono`;ctx.textAlign='right';ctx.fillText(`QCAUS v21.0 | ${new Date().toISOString().slice(0,16)}Z`,w-6,h-3);ctx.textAlign='left';ctx.textBaseline='alphabetic'}

function drawLine(ctx,pts){if(pts.length<2)return;ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length-1;i++){const cx2=(pts[i][0]+pts[i+1][0])/2,cy2=(pts[i][1]+pts[i+1][1])/2;ctx.quadraticCurveTo(pts[i][0],pts[i][1],cx2,cy2)}ctx.lineTo(pts[pts.length-1][0],pts[pts.length-1][1])}
function chart(id,{xs,lines,xL,yL,title,logX,logY,vlines}){const cv=document.getElementById(id),ctx=cv.getContext('2d'),w=cv.width,h=cv.height,p={t:32,r:16,b:30,l:50},pw=w-p.l-p.r,ph=h-p.t-p.b;ctx.fillStyle='#0a0b10';ctx.fillRect(0,0,w,h);ctx.strokeStyle='rgba(255,255,255,.05)';ctx.lineWidth=.5;for(let i=0;i<=5;i++){const y=p.t+ph*i/5;ctx.beginPath();ctx.moveTo(p.l,y);ctx.lineTo(w-p.r,y);ctx.stroke();const x=p.l+pw*i/5;ctx.beginPath();ctx.moveTo(x,p.t);ctx.lineTo(x,h-p.b);ctx.stroke()}let xMn=xs[0],xMx=xs[xs.length-1],yMn=1e30,yMx=-1e30;lines.forEach(l=>l.data.forEach(v=>{if(v<yMn)yMn=v;if(v>yMx)yMx=v}));if(logX){xMn=Math.log10(xMn);xMx=Math.log10(xMx)}if(logY){yMn=Math.log10(Math.max(yMn,1e-30));yMx=Math.log10(yMx)}const yMnR=yMn,yMxR=yMx;function ppx(xv){return logX?p.l+pw*(Math.log10(xv)-xMn)/(xMx-xMn):p.l+pw*(xv-xs[0])/(xs[xs.length-1]-xs[0])}function ppy(yv){const yv2=logY?Math.log10(Math.max(yv,1e-30)):yv;return p.t+ph*(1-(yv2-yMn)/(yMx-yMn))}ctx.fillStyle='rgba(255,255,255,.7)';ctx.font='bold 10px JetBrains Mono';ctx.textAlign='center';ctx.fillText(title,w/2,16);ctx.fillStyle='rgba(255,255,255,.4)';ctx.font='9px JetBrains Mono';ctx.textAlign='center';ctx.fillText(xL,p.l+pw/2,h-5);ctx.save();ctx.translate(10,p.t+ph/2);ctx.rotate(-Math.PI/2);ctx.fillText(yL,0,0);ctx.restore();ctx.font='7px JetBrains Mono';ctx.fillStyle='rgba(255,255,255,.3)';ctx.textAlign='right';ctx.textBaseline='middle';for(let i=0;i<=5;i++){const y=p.t+ph*(5-i)/5,v=logY?Math.pow(10,yMn+(yMx-yMn)*i/5):yMnR+(yMxR-yMnR)*i/5;ctx.fillText(logY?v.toExponential(0):v.toFixed(2),p.l-3,y)}ctx.textAlign='center';ctx.textBaseline='top';for(let i=0;i<=5;i++){const x=p.l+pw*i/5,v=logX?Math.pow(10,xMn+(xMx-xMn)*i/5):xs[0]+(xs[xs.length-1]-xs[0])*i/5;ctx.fillText(logX?v.toExponential(0):v.toFixed(2),x,h-p.b+3)}lines.forEach((l,li)=>{ctx.strokeStyle=l.color;ctx.lineWidth=1.8;ctx.setLineDash(l.dash||[]);const pts=xs.map((x,i)=>[ppx(x),ppy(l.data[i])]);drawLine(ctx,pts);ctx.stroke();ctx.setLineDash([]);if(l.label){const lx=p.l+8+li*170;ctx.fillStyle='rgba(0,0,0,.6)';ctx.fillRect(lx,p.t+2,ctx.measureText(l.label).width+20,13);ctx.strokeStyle=l.color;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(lx+2,p.t+9);ctx.lineTo(lx+14,p.t+9);ctx.stroke();ctx.fillStyle='rgba(255,255,255,.65)';ctx.font='8px JetBrains Mono';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(l.label,lx+17,p.t+9)}});if(vlines)vlines.forEach(vl=>{const x=ppx(vl.x);ctx.strokeStyle=vl.color||'#ff6b35';ctx.lineWidth=1;ctx.setLineDash([4,4]);ctx.beginPath();ctx.moveTo(x,p.t);ctx.lineTo(x,h-p.b);ctx.stroke();ctx.setLineDash([]);if(vl.label){ctx.fillStyle=vl.color||'#ff6b35';ctx.font='8px JetBrains Mono';ctx.textAlign='center';ctx.fillText(vl.label,x,p.t-1)}});ctx.textAlign='left';ctx.textBaseline='alphabetic'}

let bCV,aCV;
function initComp(){bCV=document.createElement('canvas');bCV.width=1024;bCV.height=465;aCV=document.createElement('canvas');aCV.width=1024;aCV.height=465}
function rComp(){const w=1024,h=465,sx=w/N,sy=h/N;let ctx=bCV.getContext('2d');ctx.fillStyle='#0a0b10';ctx.fillRect(0,0,w,h);const bI=ctx.createImageData(w,h),bP=bI.data;for(let py=0;py<h;py++)for(let
