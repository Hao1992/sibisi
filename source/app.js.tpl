const T=__T__;
const LBL=__LBL__;
const ALGN=__ALGN__;
const TASTE=__TASTE__;
const S=__S__;
const FIRST=__FIRST__;
const EXTRAS=__EXTRAS__;
const DR=__DR__;
const SIDE=__SIDE__;
const DRK=__DRK__;
const PR=__PR__;
const DET=__DET__;
const CT=__CT__;
const SP=__SP__;
const CORI=__CORI__;
const DRKMAP=__DRKMAP__;
const UPSELL=__UPSELL__;
const TEL=__TEL__;
const MAP=__MAP__;
const REV=__REV__;
const TOP=__TOP__;
const FRONT=__FRONT__;
const GRP=__GRP__;
const COMBO=__COMBO__;
const POT=c=>c.slice(0,2)==="1-";
const LI={zh:0,es:1,en:2};
const eur=(n,l)=>l==="en"?"€"+n.toFixed(2):n.toFixed(2).replace(".",",")+" €";
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=id=>document.getElementById(id);
let L="es";
const nm=a=>a[LI[L]];
// Allergen icons: colored disc + white pictogram, name always shown.
const ALG={
 G:{c:"#c9772b",p:'<path d="M12 6v13" /><path d="M12 9c-2-1-3-3-3-4 2 0 3 2 3 4zM12 9c2-1 3-3 3-4-2 0-3 2-3 4zM12 13c-2-1-3-3-3-4 2 0 3 2 3 4zM12 13c2-1 3-3 3-4-2 0-3 2-3 4z"/>'},
 H:{c:"#e0a21b",p:'<ellipse cx="12" cy="12.5" rx="4.2" ry="5.5"/>'},
 S:{c:"#4f8a3c",p:'<path d="M7 16c-1-4 3-9 9-9 1 4-3 9-9 9z"/><circle cx="10" cy="13" r="1.1"/><circle cx="13" cy="10.5" r="1.1"/>'},
 "Sé":{c:"#9a7a55",p:'<path d="M8 9c0-2 1-3 1.5-3S11 7 11 9s-.7 3-1.5 3S8 11 8 9zM13 9c0-2 1-3 1.5-3S16 7 16 9s-.7 3-1.5 3S13 11 13 9zM10.5 15c0-2 1-3 1.5-3s1.5 1 1.5 3-.7 3-1.5 3-1.5-1-1.5-3z"/>'},
 P:{c:"#3b7fb5",p:'<path d="M4.5 12c3-4 8.5-4 11.5 0-3 4-8.5 4-11.5 0z"/><path d="M16 12l3.5-3v6z"/>'},
 M:{c:"#7d5aa6",p:'<path d="M5.5 12.5a6.5 5.5 0 0 1 13 0z"/><path d="M10 12.5v5h4v-5"/>'}
};
const algIcon=k=>{const a=ALG[k];return `<span class="ai"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="${a.c}"/><g fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round">${a.p}</g></svg>${nm(ALGN[k])}</span>`};
const algRow=(s,lab)=>{const k=s.split(" ").filter(Boolean);return k.length?`<div class="alg">${lab?`<span class="alab">${T[L].algL}</span>`:""}${k.map(algIcon).join("")}</div>`:""};
__ILLO__
/* ---------- 筛选：素食 / 不辣 / 避开某个过敏原 ---------- */
const fls=d=>(d.fl||"").split(" ");
const als=d=>(d.al||"").split(" ");
const woLab=(k,l)=>{const n=ALGN[k][LI[l]];return T[l].fWo.replace("%s",l==="zh"?n:n.toLowerCase())};
const FILD=[
 {id:"v",  lab:l=>T[l].veg, ok:d=>fls(d).includes("v")||fls(d).includes("vg")},
 {id:"nh", lab:l=>T[l].fNo, ok:d=>!fls(d).includes("h")},
 {id:"H",  lab:l=>woLab("H",l),  ok:d=>!als(d).includes("H")},
 {id:"Se", lab:l=>woLab("Sé",l), ok:d=>!als(d).includes("Sé")},
 {id:"M",  lab:l=>woLab("M",l),  ok:d=>!als(d).includes("M")}];
let FIL=[];
const dishOk=d=>FIL.every(id=>FILD.find(f=>f.id===id).ok(d));
function renderFil(){
  const t=T[L],n=S.reduce((a,sec)=>a+sec.d.filter(dishOk).length,0);
  $("filters").innerHTML=`<span class="qlab">${esc(t.fT)}</span>`
    +FILD.map(f=>`<button class="chip" type="button" data-fil="${f.id}" aria-pressed="${FIL.includes(f.id)}">${esc(f.lab(L))}</button>`).join("")
    +(FIL.length?`<span class="fcount">${esc(t.fCount.replace("%s",n))}</span><button class="chip clr" type="button" data-fil="*">${esc(t.fClear)}</button>`:"");
}
function findDish(c){let r=null;S.forEach(s=>s.d.forEach(x=>{if(x.c===c)r=x}));return r}
function pairLine(d){const p=PR[d.c];if(!p)return "";const t=T[L];const sd=SIDE[p[0]];const d1=DRK[p[1][0]],d2=DRK[p[1][1]];
 const lo=Math.min(d1[1],d2[1]),hi=Math.max(d1[1],d2[1]);const pr=lo===hi?eur(lo,L):eur(lo,L)+"–"+eur(hi,L);
 return `<div class="pairl"><b>${t.pairWith}</b> ${esc(nm(sd[0]))} <span class="plus">+${eur(sd[1],L)}</span> · ${esc(nm(d1[0]))} ${t.orw} ${esc(nm(d2[0]))} <span class="plus">+${pr}</span></div>`}
