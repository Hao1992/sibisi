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
const BRAND=__BRAND__;
const BYURL=__BYURL__;
const HOURS=__HOURS__;
const DRILL=__DRILL__;
const DRILLV=__DRILLV__;
const MAP=__MAP__;
const REV=__REV__;
const TOP=__TOP__;
const FRONT=__FRONT__;
const GRP=__GRP__;
const COMBO=__COMBO__;
const JQ=__JQ__;
const JQW=__JQW__;
const HANZI=__HANZI__;
const SAYING=__SAYING__;
const CHOP=__CHOP__;
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
 {id:"M",  lab:l=>woLab("M",l),  ok:d=>!als(d).includes("M")},
 {id:"np", lab:l=>T[l].fNoPork,  ok:d=>!fls(d).includes("p")}];
let FIL=[];
const dishOk=d=>FIL.every(id=>FILD.find(f=>f.id===id).ok(d));
// 节气图标：一笔一画的小符号，说明这个节气是什么意思
const JQI={
 sprout:'<path d="M12 21V11"/><path d="M12 13c-4 0-6-3-6-6 4 0 6 3 6 6z"/><path d="M12 15c4 0 6-3 6-6-4 0-6 3-6 6z"/>',
 rain:'<path d="M7 13.5a4 4 0 0 1 .6-8 5.5 5.5 0 0 1 10.3 1.6A3.5 3.5 0 0 1 17.5 13.5z"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/>',
 bug:'<ellipse cx="12" cy="14" rx="4.5" ry="6"/><path d="M12 8V5M9.5 6L8 3.5M14.5 6L16 3.5M7.5 12H4M7.5 16.5H4M16.5 12H20M16.5 16.5H20"/>',
 balance:'<circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor" stroke="none"/>',
 grain:'<path d="M12 21V8"/><path d="M12 8c0-3 2-5 4.5-5 0 3-2 5-4.5 5zM12 8c0-3-2-5-4.5-5 0 3 2 5 4.5 5zM12 14c0-3 2-5 4.5-5 0 3-2 5-4.5 5zM12 14c0-3-2-5-4.5-5 0 3 2 5 4.5 5z"/>',
 sun:'<circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.6M12 19.4V22M2 12h2.6M19.4 12H22M5 5l1.9 1.9M17.1 17.1L19 19M19 5l-1.9 1.9M6.9 17.1L5 19"/>',
 hotsun:'<circle cx="12" cy="8.5" r="4"/><path d="M12 1.5v2M2.5 8.5h2M19.5 8.5h2M5.2 1.8l1.4 1.4M18.8 1.8l-1.4 1.4"/><path d="M3 16c2-1.6 4 1.6 6 0s4 1.6 6 0 2 1.6 3 .4M3 20c2-1.6 4 1.6 6 0s4 1.6 6 0 2 1.6 3 .4"/>',
 leaf:'<path d="M5 19.5C5 10.5 11 5 19.5 5c0 8.5-5.5 14.5-14.5 14.5z"/><path d="M19.5 5L9 15.5"/>',
 fall:'<path d="M15 3.5c4 3 4.5 8 1 11.5s-8.5 3-11.5-1c3-3.5 7-6 10.5-10.5z"/><path d="M4.5 20.5c3-2 5.5-4.5 8-8"/>',
 dew:'<path d="M12 4c3 4.5 5 7 5 9.5A5 5 0 0 1 7 13.5C7 11 9 8.5 12 4z"/>',
 frost:'<path d="M3 21h18"/><path d="M12 4v13M5.4 7.8l13.2 7.6M18.6 7.8L5.4 15.4"/>',
 snow:'<path d="M12 2v20M3.3 7l17.4 10M20.7 7L3.3 17"/><path d="M9.4 3.6L12 6.2l2.6-2.6M9.4 20.4L12 17.8l2.6 2.6"/>',
 ice:'<path d="M2.5 4.5h19"/><path d="M6.5 4.5L8 15l1.5-10.5M12.5 4.5L14 21l1.5-16.5M17.5 4.5L18.6 12l1.1-7.5"/>',
 moon:'<path d="M20.5 14.8A8.6 8.6 0 0 1 9.2 3.5a8.6 8.6 0 1 0 11.3 11.3z"/>'};
const EGGI={chop:'<path d="M4.5 20.5L17.5 3.5M9 20.5L20 6"/>',
 slip:'<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="M7.5 10h9M7.5 13.5h5.5"/>'};
const eggIcon=k=>`<svg class="eggi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${EGGI[k]}</svg>`;
// 节气小景：分层的 SVG 山水（天色 + 远近山 + 雾 + 当季景物），按季节换一张
const SCENE={
 light:{ink:"#3f5b36",sky:["#f2f8ea","#cfe4c4"],far:"#8db47c",near:"#5e8a52"},
 spicy:{ink:"#2f4f48",sky:["#eef4f2","#c3d9d2"],far:"#8aa9a0",near:"#5a7f75"},
 cold: {ink:"#1f4d5c",sky:["#e6f4f7","#a8d9e4"],far:"#73b6c6",near:"#3d8aa0"},
 warm: {ink:"#6b3b12",sky:["#fbf2e2","#edd6ae"],far:"#c9a269",near:"#a4692a"},
 hot:  {ink:"#2d3f52",sky:["#eff3f7","#c6d3df"],far:"#93a7ba",near:"#5d7489"}};
const enc=x=>encodeURIComponent(x).replace(/\(/g,"%28").replace(/\)/g,"%29").replace(/'/g,"%27");
function jqScene(b){
  const c=SCENE[b]||SCENE.warm,W=340,H=120;
  const mt=(pts,fill,op)=>`<path d="M0 ${H}${pts}L${W} ${H}Z" fill="${fill}" opacity="${op}"/>`;
  const mist=(x,y,rx,ry,o)=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#fff" opacity="${o}"/>`;
  let art="";
  if(b==="light")      // 春：柳条 + 燕子
    art=`<path d="M0 78q26-16 54 2t58-10 56 14 60-12 58 10 54-4" stroke="${c.near}" stroke-width="1.4" fill="none" opacity=".35"/>`
      +`<path d="M250 0q24 14 30 34" stroke="${c.near}" stroke-width="2.4" fill="none" opacity=".75"/>`
      +[0,1,2,3,4,5].map(i=>`<path d="M${256+i*6} ${8+i*5}q-9 14-6 26" stroke="${c.near}" stroke-width="1.5" fill="none" opacity=".6"/>`).join("")
      +`<path d="M168 34q7-9 10-2q3-7 10 1" stroke="${c.ink}" stroke-width="2" fill="none" opacity=".6" stroke-linecap="round"/>`
      +`<path d="M202 54q5-7 8-1.5q2.5-5.5 8 .5" stroke="${c.ink}" stroke-width="1.7" fill="none" opacity=".45" stroke-linecap="round"/>`;
  else if(b==="spicy") // 清明谷雨：烟雨 + 小船
    art=[...Array(26)].map((_,i)=>`<path d="M${8+i*13} ${6+(i%4)*9}l-9 20" stroke="#fff" stroke-width="1.3" opacity=".55"/>`).join("")
      +`<path d="M232 100q16 7 34 0-5 7-17 7t-17-7z" fill="${c.ink}" opacity=".7"/>`
      +`<path d="M249 98V80M249 80l14 14h-14" fill="${c.ink}" opacity=".55" stroke="${c.ink}" stroke-width="1.4"/>`;
  else if(b==="cold")  // 夏：烈日 + 水纹 + 荷叶
    art=`<circle cx="276" cy="34" r="19" fill="#f6b73c" opacity=".85"/>`
      +[0,1,2].map(i=>`<path d="M0 ${96+i*8}q30-6 60 0t60 0 60 0 60 0 60 0" stroke="#fff" stroke-width="1.5" fill="none" opacity=".5"/>`).join("")
      +`<ellipse cx="54" cy="96" rx="30" ry="11" fill="${c.near}" opacity=".7"/><path d="M54 96l-22-6" stroke="#fff" stroke-width="1.3" opacity=".6"/>`
      +`<ellipse cx="104" cy="106" rx="20" ry="7" fill="${c.near}" opacity=".5"/>`;
  else if(b==="warm"){ // 秋：芦苇 + 落叶
    const leaf=(x,y,r,sc)=>`<g transform="translate(${x} ${y}) rotate(${r}) scale(${sc})"><path d="M0 0c7-8 18-8 24 0-6 8-17 8-24 0z" fill="#c0601f" opacity=".82"/><path d="M1 0h22" stroke="#7d3a10" stroke-width="1.1" opacity=".45" fill="none"/></g>`;
    art=`<path d="M298 118q7-34-3-52M312 118q2-30 9-44M286 118q9-24 7-36" stroke="${c.near}" stroke-width="1.8" fill="none" opacity=".75"/>`
      +`<g fill="${c.near}" opacity=".7"><ellipse cx="295" cy="63" rx="3" ry="8" transform="rotate(-12 295 63)"/><ellipse cx="321" cy="72" rx="2.6" ry="7" transform="rotate(10 321 72)"/><ellipse cx="293" cy="80" rx="2.4" ry="6" transform="rotate(-18 293 80)"/></g>`
      +leaf(222,20,-24,1)+leaf(258,44,34,.78)+leaf(192,56,-8,.62)}
  else                 // 冬：雪山 + 枯枝 + 雪
    art=`<path d="M64 60l16-18 16 18q-16 7-32 0zM196 52l18-20 18 20q-18 8-36 0z" fill="#fff" opacity=".85"/>`
      +`<path d="M340 6q-34 10-50 34" stroke="${c.ink}" stroke-width="2.2" fill="none" opacity=".6"/>`
      +`<path d="M318 14q-6 12-4 22M300 24q-4 10 0 18" stroke="${c.ink}" stroke-width="1.5" fill="none" opacity=".45"/>`
      +[[40,26,3],[88,14,2.2],[130,40,2.6],[168,20,2],[214,70,2.4],[256,52,2],[22,62,2.2],[106,70,1.8]]
        .map(([x,y,r])=>`<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" opacity=".9"/>`).join("");
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`
   +`<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.sky[0]}"/><stop offset="1" stop-color="${c.sky[1]}"/></linearGradient></defs>`
   +`<rect width="${W}" height="${H}" fill="url(#g)"/>`
   +mt(" L40 58 L78 80 L120 48 L166 84 L212 60 L258 88 L302 64 L340 88 ",c.far,".45")
   +mt(" L52 78 L96 98 L150 72 L202 100 L252 80 L300 104 L340 86 ",c.near,".42")
   +mist(110,90,120,9,".55")+mist(248,104,96,8,".45")+art
   +`</svg>`;
  return {ink:c.ink,
    css:`background-image:linear-gradient(95deg,rgba(255,255,255,.92) 0%,rgba(255,255,255,.72) 42%,rgba(255,255,255,.12) 74%,rgba(255,255,255,0) 100%),url('data:image/svg+xml,${enc(svg)}');background-size:cover;background-position:center`}}
const jqIcon=(k,cls)=>`<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${JQI[k]||JQI.sun}</svg>`;
// 今日是哪个节气。节气按太阳位置算，全球同一天；元旦到小寒之间算上一年的冬至。
function jieqi(){
  const d=new Date(),m=d.getMonth()+1,day=d.getDate();
  let cur=JQ[JQ.length-1];
  for(const x of JQ)if(x[0]<m||(x[0]===m&&x[1]<=day))cur=x;
  return cur}