let PICK={};                       // 每道主食的套餐选择：{sd:小菜, dr:饮料}
// 可选小菜：凉菜炒饭那一区（辣白菜分小/大）+ 水煮蛋
function sideOpts(){
  const out=[];
  for(const sec of S)for(const d of sec.d){
    if(d.c==="2-11")out.push({k:d.c,c:d.c,sz:"",p:d.p});
    else if(sec.id==="frios"){
      if(d.p2){out.push({k:d.c+"|s",c:d.c,sz:"s",p:d.p});out.push({k:d.c+"|l",c:d.c,sz:"l",p:d.p2})}
      else out.push({k:d.c,c:d.c,sz:"",p:d.p})}}
  return out}
const drinkOpts=g=>DR[g].map((x,i)=>({k:`dr-${g}-${i}`,dr:`dr-${g}-${i}`,dv:"",p:x[1],n:l=>drName(x,l)}));
const sideName=o=>{const d=findDish(o.c);let n=L==="zh"?d.zh:d[L];
  if(o.sz)n+=L==="zh"?"（"+SZ.zh[o.sz]+"）":" ("+SZ[L][o.sz]+")";return n};
const pickName=o=>o.dr?(o.dv?DRK[o.dv][0][LI[L]]:drName(DRINK[o.dr],L)):sideName(o);
const pickPrice=o=>o.p!=null?o.p:(o.dr?(o.dv?DRK[o.dv][1]:DRINK[o.dr][1]):(o.sz==="l"?findDish(o.c).p2:findDish(o.c).p));
function pairBox(d){
  const p=PR[d.c];if(!p)return "";
  const t=T[L],ct=CT[L],sc=p[0].replace("s",""),ss=p[0].endsWith("s")?"s":"";
  const recSide={k:ss?sc+"|"+ss:sc,c:sc,sz:ss};
  const recDr=[p[1][0],p[1][1]].map(k=>({k:DRKMAP[k]+"|"+k,dr:DRKMAP[k],dv:k}));
  const cur=PICK[d.c]||(PICK[d.c]={sd:{[recSide.k]:{o:recSide,q:1}},dr:{}});   // 小菜默认跟推荐，饮料留空
  const line=(kind,e)=>`<li><span>${esc(pickName(e.o))}</span><span>+${eur(pickPrice(e.o),L)}</span>
     <span class="qty has"><button class="qbtn" type="button" data-cq="${kind};${d.c};${e.o.k};-1" aria-label="−">−</button><span class="qn">${e.q}</span><button class="qbtn add" type="button" data-cq="${kind};${d.c};${e.o.k};1" aria-label="＋">＋</button></span></li>`;
  const quick=(kind,o)=>cur[kind][o.k]?"":`<button class="chip" type="button" data-cq="${kind};${d.c};${o.k};1">${esc(pickName(o))} +${eur(pickPrice(o),L)}</button>`;
  const group=(kind,label,recs)=>{
    const es=Object.values(cur[kind]);
    return `<div class="grp"><span class="qlab">${esc(label)}</span>
      ${es.length?`<ul class="glist">${es.map(e=>line(kind,e)).join("")}</ul>`:""}
      <div class="opt">${recs.map(o=>quick(kind,o)).join("")}<button class="chip more" type="button" data-more="${kind}|${d.c}">${esc(kind==="sd"?ct.otherSide:ct.otherDrink)}</button></div></div>`};
  const sum=k=>Object.values(cur[k]).reduce((n,e)=>n+e.q*pickPrice(e.o),0);
  const tot=d.p+sum("sd")+sum("dr");
  return `<div class="pair"><dt>${t.pairT}</dt><p>${esc(p[3+LI[L]])}</p>
   <ul class="glist"><li><span>${d.c} ${esc(L==="zh"?d.zh:d[L])}</span><span>${eur(d.p,L)}</span>${stepper(d.c,`data-c="${d.c}"`)}</li></ul>
   ${group("sd",ct.sideL,[recSide])}
   ${group("dr",ct.drinkPick,recDr)}
   <div class="pairtot"><span>${t.total}</span><b>${eur(tot,L)}</b></div>
   <button class="obtn combo" type="button" data-combo="${d.c}">${esc(ct.combo)}</button>
   <small>${t.pairNote}</small></div>`}
function optByKey(kind,k){
  if(kind==="sd")return sideOpts().find(o=>o.k===k);
  const[dr,dv]=k.split("|");return {k:k,dr:dr,dv:dv||""}}
function bumpPick(kind,c,k,n){
  const cur=PICK[c]||(PICK[c]={sd:{},dr:{}});
  const e=cur[kind][k]||(cur[kind][k]={o:optByKey(kind,k),q:0});
  e.q=Math.max(0,Math.min(20,e.q+n));
  if(!e.q)delete cur[kind][k];
  if($("detpair"))$("detpair").innerHTML=pairBox(findDish(c));
  if(!$("pick").hidden)pickCounts(kind,c)}