// 节气决定挑什么菜：热的 / 炖的 / 清淡的 / 凉爽的 / 辣的
const JQPICK={
  hot:  d=>["hm","sopa"].includes(d._s),
  warm: d=>d.ta.includes("intenso")||d.ta.includes("sabroso"),
  light:d=>d.ta.includes("suave")||d.ta.includes("agridulce"),
  cold: d=>["mix","frios"].includes(d._s)||d.ta.includes("fresco")||d.ta.includes("acido"),
  spicy:d=>fls(d).includes("h")};
let LUCK=null;
function pickLucky(){
  const q=jieqi(),want=JQPICK[q[6]];
  const all=[];
  for(const sec of S)for(const d of sec.d){
    if(d.c==="2-11"||!dishOk(d))continue;
    all.push(Object.assign({_s:sec.id},d))}
  let pool=all.filter(want),fb=false;
  if(!pool.length){pool=all;fb=true}            // 筛选之后没有应季的，就不提节气那句话
  if(LUCK){const f=pool.filter(x=>x.c!==LUCK.d.c);if(f.length)pool=f}
  if(!pool.length)return null;
  return {q:q,fb:fb,d:pool[Math.floor(Math.random()*pool.length)]}}
function renderLuck(){
  const box=$("luck"),t=T[L];box.hidden=false;
  if(!LUCK){
    const q0=jieqi();
    box.className="lask";box.removeAttribute("style");
    const sc=jqScene(q0[6]);
    box.innerHTML=`<button class="lbtn" type="button" id="lbtn" style="${sc.css};color:${sc.ink}">${jqIcon(q0[7],"lic")}
      <span class="lbt"><b>${esc(t.luckAsk)}</b><em>${esc(t.luckSub.replace("%s",q0[2]))}</em></span></button>`;
    $("lbtn").onclick=()=>{LUCK=pickLucky();renderLuck();
      $("luck").scrollIntoView({block:"nearest",behavior:"smooth"})};
    return}
  const d=findDish(LUCK.d.c),q=LUCK.q;
  box.className="luck";box.removeAttribute("style");
  const sc=jqScene(q[6]);
  box.innerHTML=`<div class="lban" style="${sc.css};color:${sc.ink}">
     <span class="lbd">${jqIcon(q[7],"jqi")}${esc(t.today)}</span>
     <b class="lbz">${esc(q[2])}</b>
     <span class="lbp">${esc(q[3])}${L==="zh"?"":" · "+esc(L==="es"?q[4]:q[5])}</span></div>
    ${LUCK.fb?"":`<p>${esc(JQW[q[6]][LI[L]])}</p>`}
    <div class="lrow">
      <div class="thumb">${d.img?`<img src="img/t/${d.img}.jpg" alt="" loading="lazy">`:illo(d.c,"")}<span class="badge">${d.c}</span></div>
      <div class="lt"><h4>${esc(L==="zh"?d.zh:d[L])}</h4>${DET[d.c]?`<button class="llink" type="button" data-det="${d.c}">${esc(t.seeIt)}</button>`:""}</div>
      <div class="lr"><b>${eur(d.p,L)}</b>${stepper(d.c,`data-c="${d.c}"`)}</div></div>
    <button class="chip more" type="button" id="lagain">${esc(t.luckAgain)}</button>`;
  $("lagain").onclick=()=>{LUCK=pickLucky();renderLuck();
    $("luck").scrollIntoView({block:"nearest",behavior:"smooth"})};
}
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
  const cur=PICK[d.c]||(PICK[d.c]={sd:{[recSide.k]:{o:recSide,q:1}},dr:{[recDr[0].k]:{o:recDr[0],q:1}}});   // 小菜和饮料都默认跟推荐，不要就点「不要饮料」
  const line=(kind,e)=>`<li><span>${esc(pickName(e.o))}</span><span>+${eur(pickPrice(e.o),L)}</span>
     <span class="qty has"><button class="qbtn" type="button" data-cq="${kind};${d.c};${e.o.k};-1" aria-label="−">−</button><span class="qn">${e.q}</span><button class="qbtn add" type="button" data-cq="${kind};${d.c};${e.o.k};1" aria-label="＋">＋</button></span></li>`;
  const quick=(kind,o)=>cur[kind][o.k]?"":`<button class="chip" type="button" data-cq="${kind};${d.c};${o.k};1">${esc(pickName(o))} +${eur(pickPrice(o),L)}</button>`;
  const group=(kind,label,recs)=>{
    const es=Object.values(cur[kind]);
    const none=kind==="dr"&&es.length?`<button class="chip none" type="button" data-cq="dr;${d.c};!;0">${esc(ct.noDrink)}</button>`:"";
    return `<div class="grp"><span class="qlab">${esc(label)}</span>
      ${es.length?`<ul class="glist">${es.map(e=>line(kind,e)).join("")}</ul>`:""}
      <div class="opt">${recs.map(o=>quick(kind,o)).join("")}<button class="chip more" type="button" data-more="${kind}|${d.c}">${esc(kind==="sd"?ct.otherSide:ct.otherDrink)}</button>${none}</div></div>`};
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
  if(c==="*"){const o=kind==="sd"?sideOpts().find(x=>x.k===k):optByKey("dr",k);
    cartBump(k,n,o.dr?{dr:o.dr,dv:o.dv}:{c:o.c,sz:o.sz});
    if(!$("pick").hidden)pickCounts(kind,c);
    return}
  const cur=PICK[c]||(PICK[c]={sd:{},dr:{}});
  if(k==="!"){cur[kind]={};
    if($("detpair"))$("detpair").innerHTML=pairBox(findDish(c));
    if(!$("pick").hidden)pickCounts(kind,c);
    return}
  const e=cur[kind][k]||(cur[kind][k]={o:optByKey(kind,k),q:0});
  e.q=Math.max(0,Math.min(20,e.q+n));
  if(!e.q)delete cur[kind][k];
  if($("detpair"))$("detpair").innerHTML=pairBox(findDish(c));
  if(!$("pick").hidden)pickCounts(kind,c)}
function pickCounts(kind,c){
  const toCart=c==="*",cur=toCart?null:((PICK[c]||{})[kind]||{});
  $("pick").querySelectorAll("[data-cq]").forEach(b=>{
    const k=b.dataset.cq.split(";")[2];
    const q=toCart?(CART[k]?CART[k].q:0):(cur[k]?cur[k].q:0);
    b.setAttribute("aria-pressed",!!q);
    const s=b.querySelector(".pcount");if(s)s.textContent=q?"×"+q:""})}
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
  $("tagline").textContent=BACK?t.hiAgain:t.tagline;
  {const q=jieqi();                                   // 报头下面的今日节气，每天自己变
   $("jqbar").innerHTML=jqIcon(q[7],"jqi")+`<span><b>${esc(t.today)} · <span class="jqz">${esc(q[2])}</span></b> ${esc(q[3])}${L==="zh"?"":" · "+esc(L==="es"?q[4]:q[5])} · ${esc(JQW[q[6]][LI[L]])}</span>`;} $("h-eye").textContent=t.eye; $("h-title").textContent=t.title;
  $("h-desc").textContent=t.desc; $("h-from").textContent=t.frm;
  $("steps").innerHTML=t.steps.map(s=>`<li>${esc(s)}</li>`).join("");
  $("first-t").textContent=t.firstT;
  $("first").innerHTML=FIRST.map(f=>{const d=findDish(f.c),det=DET[f.c]?` data-det="${f.c}" tabindex="0" role="button"`:"";
    return `<li${det}><div class="thumb">${d.img?`<img src="img/t/${d.img}.jpg" alt="" loading="lazy">`:illo(d.c,"")}<span class="badge">${d.c}</span></div>
      <div class="ft"><h4>${esc(L==="zh"?d.zh:d[L])}</h4><em>${esc(f[L])}</em></div>
      <div class="fr"><b>${eur(d.p,L)}</b>${stepper(d.c,`data-c="${d.c}"`)}</div></li>`}).join("");
  $("herobuy").innerHTML=`<span class="qlab">1-1 ${esc(L==="zh"?findDish("1-1").zh:findDish("1-1")[L])}</span>${stepper("1-1",'data-c="1-1"')}`;
  renderPacks();
  $("promise").innerHTML=`<b>${esc(t.promiseT)}</b><ul>${t.promise.map(([ic,x])=>`<li><span>${ic}</span>${esc(x)}</li>`).join("")}</ul>`;
  $("f-take").textContent=t.take; $("copy").textContent=t.copy;
  $("phone").href="tel:"+TEL;
  $("totop").setAttribute("aria-label",CT[L].toTop);
  $("f-hrs-t").textContent=t.hrsT;
  const wd=new Date().getDay();
  $("f-hrs").innerHTML=HOURS.map(g=>`<div class="hr${g.d.includes(wd)?" now":""}"><span>${esc(g[L])}</span><span>${esc(g.h[L])}</span></div>`).join("");
  $("f-dirs").textContent=t.dirs; $("f-dirs").href=MAP;
  $("f-rev").textContent=t.rev;   $("f-rev").href=REV;
  $("f-all").innerHTML=algRow("G H S Sé P M",true)+`<div style="margin-top:6px">${esc(t.all)}</div>`;
  $("f-by").href=BYURL;$("f-by").innerHTML=esc(t.by).replace("%s",`<b>${esc(BRAND)}</b>`)+" ›";
  document.querySelectorAll(".lang button").forEach(b=>b.setAttribute("aria-pressed",b.dataset.l===L));
  const secName=s=>L==="zh"?s.zh:s[L];
  renderFil();
  renderLuck();
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
      const price=d.p2?`<span class="pz">${SZ[L].s}</span>${eur(d.p,L)}<span class="pz">${SZ[L].l}</span>${eur(d.p2,L)}`:eur(d.p,L);
      h+=`<div class="dish" id="d-${d.c}"${det}><div class="thumb">${d.img?`<img src="img/t/${d.img}.jpg" alt="" loading="lazy">`:illo(d.c,"")}<span class="badge">${d.c}</span></div>
        <div class="t"><h4>${esc(name)}</h4><div class="zhn">${esc(sub)}</div>${desc?`<p>${esc(desc)}</p>`:""}${taste?`<div class="taste">${taste}</div>`:""}${tags?`<div class="tags">${tags}</div>`:""}${algRow(d.al,true)}${pairLine(d)}${DET[d.c]?`<span class="more">${t.more}</span>`:""}<div class="qwrap">${qty}</div></div>
        <div class="price${d.p2?" two":""}">${price}</div></div>`;
    }
    h+=`</div>`;
    if(s.id==="hm")h+=`<div class="extras"><b>${t.extras}</b><ul>${EXTRAS.map(e=>`<li><span>${esc(nm(e[0]))}</span><span>+${eur(e[1],L)}</span></li>`).join("")}</ul></div>`;
    h+=`</section>`;
  }
  h+=`<section id="bebidas"><div class="sh"><h3>${t.drinks}</h3>${L==="zh"?"":'<span class="zh">酒水</span>'}</div><div class="drinks">`;
  for(const k of ["beers","wine","soft","water"])h+=`<div><h5>${t[k]}</h5><ul>${DR[k].map((x,i)=>{const id=`dr-${k}-${i}`;return `<li><span class="dth">${drArt(id)}</span><span class="dn">${esc(drName(x,L))}</span><span class="dr-r">${eur(x[1],L)}${stepper(id,`data-dr="${id}"`)}</span></li>`}).join("")}</ul></div>`;
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
// 套餐里每一行的小图：菜用实拍缩略图，酒水用一个瓶子符号
const BOTTLE='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2h4v3.5l2 3V21a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V8.5l2-3z"/><path d="M8 13h8"/></svg>';
const packThumb=o=>{if(o.dr)return drArt(o.dr,o.dv)||BOTTLE;const d=findDish(o.c);
  return d&&d.img?`<img src="img/t/${d.img}.jpg" alt="" loading="lazy">`:BOTTLE};