function pickCounts(kind,c){
  const cur=(PICK[c]||{})[kind]||{};
  $("pick").querySelectorAll("[data-cq]").forEach(b=>{
    const parts=b.dataset.cq.split(";"),k=parts[2],e=cur[k];
    b.setAttribute("aria-pressed",!!e);
    const s=b.querySelector(".pcount");if(s)s.textContent=e?"×"+e.q:""})}
// 「加小菜 / 加饮料」：全屏列表，点一下加一份，可以连着加
function openPick(kind,c){
  const ct=CT[L],t=T[L];
  const row=o=>`<li><button type="button" data-cq="${kind};${c};${o.k};1"><span>${esc(pickName(o))}</span><b>${eur(pickPrice(o),L)}</b><span class="pcount"></span></button></li>`;
  const body=kind==="sd"
    ?`<ul class="picklist">${sideOpts().map(row).join("")}</ul>`
    :["beers","wine","soft","water"].map(g=>`<h5>${esc(t[g])}</h5><ul class="picklist">${drinkOpts(g).map(row).join("")}</ul>`).join("");
  $("pick").innerHTML=`<div class="pickhead"><h3>${esc(kind==="sd"?ct.pickSide:ct.pickDrink)}</h3>
     <button class="xbtn" type="button" id="pclose" aria-label="${esc(t.close)}">×</button></div>
    <div class="pickbody">${body}</div>
    <div class="pickfoot"><button class="obtn" type="button" id="pdone">${esc(ct.pickDone)}</button></div>`;
  $("pick").hidden=false;document.body.style.overflow="hidden";
  pickCounts(kind,c);
  $("pclose").onclick=closePick;$("pdone").onclick=closePick;$("pclose").focus()}
function closePick(){$("pick").hidden=true;document.body.style.overflow=$("sheet").hidden&&$("order").hidden?"":"hidden"}
function render(){
  const t=T[L]; document.documentElement.lang=L==="zh"?"zh-CN":L;
  $("tagline").textContent=t.tagline; $("h-eye").textContent=t.eye; $("h-title").textContent=t.title;
  $("h-desc").textContent=t.desc; $("h-from").textContent=t.frm;
  $("steps").innerHTML=t.steps.map(s=>`<li>${esc(s)}</li>`).join("");
  $("first-t").textContent=t.firstT;
  $("first").innerHTML=FIRST.map(f=>{const d=findDish(f.c),det=DET[f.c]?` data-det="${f.c}" tabindex="0" role="button"`:"";
    return `<li${det}><div class="thumb">${d.img?`<img src="img/${d.img}.jpg" alt="" loading="lazy">`:illo(d.c,"")}<span class="badge">${d.c}</span></div>
      <div class="ft"><h4>${esc(L==="zh"?d.zh:d[L])}</h4><em>${esc(f[L])}</em></div>
      <div class="fr"><b>${eur(d.p,L)}</b>${stepper(d.c,`data-c="${d.c}"`)}</div></li>`}).join("");
  $("herobuy").innerHTML=`<span class="qlab">1-1 ${esc(L==="zh"?findDish("1-1").zh:findDish("1-1")[L])}</span>${stepper("1-1",'data-c="1-1"')}`;
  renderPacks();
  $("promise").innerHTML=`<b>${esc(t.promiseT)}</b><ul>${t.promise.map(([ic,x])=>`<li><span>${ic}</span>${esc(x)}</li>`).join("")}</ul>`;
  $("f-take").textContent=t.take; $("copy").textContent=t.copy;
  $("phone").href="tel:"+TEL;
  $("f-dirs").textContent=t.dirs; $("f-dirs").href=MAP;
  $("f-rev").textContent=t.rev;   $("f-rev").href=REV;
  $("f-all").innerHTML=algRow("G H S Sé P M",true)+`<div style="margin-top:6px">${esc(t.all)}</div>`;
  document.querySelectorAll(".lang button").forEach(b=>b.setAttribute("aria-pressed",b.dataset.l===L));
  const secName=s=>L==="zh"?s.zh:s[L];
  renderFil();
  const SS=S.map(s=>Object.assign({},s,{d:s.d.filter(dishOk)})).filter(s=>s.d.length);
  $("rail").innerHTML=SS.map(s=>`<a href="#${s.id}" data-s="${s.id}">${esc(secName(s))}</a>`).join("")+`<a href="#bebidas" data-s="bebidas">${t.drinks}</a>`;
  let h=SS.length?"":`<p class="fempty">${esc(t.fEmpty)}</p>`;
  for(const s of SS){
    h+=`<section id="${s.id}"><div class="sh"><h3>${esc(secName(s))}</h3>${L==="zh"?"":`<span class="zh">${s.zh}</span>`}</div><p class="note">${esc(s.note[L])}</p><div class="list">`;
    for(const d of s.d){
      const name=L==="zh"?d.zh:d[L];
      const sub=L==="zh"?d.es:L==="en"?d.zh+" · "+d.es:d.zh;
      const desc=L==="en"?d.en2:L==="es"?d.es2:"";
      const f=(d.fl||"").split(" ");
      let tags="";
      if(TOP.includes(d.c))tags+=`<span class="tag top">★ ${t.top}</span>`;
      if(f.includes("vg"))tags+=`<span class="tag veg">${t.vegan}</span>`;
      else if(f.includes("v"))tags+=`<span class="tag veg">${t.veg}</span>`;
      const taste=d.ta.map(k=>{const hot=k==="picante"||k==="mala";return `<span class="tt${hot?" hotx":""}">${hot?"🌶 ":""}${esc(nm(TASTE[k]))}</span>`}).join("");
      const det=DET[d.c]?` data-det="${d.c}" tabindex="0" role="button"`:"";
      const qty=d.p2
        ?`<div class="qty2"><span class="qlab">${SZ[L].s}</span>${stepper(d.c+"|s",`data-c="${d.c}" data-sz="s"`)}</div>
           <div class="qty2"><span class="qlab">${SZ[L].l}</span>${stepper(d.c+"|l",`data-c="${d.c}" data-sz="l"`)}</div>`
        :stepper(d.c,`data-c="${d.c}"`);
      const price=d.p2?`<span class="pz">${L==="zh"?"小":L==="en"?"S":"P"}</span> ${eur(d.p,L)}<br><span class="pz">${L==="zh"?"大":L==="en"?"L":"G"}</span> ${eur(d.p2,L)}`:eur(d.p,L);
      h+=`<div class="dish" id="d-${d.c}"${det}><div class="thumb">${d.img?`<img src="img/${d.img}.jpg" alt="" loading="lazy">`:illo(d.c,"")}<span class="badge">${d.c}</span></div>
        <div class="t"><h4>${esc(name)}</h4><div class="zhn">${esc(sub)}</div>${desc?`<p>${esc(desc)}</p>`:""}${taste?`<div class="taste">${taste}</div>`:""}${tags?`<div class="tags">${tags}</div>`:""}${algRow(d.al,true)}${pairLine(d)}${DET[d.c]?`<span class="more">${t.more}</span>`:""}<div class="qwrap">${qty}</div></div>
        <div class="price">${price}</div></div>`;
    }
    h+=`</div>`;
    if(s.id==="hm")h+=`<div class="extras"><b>${t.extras}</b><ul>${EXTRAS.map(e=>`<li><span>${esc(nm(e[0]))}</span><span>+${eur(e[1],L)}</span></li>`).join("")}</ul></div>`;
    h+=`</section>`;
  }
  h+=`<section id="bebidas"><div class="sh"><h3>${t.drinks}</h3>${L==="zh"?"":'<span class="zh">酒水</span>'}</div><div class="drinks">`;
  for(const k of ["beers","wine","soft","water"])h+=`<div><h5>${t[k]}</h5><ul>${DR[k].map((x,i)=>{const id=`dr-${k}-${i}`;return `<li><span>${esc(drName(x,L))}</span><span class="dr-r">${eur(x[1],L)}${stepper(id,`data-dr="${id}"`)}</span></li>`}).join("")}</ul></div>`;
  h+=`</div></section>`;
  $("menu").innerHTML=h;
  syncCart();
  spy();
}
/* ---------- 多人组合：固定搭配，一个按钮加全 ---------- */
const packOpt=k=>k.indexOf("dr-")===0
  ?{k:k,dr:k.split("|")[0],dv:k.split("|")[1]||""}
  :{k:k,c:k.split("|")[0],sz:k.split("|")[1]||""};