function renderPacks(){
  const t=T[L];
  $("packs").innerHTML=`<b>${esc(t.packT)}</b>`+COMBO.map(p=>{
    const tot=packTotal(p);
    return `<div class="pk"><div class="pkh"><b>${esc(p[L])}</b></div>
      <p>${esc(p[L+"2"])}</p>
      <ul>${p.items.map(([k,q])=>{const o=packOpt(k);
        return `<li><span class="pth">${packThumb(o)}</span><span class="pn">${esc(pickName(o))}</span><span>×${q}</span></li>`}).join("")}</ul>
      <p class="pksame">${esc(t.packSame)}</p>
      <div class="pkf"><div class="pkp"><b>${eur(tot,L)}</b><em>${esc(t.packEach.replace("%s",eur(tot/p.n,L)))}</em></div>
        <button class="obtn" type="button" data-pack="${p.id}">${esc(t.packAdd)}</button></div></div>`}).join("")
    +`<small>${esc(t.packNote)}</small>`;
}
// 筷子示意图：两根筷子 + 标号的手指位置，和菜品插画同一套配色
function chopSvg(n){
  const bg='<rect width="160" height="90" fill="#efe4c8"/>';
  // 手握左边，筷尖在右边；越往右越细
  const stk=(y1,y2,w,col)=>`<polygon points="12,${y1-w} 150,${y2-1.6} 150,${y2+1.6} 12,${y1+w}" fill="${col}"/>`;
  const dot=(x,y,i)=>`<circle cx="${x}" cy="${y}" r="11" fill="#d4482f"/><text x="${x}" y="${y+5}" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">${i}</text>`;
  const W="#b07c46",G="#dcc9ad";
  if(n===1)return `<svg viewBox="0 0 160 90" role="img">${bg}${stk(72,60,5,W)}${dot(42,69,1)}${dot(78,66,2)}</svg>`;
  if(n===2)return `<svg viewBox="0 0 160 90" role="img">${bg}${stk(72,60,5,G)}${stk(34,52,4.5,W)}${dot(36,39,1)}${dot(66,42,2)}${dot(96,46,3)}</svg>`;
  return `<svg viewBox="0 0 160 90" role="img">${bg}${stk(72,60,5,W)}${stk(26,44,4.5,G)}${stk(44,56,4.5,W)}
    <path d="M58 26 q-14 14 -2 28" stroke="#d4482f" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <path d="M50 52 l10 2 -3 -10z" fill="#d4482f"/>
    <circle cx="148" cy="58" r="8" fill="none" stroke="#3f8f3a" stroke-width="3"/></svg>`}
let CHOPOPEN=false;
function chopBlock(){
  const t=T[L];
  return `<button class="eggb" type="button" data-chop="1" aria-expanded="${CHOPOPEN}">${eggIcon("chop")}${esc(t.chopT)}</button>`
    +(CHOPOPEN?`<div class="chop">${CHOP.map((x,i)=>`<div class="cstep">${chopSvg(i+1)}<p><b>${i+1}</b>${esc(x[LI[L]])}</p></div>`).join("")}<small>${esc(t.chopEnd)}</small></div>`:"")}
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
  const ch=e.target.closest("[data-chop]");
  if(ch){e.preventDefault();CHOPOPEN=!CHOPOPEN;renderOrder();return}
  const sl=e.target.closest("[data-slip]");
  if(sl){e.preventDefault();if(!canDraw())return;drawSlip();
    clearTimeout(SLIPT);
    SLIPT=setTimeout(()=>{if(!$("order").hidden)renderOrder();if(!$("staff").hidden)renderStaff()},SWIN+200);
    if(!$("order").hidden)renderOrder();
    if(!$("staff").hidden)renderStaff();
    const c=document.querySelector(".slipcard");if(c)c.scrollIntoView({block:"nearest",behavior:"smooth"});return}
  const sp=e.target.closest("[data-split]");
  if(sp){e.preventDefault();splitLine(sp.dataset.split);return}
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
const SZ={zh:{s:"小",l:"大"},es:{s:"pequeña",l:"grande"},en:{s:"small",l:"large"}};
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
const lineQ=k=>CART[k]?CART[k].q:0;
const dishQ=k=>cKeys().reduce((n,x)=>n+(x===k||x.indexOf(k+"#")===0?CART[x].q:0),0);
const stepper=(k,data,raw)=>{const q=raw?lineQ(k):dishQ(k);
  return `<span class="qty${q?" has":""}" data-k="${k}"${raw?' data-raw="1"':""}><button class="qbtn" type="button" data-q="-1" data-k="${k}" aria-label="−">−</button><span class="qn">${q}</span><button class="qbtn add" type="button" data-q="1" data-k="${k}" ${data||""} aria-label="＋">＋</button></span>`};
const codeOf=k=>k.split("#")[0];                 // 1-1#2 -> 1-1
const exList=k=>((OPT[k]||{}).ex||[]);
const exSum=k=>exList(k).reduce((n,i)=>n+EXTRAS[i][1],0);
const itPrice=k=>{const it=CART[k];
  return it.dr?(it.dv?DRK[it.dv][1]:DRINK[it.dr][1])
             :((it.sz==="l"?findDish(it.c).p2:findDish(it.c).p)+(it.sz?0:exSum(k)))};
// 这道菜选了什么：辣度（黄焖锅一定写出来）、不要香菜、加配菜
function optTxt(k,l){
  const it=CART[k];if(!it||it.dr||it.sz)return [];
  const o=OPT[k]||{},out=[];
  if(POT(it.c))out.push(SP[o.sp||0][LI[l]]);
  if(o.nc)out.push(CT[l].noCo);
  exList(k).forEach(i=>out.push("+"+EXTRAS[i][0][LI[l]]));
  return out}
// 客人看的那一份：辣度带上「辣度：」，免得英文里只剩一个 None
function optTxtUI(k,l){
  const it=CART[k];if(!it||it.dr||it.sz)return [];
  const o=OPT[k]||{},out=[],lc=x=>l==="zh"?x:x.toLowerCase();
  if(POT(it.c))out.push(CT[l].spice+(l==="zh"?"：":": ")+lc(SP[o.sp||0][LI[l]]));
  if(o.nc)out.push(CT[l].noCo);
  exList(k).forEach(i=>out.push("+"+EXTRAS[i][0][LI[l]]));
  return out}
const hasOpt=it=>!it.dr&&!it.sz&&(POT(it.c)||CORI.includes(it.c));
// 把一行里的 1 份拆出来，复制当前选项，之后两行各改各的
function splitLine(k){
  const it=CART[k];if(!it||it.q<2)return;
  const c=it.c;let i=2;while(CART[c+"#"+i])i++;
  const nk=c+"#"+i,o=OPT[k]||{};
  OPT[nk]={sp:o.sp||0,nc:!!o.nc,ex:(o.ex||[]).slice()};
  it.q--;
  const next={};
  for(const key of cKeys()){next[key]=CART[key];if(key===k)next[nk]={c:c,q:1}}
  CART=next;OEDIT={};OEDIT[nk]=true;
  cartSave();syncCart()}
let OEDIT={};
const chipBtn=(d,label,on)=>`<button class="chip" type="button" data-opt="${d}" aria-pressed="${on}">${esc(label)}</button>`;
function optUI(k){
  const c=codeOf(k),o=OPT[k]||{},ct=CT[L],out=[];
  if(POT(c)){
    out.push(`<div class="opt"><span class="qlab">${ct.spice}</span>${SP.map((x,i)=>chipBtn(`sp|${k}|${i}`,x[LI[L]],(o.sp||0)===i)).join("")}</div>`);
    out.push(`<div class="opt"><span class="qlab">${ct.extras}</span>${EXTRAS.map((e,i)=>chipBtn(`ex|${k}|${i}`,nm(e[0])+" +"+eur(e[1],L),exList(k).includes(i))).join("")}</div>`)}
  if(CORI.includes(c))out.push(`<div class="opt">${chipBtn(`nc|${k}|0`,ct.noCo,!!o.nc)}</div>`);
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
const cTotal=()=>cKeys().reduce((n,k)=>n+CART[k].q*itPrice(k),0);
const grpOf=it=>it.dr||FRONT.includes(it.c)?"f":"k";
const zhLines=()=>{const seen={},out=[];
  for(const k of cKeys()){const it=CART[k];
    const r={n:itName(it,"zh"),q:it.q,o:optTxt(k,"zh").join(" · "),g:grpOf(it),
             n2:itName(it,L),o2:optTxtUI(k,L).join(" · ")};
    const id=r.g+"\u0000"+r.n+"\u0000"+r.o;
    if(seen[id])seen[id].q+=r.q;else out.push(seen[id]=r)}
  return out};
// 按出餐分组，空的那组不出现
const zhGroups=()=>{const ls=zhLines();
  return ["k","f"].map(g=>({g:g,lab:GRP[g],rows:ls.filter(x=>x.g===g)})).filter(x=>x.rows.length)};
function cartBump(k,n,ds){
  if(n<0&&!CART[k]){const vs=cKeys().filter(x=>x.indexOf(k+"#")===0);if(vs.length)k=vs[vs.length-1]}
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
    const q=el.dataset.raw?lineQ(el.dataset.k):dishQ(el.dataset.k);
    el.classList.toggle("has",q>0);
    const o=el.querySelector(".qn");if(o)o.textContent=q});
  document.querySelectorAll("#menu .dish").forEach(el=>{const c=el.id.slice(2);
    el.classList.toggle("picked",!!(dishQ(c)||CART[c+"|s"]||CART[c+"|l"]))});
  document.querySelectorAll("[data-opt]").forEach(b=>{const[kind,k,i]=b.dataset.opt.split("|");const o=OPT[k]||{};
    b.setAttribute("aria-pressed",kind==="sp"?(o.sp||0)===+i:kind==="nc"?!!o.nc:exList(k).includes(+i))});
  $("cartbar").hidden=!n;document.body.classList.toggle("hascart",!!n);
  if(n){$("cb-n").textContent=n===1&&ct.item1?ct.item1:ct.items.replace("%s",n);$("cb-t").textContent=eur(cTotal(),L);$("cb-go").textContent=ct.view}
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
  const chip=(o,ds)=>`<button class="chip" type="button" data-q="1" data-k="${o.k}" ${ds}>${esc(pickName(o))} +${eur(pickPrice(o),L)}</button>`;
  const more=(kind,lab)=>`<button class="chip more" type="button" data-more="${kind}|*">${esc(lab)}</button>`;
  return `<div class="addon">
    <b>${esc(ct.addT)}</b>
    <div class="opt">${sides.map(o=>chip(o,`data-c="${o.c}" data-sz="${o.sz||""}"`)).join("")}${more("sd",ct.otherSide)}${drinks.length?"":more("dr",ct.otherDrink)}</div>
    ${drinks.length?`<b>${esc(ct.addD)}</b><div class="opt">${drinks.map(o=>chip(o,`data-dr="${o.dr}" data-dv="${o.dv}"`)).join("")}${more("dr",ct.otherDrink)}</div>`:""}</div>`;
}
function renderOrder(){
  const ct=CT[L],ks=cKeys();
  const rows=ks.map(k=>{const it=CART[k];
    const o=optTxtUI(k,L).join(" · ");
    const ed=hasOpt(it)?`<button class="on-edit" type="button" data-oedit="${k}" aria-expanded="${!!OEDIT[k]}">${o?esc(o)+" · "+esc(ct.optEdit):esc(ct.canNoCo)} <span class="ar">${OEDIT[k]?"▾":"›"}</span></button>${OEDIT[k]?`<div class="on-opts">${optUI(k)}${it.q>1?`<button class="chip split" type="button" data-split="${k}">${esc(ct.splitOne)}</button>`:""}</div>`:""}`:(o?`<em class="on-o">${esc(o)}</em>`:"");
    return `<li><div class="on-r"><div class="on-n">${esc(itName(it,L))}</div>
      ${stepper(k,"",1)}<div class="on-p">${eur(it.q*itPrice(k),L)}</div></div>${ed}</li>`}).join("");
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
      <button class="obtn sec" type="button" id="oclear">${esc(ct.clear)}</button></div>
    <div class="egg">${chopBlock()}${slipBlock()}</div>`
    :`<p class="ohint">${esc(ct.empty)}</p>`}
  </div>`;
  $("oclose").onclick=closeOrder;
  initScratch();
  if(!ks.length)return;
  $("ostaff").onclick=openStaff;
  $("oclear").onclick=()=>{CART={};cartSave();syncCart()};
  $("ocopy").onclick=e=>{const b=e.currentTarget;
    const done=()=>{b.textContent=CT[L].copied;setTimeout(()=>{if(!$("order").hidden)b.textContent=CT[L].copy},1500)};
    try{navigator.clipboard.writeText(orderText()).then(done,()=>{})}catch(_){}};
}
// 饭后签：一次来店只抽一张，六小时后算下一顿（只记在这台手机上）
const SKEY="sibisi.slip",SWIN=60e3;   // 抽到的签一直留着，SWIN 只管多久能再抽一张
const slipSeen=()=>store.get("sibisi.ordered")==="1";
const slipDeck=()=>L==="zh"?SAYING:HANZI;   // 中文客人抽中国话，其他语言抽菜单上的汉字
function slipGot(){
  try{const r=JSON.parse(store.get(SKEY)||"null");if(r&&r.i!=null)return r}catch(e){}
  return null}