const packTotal=p=>p.items.reduce((n,[k,q])=>n+q*pickPrice(packOpt(k)),0);
function renderPacks(){
  const t=T[L];
  $("packs").innerHTML=`<b>${esc(t.packT)}</b>`+COMBO.map(p=>{
    const tot=packTotal(p);
    return `<div class="pk"><div class="pkh"><b>${esc(p[L])}</b></div>
      <p>${esc(p[L+"2"])}</p>
      <ul>${p.items.map(([k,q])=>{const o=packOpt(k);
        return `<li><span>${esc(pickName(o))}</span><span>×${q}</span></li>`}).join("")}</ul>
      <div class="pkf"><div class="pkp"><b>${eur(tot,L)}</b><em>${esc(t.packEach.replace("%s",eur(tot/p.n,L)))}</em></div>
        <button class="obtn" type="button" data-pack="${p.id}">${esc(t.packAdd)}</button></div></div>`}).join("")
    +`<small>${esc(t.packNote)}</small>`;
}
function openDet(c){
  const d=findDish(c);if(!d||!DET[c])return;const t=T[L],lb=LBL[L],x=DET[c][L];
  const rows=["what","story","ing","taste","adj","how","note","who"].filter(k=>x[k]).map(k=>{
    const v=k==="adj"?t.adj:(k==="how"&&x.how==="POT"?t.pot:x[k]);return `<div><dt>${lb[k]}</dt><dd>${esc(v)}</dd></div>`}).join("");
  const price=d.p2?`${eur(d.p,L)} / ${eur(d.p2,L)}`:eur(d.p,L);
  const sh=$("sheet");
  sh.innerHTML=`<button class="close" id="close" aria-label="${t.close}">×</button>${d.img?`<img src="img/${d.img}.jpg" alt="">`:`<div class="ph">${illo(d.c,t.illo)}</div>`}
   <div class="in"><h3>${esc(L==="zh"?d.zh:d[L])}</h3><div class="meta"><span>${d.c} · ${esc(L==="zh"?d.es:d.zh)}</span><b>${price}</b></div>
   <div id="detbuy">${buyBlock(c)}</div>
   <div class="algbox"><dt>${lb.alg}</dt>${algRow(d.al)}</div>
   <dl>${rows}</dl><div id="detpair">${pairBox(d)}</div></div>`;
  DETC=c;sh.hidden=false;$("scrim").hidden=false;document.body.classList.add("detailing");
  document.body.style.overflow="hidden";$("close").focus();
  $("close").onclick=closeDet;
}
function closeDet(){DETC=null;$("sheet").hidden=true;$("scrim").hidden=true;
  document.body.classList.remove("detailing");document.body.style.overflow=""}