const canDraw=()=>{const g=slipGot();return !g||Date.now()-g.t>=SWIN};
let SLIPT=null;
function drawSlip(){
  const n=slipDeck().length,had=slipGot();
  let i=Math.floor(Math.random()*n);
  if(had&&n>1&&i===had.i)i=(i+1+Math.floor(Math.random()*(n-1)))%n;
  store.set(SKEY,JSON.stringify({i:i,t:Date.now()}))}
// 两副牌一样长，换语言时同一次抽到的是对应的那一张
function slipCard(){
  const t=T[L],g=slipGot();if(!g)return "";
  const deck=slipDeck(),x=deck[g.i%deck.length];
  const inner=(x.m
    ?`<div class="slipcard say"><b>${esc(x.zh)}</b><p>${esc(x.m)}</p>
       <div class="sayes"><dt>${esc(t.sayEs)}</dt>${esc(x.es)}</div></div>`
    :`<div class="slipcard"><b>${esc(x.c)}</b><i>${esc(x.py)}</i><p>${esc(x[L])}</p></div>`);
  if(!g.rv)return `<div class="slipwrap">${inner}<canvas class="scratch"></canvas></div>`;
  return inner
    +(canDraw()?`<button class="chip more" type="button" data-slip="1">${esc(t.slipAgain)}</button>`
               :`<small class="slipone">${esc(t.slipOnce)}</small>`)}