document.addEventListener("click",e=>{
  const q=e.target.closest("[data-q]");
  if(q){e.preventDefault();const f=+q.dataset.q>0?flyFrom(q):null;
    cartBump(q.dataset.k,+q.dataset.q,q.dataset);flyToCart(f);
    return}
  const cb=e.target.closest("[data-combo]");
  if(cb){e.preventDefault();
    const c=cb.dataset.combo,sel=PICK[c]||{sd:{},dr:{}},f=flyFrom(cb);
    cartBump(c,1,{c:c});
    for(const e of Object.values(sel.sd||{}))cartBump(e.o.k,e.q,{c:e.o.c,sz:e.o.sz});
    for(const e of Object.values(sel.dr||{}))cartBump(e.o.k,e.q,{dr:e.o.dr,dv:e.o.dv});
    flyToCart(f);
    return}
  const fb=e.target.closest("[data-fil]");
  if(fb){e.preventDefault();const id=fb.dataset.fil;
    FIL=id==="*"?[]:FIL.includes(id)?FIL.filter(x=>x!==id):FIL.concat(id);
    render();
    if(FIL.length)$("filters").scrollIntoView({block:"start",behavior:"smooth"});
    return}
  const pk=e.target.closest("[data-pack]");
  if(pk){e.preventDefault();const p=COMBO.find(x=>x.id===pk.dataset.pack),f=flyFrom(pk);
    for(const[k,q]of p.items){const o=packOpt(k);
      cartBump(k,q,o.dr?{dr:o.dr,dv:o.dv}:{c:o.c,sz:o.sz})}
    flyToCart(f);return}
  const oe=e.target.closest("[data-oedit]");
  if(oe){e.preventDefault();const c=oe.dataset.oedit;OEDIT[c]=!OEDIT[c];renderOrder();return}
  const mo=e.target.closest("[data-more]");
  if(mo){e.preventDefault();const[kind,c]=mo.dataset.more.split("|");openPick(kind,c);return}
  const cq=e.target.closest("[data-cq]");
  if(cq){e.preventDefault();const[kind,c,k,n]=cq.dataset.cq.split(";");
    const f=+n>0&&!$("pick").hidden?flyFrom(cq):null;
    bumpPick(kind,c,k,+n);flyToCart(f);return}
  const op=e.target.closest("[data-opt]");
  if(op){e.preventDefault();const[kind,c,i]=op.dataset.opt.split("|");setOpt(kind,c,+i);return}
  const r=e.target.closest("[data-det]");if(r)openDet(r.dataset.det);
  else if(e.target.id==="scrim"){closeDet();closeOrder()}
});
document.addEventListener("keydown",e=>{
  if(e.key==="Escape"){if(!$("pick").hidden)closePick();else if(!$("staff").hidden)closeStaff();else if(!$("order").hidden)closeOrder();else closeDet()}
  if(e.target.closest&&e.target.closest("[data-q],[data-opt]"))return;
  const r=e.target.closest&&e.target.closest("[data-det]");
  if(r&&(e.key==="Enter"||e.key===" ")){e.preventDefault();openDet(r.dataset.det)}
});
function setLang(l){L=l;store.set("lang",l);render()}
document.querySelectorAll(".lang button").forEach(b=>b.addEventListener("click",()=>setLang(b.dataset.l)));
$("copy").addEventListener("click",e=>{
  const b=e.currentTarget;const sel=()=>getSelection().selectAllChildren($("phone"));
  const done=()=>{b.textContent=T[L].copied;setTimeout(()=>b.textContent=T[L].copy,1500)};
  try{navigator.clipboard.writeText("+34671343226").then(done,sel)}catch(_){sel()}
});
let obs;
function spy(){
  if(obs)obs.disconnect();
  if(!("IntersectionObserver" in window))return;
  obs=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){document.querySelectorAll(".rail a").forEach(a=>{const on=a.dataset.s===en.target.id;a.classList.toggle("on",on);if(on){a.parentNode.scrollLeft=a.offsetLeft-16}})}})},{rootMargin:"-30% 0px -60% 0px"});
  document.querySelectorAll("main section").forEach(s=>obs.observe(s));
}
/* ---------- 点单（购物车）：状态在本机，不发给任何服务器 ---------- */
const SZ={zh:{s:"小",l:"大"},es:{s:"P",l:"G"},en:{s:"S",l:"L"}};
const DRINK={};
for(const g of ["beers","wine","soft","water"])DR[g].forEach((x,i)=>{DRINK["dr-"+g+"-"+i]=x});
const drName=(x,l)=>typeof x[0]==="string"?x[0]:x[0][LI[l]];
const CKEY="sibisi.cart";
const store={
  get(k){for(const s of [localStorage,sessionStorage]){try{const v=s.getItem(k);if(v)return v}catch(e){}}return null},
  set(k,v){for(const s of [localStorage,sessionStorage]){try{s.setItem(k,v)}catch(e){}}},
  del(k){for(const s of [localStorage,sessionStorage]){try{s.removeItem(k)}catch(e){}}}};
let CART={},OPT={},DETC=null;
function cartSave(){store.set(CKEY,JSON.stringify({t:Date.now(),c:CART,o:OPT}))}
(function(){try{const r=JSON.parse(store.get(CKEY)||"null");
 if(r&&Date.now()-r.t<12*36e5){CART=r.c||{};OPT=r.o||{};
   if(r.s)for(const k in r.s)OPT[k]=Object.assign({sp:r.s[k]},OPT[k])}}catch(e){}})();
// 手机上切后台、关标签前再存一次，别让刚点的菜丢了
addEventListener("visibilitychange",()=>{if(document.visibilityState==="hidden")cartSave()});
addEventListener("pagehide",cartSave);
const stepper=(k,data)=>{const q=CART[k]?CART[k].q:0;
  return `<span class="qty${q?" has":""}" data-k="${k}"><button class="qbtn" type="button" data-q="-1" data-k="${k}" aria-label="−">−</button><span class="qn">${q}</span><button class="qbtn add" type="button" data-q="1" data-k="${k}" ${data||""} aria-label="＋">＋</button></span>`};
const exList=c=>((OPT[c]||{}).ex||[]);
const exSum=c=>exList(c).reduce((n,i)=>n+EXTRAS[i][1],0);
const itPrice=it=>it.dr?(it.dv?DRK[it.dv][1]:DRINK[it.dr][1]):((it.sz==="l"?findDish(it.c).p2:findDish(it.c).p)+(it.sz?0:exSum(it.c)));
// 这道菜选了什么：辣度（黄焖锅一定写出来）、不要香菜、加配菜
function optTxt(it,l){
  if(it.dr||it.sz)return [];
  const o=OPT[it.c]||{},out=[];
  if(POT(it.c))out.push(SP[o.sp||0][LI[l]]);
  if(o.nc)out.push(CT[l].noCo);
  exList(it.c).forEach(i=>out.push("+"+EXTRAS[i][0][LI[l]]));
  return out}
// 客人看的那一份：辣度带上「辣度：」，免得英文里只剩一个 None
function optTxtUI(it,l){
  if(it.dr||it.sz)return [];
  const o=OPT[it.c]||{},out=[],lc=x=>l==="zh"?x:x.toLowerCase();
  if(POT(it.c))out.push(CT[l].spice+(l==="zh"?"：":": ")+lc(SP[o.sp||0][LI[l]]));
  if(o.nc)out.push(CT[l].noCo);
  exList(it.c).forEach(i=>out.push("+"+EXTRAS[i][0][LI[l]]));
  return out}
const hasOpt=it=>!it.dr&&!it.sz&&(POT(it.c)||CORI.includes(it.c));
let OEDIT={};
const chipBtn=(d,label,on)=>`<button class="chip" type="button" data-opt="${d}" aria-pressed="${on}">${esc(label)}</button>`;
function optUI(c){
  const o=OPT[c]||{},ct=CT[L],out=[];
  if(POT(c)){
    out.push(`<div class="opt"><span class="qlab">${ct.spice}</span>${SP.map((x,i)=>chipBtn(`sp|${c}|${i}`,x[LI[L]],(o.sp||0)===i)).join("")}</div>`);
    out.push(`<div class="opt"><span class="qlab">${ct.extras}</span>${EXTRAS.map((e,i)=>chipBtn(`ex|${c}|${i}`,nm(e[0])+" +"+eur(e[1],L),exList(c).includes(i))).join("")}</div>`)}
  if(CORI.includes(c))out.push(`<div class="opt">${chipBtn(`nc|${c}|0`,ct.noCo,!!o.nc)}</div>`);
  return out.join("")}
function buyBlock(c){
  const d=findDish(c);if(!d)return "";
  const q=d.p2
    ?`<div class="qty2"><span class="qlab">${SZ[L].s}</span>${stepper(c+"|s",`data-c="${c}" data-sz="s"`)}</div>
      <div class="qty2"><span class="qlab">${SZ[L].l}</span>${stepper(c+"|l",`data-c="${c}" data-sz="l"`)}</div>`
    :stepper(c,`data-c="${c}"`);
  return `<div class="buy">${optUI(c)}<div class="buyrow"><span class="qlab">${esc(CT[L].pick)}</span><span class="buyq">${q}</span></div></div>`}
function itName(it,l){
  if(it.dr)return it.dv?DRK[it.dv][0][LI[l]]:drName(DRINK[it.dr],l);
  const d=findDish(it.c);let n=l==="zh"?d.zh:d[l];
  if(it.sz)n+=l==="zh"?"（"+SZ.zh[it.sz]+"）":" ("+SZ[l][it.sz]+")";
  return n}
const cKeys=()=>Object.keys(CART);
const cCount=()=>cKeys().reduce((n,k)=>n+CART[k].q,0);
const cTotal=()=>cKeys().reduce((n,k)=>n+CART[k].q*itPrice(CART[k]),0);
const grpOf=it=>it.dr||FRONT.includes(it.c)?"f":"k";
const zhLines=()=>cKeys().map(k=>{const it=CART[k];
  return {n:itName(it,"zh"),q:it.q,o:optTxt(it,"zh").join(" · "),g:grpOf(it)}});