// 刮刮卡：按住擦掉涂层，擦掉一半自动全开
// 单子和店员页可能同时各有一张，全都要接上
function initScratch(){document.querySelectorAll(".scratch:not([data-on])").forEach(setupScratch)}
function setupScratch(c){
  const wrap=c.parentNode,r=wrap.getBoundingClientRect(),w=Math.round(r.width),h=Math.round(r.height);
  if(!w||!h){requestAnimationFrame(()=>setupScratch(c));return}
  c.dataset.on="1";
  const dpr=Math.min(devicePixelRatio||1,2);
  c.width=w*dpr;c.height=h*dpr;c.style.width=w+"px";c.style.height=h+"px";
  const x=c.getContext("2d");x.scale(dpr,dpr);
  const g1=x.createLinearGradient(0,0,w,h);
  g1.addColorStop(0,"#d4482f");g1.addColorStop(1,"#a8381f");
  x.fillStyle=g1;x.fillRect(0,0,w,h);
  x.strokeStyle="rgba(255,255,255,.10)";x.lineWidth=11;
  for(let i=-h;i<w+h;i+=24){x.beginPath();x.moveTo(i,0);x.lineTo(i+h,h);x.stroke()}
  x.fillStyle="rgba(255,255,255,.95)";x.textAlign="center";
  x.font='800 15px '+getComputedStyle(document.body).fontFamily;
  x.fillText(T[L].scratch,w/2,h/2+5);
  x.globalCompositeOperation="destination-out";
  x.fillStyle="#000";x.strokeStyle="#000";x.lineCap="round";x.lineJoin="round";
  let down=false,last=null,n=0,done=false;
  const at=e=>{const b=c.getBoundingClientRect();return [e.clientX-b.left,e.clientY-b.top]};
  const blob=p=>{x.beginPath();x.arc(p[0],p[1],21,0,6.3);x.fill()};
  const cleared=()=>{const d=x.getImageData(0,0,c.width,c.height).data;
    let a=0,b=0;for(let i=3;i<d.length;i+=4*24){b++;if(d[i]<40)a++}return a/b};
  const finish=()=>{if(done)return;done=true;
    c.classList.add("gone");
    const g=slipGot()||{};g.rv=1;store.set(SKEY,JSON.stringify(g));
    setTimeout(()=>{if(!$("order").hidden)renderOrder();if(!$("staff").hidden)renderStaff()},420)};
  c.addEventListener("pointerdown",e=>{down=true;last=at(e);blob(last);
    try{c.setPointerCapture(e.pointerId)}catch(_){}
    e.preventDefault()});
  c.addEventListener("pointermove",e=>{if(!down)return;
    const p=at(e);x.lineWidth=42;x.beginPath();x.moveTo(last[0],last[1]);x.lineTo(p[0],p[1]);x.stroke();
    last=p;if(++n%8===0&&cleared()>.45)finish();
    e.preventDefault()});
  const up=()=>{if(!down)return;down=false;if(cleared()>.42)finish()};
  c.addEventListener("pointerup",up);c.addEventListener("pointercancel",up);
}
const slipArt=()=>`<svg class="eggart" viewBox="0 0 56 56" fill="none" aria-hidden="true">
 <g transform="rotate(-7 27 30)"><rect x="11" y="11" width="32" height="38" rx="3" fill="#f6ecd6" stroke="#b9a582" stroke-width="1.6"/>
 <path d="M17 25h20M17 32h16M17 39h11" stroke="#c3ad87" stroke-width="1.7" stroke-linecap="round"/></g>
 <g transform="rotate(9 42 15)"><rect x="34" y="7" width="17" height="17" rx="3" fill="#d4482f"/>
 <rect x="38.5" y="11.5" width="8" height="8" rx="1" fill="none" stroke="#fff" stroke-width="1.7"/></g>
 <path d="M7 9l1.6 3.8L12.4 14.4 8.6 16 7 19.8 5.4 16 1.6 14.4 5.4 12.8z" fill="#e8a33d"/>
 <path d="M48 41l1.1 2.5 2.5 1.1-2.5 1.1L48 48.2l-1.1-2.5-2.5-1.1 2.5-1.1z" fill="#e8a33d"/></svg>`;
function slipBlock(){
  if(!slipSeen())return "";
  const t=T[L];
  return slipGot()?slipCard()
    :`<button class="eggcard" type="button" data-slip="1">${slipArt()}
       <span class="ect"><b>${esc(t.slipT)}</b><em>${esc(t.slipSub)}</em></span>
       <span class="ecgo">›</span></button>`}
function renderStaff(){
  // 中文给店员看，客人自己那门语言放小一号在下面，方便客人指着补充说明
  const sub=x=>L==="zh"?"":`<i class="sl">${esc(x.n2)}${x.o2?" · "+esc(x.o2):""}</i>`;
  $("staff").innerHTML=`<div class="sx"><span>${esc(CT.zh.staffNote)}</span><button type="button" id="sclose" aria-label="关闭">×</button></div>
   ${zhGroups().map(g=>`<h4 class="sg">${g.lab}</h4><ul>${g.rows.map(x=>`<li><span>${esc(x.n)}${x.o?`<em>${x.o}</em>`:""}${sub(x)}</span><b>×${x.q}</b></li>`).join("")}</ul>`).join("")}
   <div class="stot"><span>共 ${cCount()} 份</span><b>${eur(cTotal(),"es")}</b></div>
   <div class="sgift">${slipBlock()}</div>`;
  initScratch();
  $("sclose").onclick=closeStaff;
}
const orderText=()=>["Sibisi Ramen"].concat(
  ...zhGroups().map(g=>["【"+g.lab+"】"].concat(g.rows.map(x=>`${x.n}${x.o?"（"+x.o+"）":""} ×${x.q}`))),
  [`共 ${cCount()} 份　${eur(cTotal(),"es")}`]).join("\n");
function openOrder(){renderOrder();$("order").hidden=false;$("scrim").hidden=false;
  document.body.classList.add("ordering");document.body.style.overflow="hidden"}
function closeOrder(){$("order").hidden=true;$("scrim").hidden=true;
  document.body.classList.remove("ordering");document.body.style.overflow=""}
function openStaff(){store.set("sibisi.ordered","1");renderStaff();$("staff").hidden=false;document.body.style.overflow="hidden"}
function closeStaff(){$("staff").hidden=true;document.body.style.overflow=$("order").hidden?"":"hidden";
  if(!$("order").hidden)renderOrder()}   // 点过店员页之后，饭后签才会出现，得重画一次
$("cb-go").addEventListener("click",openOrder);
$("totop").addEventListener("click",()=>scrollTo({top:0,behavior:"smooth"}));
const topBtn=()=>{$("totop").hidden=scrollY<700};
addEventListener("scroll",topBtn,{passive:true});topBtn();
// 来过的人打开菜单时换一句招呼（只存在这台手机上）
let BACK=false;
(function(){try{
  const r=JSON.parse(store.get("sibisi.v")||"null")||{n:0,t:0};
  if(Date.now()-r.t>2*36e5){BACK=r.n>0;r.n++;r.t=Date.now();store.set("sibisi.v",JSON.stringify(r))}
  else BACK=r.n>1;
}catch(e){}})();
(function(){let l=new URLSearchParams(location.search).get("l")||store.get("lang");
 if(!l){const n=(navigator.language||"es").slice(0,2);l=n==="zh"?"zh":(n==="es"||n==="ca")?"es":"en"}
 L=T[l]?l:"es";render()})();