// 按出餐分组，空的那组不出现
const zhGroups=()=>{const ls=zhLines();
  return ["k","f"].map(g=>({g:g,lab:GRP[g],rows:ls.filter(x=>x.g===g)})).filter(x=>x.rows.length)};
function cartBump(k,n,ds){
  let it=CART[k];
  if(!it){if(n<0)return;
    it=CART[k]=ds&&ds.dr?(ds.dv?{dr:ds.dr,dv:ds.dv,q:0}:{dr:ds.dr,q:0}):{c:ds.c,q:0};
    if(ds&&ds.sz)it.sz=ds.sz}
  it.q=Math.min(99,it.q+n);
  if(it.q<1)delete CART[k];
  cartSave();syncCart()}
function setOpt(kind,c,i){
  const o=OPT[c]||(OPT[c]={});
  if(kind==="sp")o.sp=i;
  else if(kind==="nc")o.nc=!o.nc;
  else{const a=o.ex||(o.ex=[]),p=a.indexOf(i);p<0?a.push(i):a.splice(p,1);a.sort((x,y)=>x-y)}
  cartSave();syncCart()}
function flyFrom(btn){
  if(!btn||matchMedia("(prefers-reduced-motion:reduce)").matches)return null;
  btn.classList.remove("tap");void btn.offsetWidth;btn.classList.add("tap");
  const card=btn.closest(".dish,.first li"),img=card&&card.querySelector(".thumb img");
  return {b:btn.getBoundingClientRect(),src:img?img.src:""}}
function flyToCart(f){
  if(!f)return;
  const bar=$("cartbar"),b=f.b;
  const el=document.createElement("div");
  el.className="fly";
  if(f.src)el.style.backgroundImage=`url("${f.src}")`;
  el.style.left=(b.left+b.width/2-19)+"px";
  el.style.top=(b.top+b.height/2-19)+"px";
  document.body.appendChild(el);
  const t=bar.hidden?null:bar.getBoundingClientRect();
  const tx=t?t.left+40:innerWidth/2, ty=t?t.top+t.height/2:innerHeight-40;
  const go=()=>{el.style.transform=`translate(${tx-(b.left+b.width/2)}px,${ty-(b.top+b.height/2)}px) scale(.3)`;
    el.style.opacity=".2"};
  requestAnimationFrame(go);setTimeout(go,40);   // 后台标签页里 rAF 会被掐掉，补一个定时器
  setTimeout(()=>el.remove(),600);
  if(!bar.hidden){bar.classList.remove("pop");void bar.offsetWidth;bar.classList.add("pop")}}
function syncCart(){
  const ct=CT[L],n=cCount();
  document.querySelectorAll("[data-k]").forEach(el=>{
    const q=CART[el.dataset.k]?CART[el.dataset.k].q:0;
    el.classList.toggle("has",q>0);
    const o=el.querySelector(".qn");if(o)o.textContent=q});
  document.querySelectorAll("#menu .dish").forEach(el=>{const c=el.id.slice(2);
    el.classList.toggle("picked",!!(CART[c]||CART[c+"|s"]||CART[c+"|l"]))});
  document.querySelectorAll("[data-opt]").forEach(b=>{const[kind,c,i]=b.dataset.opt.split("|");const o=OPT[c]||{};
    b.setAttribute("aria-pressed",kind==="sp"?(o.sp||0)===+i:kind==="nc"?!!o.nc:exList(c).includes(+i))});
  $("cartbar").hidden=!n;document.body.classList.toggle("hascart",!!n);
  if(n){$("cb-n").textContent=ct.items.replace("%s",n);$("cb-t").textContent=eur(cTotal(),L);$("cb-go").textContent=ct.view}
  if(!$("sheet").hidden&&DETC&&$("detbuy")){$("detbuy").innerHTML=buyBlock(DETC);
    if($("detpair"))$("detpair").innerHTML=pairBox(findDish(DETC))}
  if(!$("order").hidden)renderOrder();
  if(!$("staff").hidden)renderStaff();
}
// 结算前的加点：小菜按 UPSELL（出餐快、毛利高），饮料按单子里那些菜各自的推荐
function addonBlock(){
  const ct=CT[L],ks=cKeys();
  const sides=UPSELL.map(k=>sideOpts().find(o=>o.k===k)).filter(o=>o&&!CART[o.k]).slice(0,2);
  let drinks=[];
  if(!ks.some(k=>CART[k].dr)){
    const seen={};
    for(const k of ks){const p=PR[CART[k].c];if(!p)continue;
      for(const dk of p[1])if(!seen[dk]){seen[dk]=1;drinks.push(dk)}}
    if(!drinks.length)drinks=["am","cc"];
    drinks=drinks.slice(0,3).map(dk=>({k:DRKMAP[dk]+"|"+dk,dr:DRKMAP[dk],dv:dk}));
  }
  if(!sides.length&&!drinks.length)return "";
  const chip=(o,ds)=>`<button class="chip" type="button" data-q="1" data-k="${o.k}" ${ds}>${esc(pickName(o))} +${eur(pickPrice(o),L)}</button>`;
  return `<div class="addon">
    ${sides.length?`<b>${esc(ct.addT)}</b><div class="opt">${sides.map(o=>chip(o,`data-c="${o.c}" data-sz="${o.sz||""}"`)).join("")}</div>`:""}
    ${drinks.length?`<b>${esc(ct.addD)}</b><div class="opt">${drinks.map(o=>chip(o,`data-dr="${o.dr}" data-dv="${o.dv}"`)).join("")}</div>`:""}</div>`;
}
function renderOrder(){
  const ct=CT[L],ks=cKeys();
  const rows=ks.map(k=>{const it=CART[k];
    const o=optTxtUI(it,L).join(" · ");
    const ed=hasOpt(it)?`<button class="on-edit" type="button" data-oedit="${it.c}" aria-expanded="${!!OEDIT[it.c]}">${o?esc(o)+" · "+esc(ct.optEdit):esc(ct.optEdit)+(L==="zh"?"：":": ")+esc(L==="zh"?ct.noCo:ct.noCo.toLowerCase())} <span class="ar">${OEDIT[it.c]?"▾":"›"}</span></button>${OEDIT[it.c]?`<div class="on-opts">${optUI(it.c)}</div>`:""}`:(o?`<em class="on-o">${esc(o)}</em>`:"");
    return `<li><div class="on-r"><div class="on-n">${esc(itName(it,L))}</div>
      ${stepper(k)}<div class="on-p">${eur(it.q*itPrice(it),L)}</div></div>${ed}</li>`}).join("");
  const zh=zhGroups().map(g=>`<div class="zhg">${g.lab}</div>`+g.rows.map(x=>`<div class="zhrow"><span class="zhn2">${esc(x.n)}${x.o?" · "+x.o:""}</span><span>×${x.q}</span></div>`).join("")).join("");
  $("order").innerHTML=`<div class="in">
    <div class="orow"><h3>${esc(ct.title)}</h3><button class="xbtn" type="button" id="oclose" aria-label="${esc(ct.back)}">×</button></div>
    ${ks.length?`<div class="warn">${esc(ct.notOrder)}</div>
    <ul class="olist">${rows}</ul>
    <div class="otot"><span>${esc(ct.total)}</span><b>${eur(cTotal(),L)}</b></div>
    <div class="ohint">${esc(ct.priceNote)}</div>
    ${addonBlock()}
    <div class="zhbox"><dt>给店员看 · 中文</dt>${zh}
      <div class="zhrow zhsum"><span>共 ${cCount()} 份</span><span>${eur(cTotal(),"es")}</span></div></div>
    <div class="oact"><button class="obtn" type="button" id="ostaff">${esc(ct.staff)}</button>
      <button class="obtn sec" type="button" id="ocopy">${esc(ct.copy)}</button>
      <button class="obtn sec" type="button" id="oclear">${esc(ct.clear)}</button></div>`
    :`<p class="ohint">${esc(ct.empty)}</p>`}
  </div>`;
  $("oclose").onclick=closeOrder;
  if(!ks.length)return;
  $("ostaff").onclick=openStaff;
  $("oclear").onclick=()=>{CART={};cartSave();syncCart()};
  $("ocopy").onclick=e=>{const b=e.currentTarget;
    const done=()=>{b.textContent=CT[L].copied;setTimeout(()=>{if(!$("order").hidden)b.textContent=CT[L].copy},1500)};
    try{navigator.clipboard.writeText(orderText()).then(done,()=>{})}catch(_){}};
}
function renderStaff(){
  $("staff").innerHTML=`<div class="sx"><span>${esc(CT[L].staffNote)}</span><button type="button" id="sclose" aria-label="关闭">×</button></div>
   ${zhGroups().map(g=>`<h4 class="sg">${g.lab}</h4><ul>${g.rows.map(x=>`<li><span>${esc(x.n)}${x.o?`<em>${x.o}</em>`:""}</span><b>×${x.q}</b></li>`).join("")}</ul>`).join("")}
   <div class="stot"><span>共 ${cCount()} 份</span><b>${eur(cTotal(),"es")}</b></div>`;
  $("sclose").onclick=closeStaff;
}
const orderText=()=>["Sibisi Ramen"].concat(
  ...zhGroups().map(g=>["【"+g.lab+"】"].concat(g.rows.map(x=>`${x.n}${x.o?"（"+x.o+"）":""} ×${x.q}`))),
  [`共 ${cCount()} 份　${eur(cTotal(),"es")}`]).join("\n");
function openOrder(){renderOrder();$("order").hidden=false;$("scrim").hidden=false;
  document.body.classList.add("ordering");document.body.style.overflow="hidden"}
function closeOrder(){$("order").hidden=true;$("scrim").hidden=true;
  document.body.classList.remove("ordering");document.body.style.overflow=""}
function openStaff(){renderStaff();$("staff").hidden=false;document.body.style.overflow="hidden"}
function closeStaff(){$("staff").hidden=true;document.body.style.overflow=$("order").hidden?"":"hidden"}
$("cb-go").addEventListener("click",openOrder);
(function(){let l=store.get("lang");
 if(!l){const n=(navigator.language||"es").slice(0,2);l=n==="zh"?"zh":(n==="es"||n==="ca")?"es":"en"}
 L=T[l]?l:"es";render()})();
