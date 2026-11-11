// ===================== V3 : ton « banger », réseau réel des liens Minato ↔ Itachi =====================
const MONO="JB";
function mono(s,px,py,size,{c=INK,al='left',a=1,rot=0,w=500}={}){txt(s,px,py,size,{f:MONO,w,c,al,a,rot})}
const NET=JSON.parse(document.getElementById('net').textContent);
const CONST=JSON.parse(document.getElementById('const').textContent);
const SUBS=[[0.15,3.5,"Votre gars Itachi, c'est *un ouf.* Sharingan, Tsukuyomi… il plie la moitié du verse."],
 [3.6,6.9,"Mais face à *l'Éclair jaune de Konoha*… votre boug *n'est pas au niveau.*"],
 [7.0,12.7,"Et c'est pas un avis. J'ai mis *les 193 combats* du manga dans un modèle mathématique : qui a battu qui, quand, et à quel point."],
 [12.8,17.5,"Regarde. Minato tient tête au *Raikage ET à Killer B.* En même temps."],
 [17.6,21.1,"Ce Raikage-là *démonte Sasuke* au Sommet des Kage."],
 [21.2,24.9,"Killer B et Naruto, à deux, *prennent pas le dessus* sur Itachi."],
 [25.0,30.3,"Itachi l'avoue lui-même : contre *Jiraiya, le maître de Minato*, à deux ils y laisseraient la vie."],
 [30.4,33.9,"Et le Raikage le dit : sans Minato, *c'est lui le plus rapide du monde.*"],
 [34.0,39.9,"Ça, c'est 5 liens. Entre ces deux-là, le modèle en a *60.* Et il pèse chaque combat selon *le moment* où il a lieu."],
 [40.0,45.7,"Verdict, sur 4 000 combats simulés : *Minato 48 %.* Itachi 38 %. Le reste, match nul."],
 [45.8,49.9,"Votre gars est fort, hein : il bat *3 persos sur 4* de tout Naruto."],
 [50.0,55.4,"Mais face à Minato… il trouve plus fort. *Pas d'accord ?* Balance ton argument en commentaire, *je le passe dans le modèle.*"]];
const PORT={minato:'f_minato',itachi:'f_itachi',kakashi:'f_kakashi',obito:'f_obito',a4:'raikage_f',killer_b:'killer_f',madara:'p_madara',naruto:'p_naruto',sasuke:'p_sasuke',jiraiya:'p_jiraiya',orochimaru:'p_orochimaru',nagato:'p_nagato',kisame:'p_kisame'};
const key=(a,b)=>[a,b].sort().join('|');
// liens racontés : [début, fin, arêtes, couleur, légende, position de la légende, pointillé ?]
const TOLD=[[12.9,17.5,[['minato','a4'],['minato','killer_b']],GOLD,'TIENT TÊTE AUX DEUX',null,false],
 [17.7,21.1,[['a4','sasuke']],GOLD,'DÉMONTE SASUKE',null,false],
 [21.3,24.9,[['killer_b','itachi'],['naruto','itachi']],RED,'PAS LE DESSUS',null,false],
 [25.1,30.3,[['itachi','jiraiya'],['jiraiya','minato']],RED,'« À DEUX, ON Y RESTE »',null,true],
 [30.5,33.9,[['a4','minato']],GOLD,'PLUS RAPIDE QUE LE RAIKAGE',null,true]];
const NP=n=>NET.nodes[n];
function edgePts(a,b,bend){const A=NP(a),B=NP(b);const mx=(A[0]+B[0])/2+(B[1]-A[1])*bend,my=(A[1]+B[1])/2-(B[0]-A[0])*bend;return [[A[0],A[1]],[mx,my],[B[0],B[1]]]}
function curvePts(a,b,bend,n=24){const [P0,P1,P2]=edgePts(a,b,bend);const out=[];for(let i=0;i<=n;i++){const u=i/n;out.push([(1-u)*(1-u)*P0[0]+2*(1-u)*u*P1[0]+u*u*P2[0],(1-u)*(1-u)*P0[1]+2*(1-u)*u*P1[1]+u*u*P2[1]])}return out}
function dashedCurve(pts,p,col,wd){const n=Math.floor((pts.length-1)*p);for(let i=0;i<n;i+=2)brush([pts[i],pts[i+1]],1,wd,col,i)}

function network(t,a){if(a<=0)return;x.save();x.globalAlpha*=a;const tq=q12(t);
  // toutes les arêtes (combats) se dessinent très vite, puis restent en gris encre
  NET.edges.forEach(([u,v],i)=>{const t0=13.0+i*.025;const p=eo(seg(t,t0,t0+.35));if(p<=0)return;const told=TOLD.some(([a0,a1,es])=>t>=a0&&es.some(e=>key(...e)===key(u,v)));
    x.save();x.globalAlpha*=told?1:.42;brush(curvePts(u,v,.08),p,told?0:5,INK,i);x.restore()});
  // pulsation des 60 chemins (scène « 60 »)
  if(t>34.2&&t<39.9){const k=win(t,34.3,39.9,.3,.3);const f=Math.floor(t*10);NET.edges.forEach(([u,v],i)=>{if(hash(i*3.1+f)<.35){x.save();x.globalAlpha*=k*.9;brush(curvePts(u,v,.08),1,7,hash(i+f)<.5?GOLD:RED,i+f);x.restore()}})}
  // liens racontés
  TOLD.forEach(([a0,a1,es,col,lab,_,dash])=>{if(t<a0)return;const live=t<a1+.3;const p=eo(seg(t,a0+.1,a0+.7));es.forEach(([u,v],j)=>{const pts=curvePts(u,v,dash?-.14:.08);x.save();x.globalAlpha*=live?1:.55;if(dash)dashedCurve(pts,p,col,10);else brush(pts,p,live?13:8,col,j+a0)
      ;x.restore()});
    if(live)stamp(lab,W/2,1360,lab.length>20?46:58,col===GOLD?'#8a6400':col,a0+.35,t,-.04,'#fffaf0')});
  // nœuds
  Object.entries(NET.nodes).forEach(([n,[px,py,name]])=>{const big=n==='minato'||n==='itachi';const tIn=big?12.8:13.0+NET.order[n]*.25+hash(px)*.2;const k=back(seg(tq,tIn,tIn+.25));if(k<=0)return;
    const hot=TOLD.some(([a0,a1,es])=>t>=a0&&t<a1+.3&&es.some(e=>e.includes(n)));const R=big?92:(PORT[n]?52:40);x.save();x.translate(px,py);x.scale(k*(hot&&!big?1.18:1),k*(hot&&!big?1.18:1));
    x.beginPath();x.arc(0,0,R,0,7);x.fillStyle=n==='minato'?GOLD:n==='itachi'?RED:'#e7dcc4';x.fill();
    if(PORT[n]&&IMG[PORT[n]]){x.save();x.beginPath();x.arc(0,0,R-7,0,7);x.clip();const im=IMG[PORT[n]];const sc=2*(R-7)/Math.min(im.width,im.height);x.drawImage(im,-im.width*sc/2,-im.height*sc/2,im.width*sc,im.height*sc);x.restore()}
    else txt(name.slice(0,1),0,14,42,{c:INK});
    x.lineWidth=big?10:6;x.strokeStyle=INK;x.beginPath();x.arc(0,0,R,0,7);x.stroke();x.restore();
    txt(big?name.toUpperCase():name,px,py+R*k+(big?44:30),big?40:24,{f:big?'Dela':'Zen',w:900,c:n==='minato'?'#8a6400':n==='itachi'?RED:INK,stroke:big?0:5,sc:PAPER})});
  x.restore()}

function renderAt(T){
  const t=T,tq=q12(T);x.setTransform(1,0,0,1,0,0);
  if(IMG.paper)x.drawImage(IMG.paper,0,0,W,H);else{x.fillStyle=PAPER;x.fillRect(0,0,W,H)}
  let shake=0;[1.9,3.65,13.0,41.6,52.2].forEach(s=>{const u=t-s;if(u>=0&&u<.32)shake=Math.max(shake,1-u/.32)});const sx=(hash(Math.floor(t*24))-.5)*28*shake,sy=(hash(Math.floor(t*24)+9)-.5)*20*shake;x.translate(sx,sy);

  // ---- 0-3,6 s : « Votre gars Itachi, c'est un ouf »
  if(t<3.75){const a=1-seg(t,3.6,3.75);
    panel(40,170,1000,1380,(w,h)=>{x.fillStyle=INK;x.fillRect(0,0,w,h);speedLines(w/2,h*.45,360,96,tq,PAPER,.9);pic('itachi_front',w/2,h*.6+lerp(240,0,eo(seg(tq,0,.5))),1180,{boil:3,t:tq})},{a,rot:-.012});
    sfx('ゴゴゴ',930,330,100,RED,t,a*seg(t,.1,.3),true);
    txt('VOTRE GARS ITACHI,',W/2,300,74,{c:PAPER,stroke:14,sc:INK,a:a*seg(tq,.1,.25),rot:-.03});
    const k=back(seg(tq,1.0,1.25));x.save();x.translate(W/2,1300);x.rotate(-.05);x.scale(lerp(2.4,1,k),lerp(2.4,1,k));txt("C'EST UN OUF.",0,0,100,{c:RED,stroke:22,sc:INK,a:a*cl(k)});x.restore();
    ['SHARINGAN','TSUKUYOMI','SUSANOO'].forEach((s,i)=>{const k2=back(seg(tq,1.9+i*.35,2.15+i*.35));if(k2>0){x.save();x.translate(220+i*320,1440);x.rotate((i-1)*.06);x.scale(k2,k2);mono(s,0,0,34,{al:'center',c:PAPER,w:700});x.restore()}})}
  // ---- 3,6-7 s : l'Éclair jaune arrive
  if(t>3.55&&t<7.1){const a=win(t,3.6,7.1,.02,.2);const kp=seg(t,3.55,3.75);if(kp<1)pic('kunai',lerp(-200,1300,kp),lerp(1500,500,kp),240,{rot:-.6});
    panel(40,170,1000,1380,(w,h)=>{x.fillStyle='#f4d78a';x.fillRect(0,0,w,h);speedLines(w*.55,h*.42,280,100,tq,INK,.7);pic('minato_fight',w*.5+lerp(500,0,eo(seg(tq,3.7,4.0))),h*.45,980,{boil:3,t:tq})},{a,rot:.01});
    txt("L'ÉCLAIR JAUNE",W/2,300,84,{c:GOLD,stroke:16,sc:INK,a:a*seg(tq,3.8,4.0),rot:-.03});
    stamp('PAS AU NIVEAU.',W/2,1330,90,RED,5.4,t,-.07,'#fffaf0');sfx('ドン',880,560,150,RED,t,win(t,3.7,6.5,.05,.3))}
  // ---- 7-12,8 s : la méthode en deux phrases (tous les combats du manga à l'encre)
  if(t>6.9&&t<12.9){const a=win(t,7.0,12.9,.15,.2);x.save();x.globalAlpha=a;
    const N=CONST.N,E=CONST.E,ord=CONST.order;const CX0=90,CX1=990,CY0=380,CY1=1180;const P=N.map(([ar,m,c])=>[CX0+(ar+.12+.76*hash(c.length*7.7+ar))/CONST.narcs*(CX1-CX0),CY1-(m+1)/10*(CY1-CY0)]);
    const shown=Math.floor(eo(seg(t,7.3,10.5))*E.length);for(let r=0;r<shown;r++){const e=E[ord[r]];const A=P[e[0]],B=P[e[1]];x.strokeStyle=r>shown-8?RED:'rgba(24,20,15,.55)';x.lineWidth=r>shown-8?4:2;x.beginPath();x.moveTo(A[0],A[1]);x.quadraticCurveTo((A[0]+B[0])/2,(A[1]+B[1])/2-30,B[0],B[1]);x.stroke()}
    P.forEach(([px,py])=>{x.fillStyle=INK;x.beginPath();x.arc(px,py,4,0,7);x.fill()});
    mono('combats codés : '+String(Math.min(193,Math.round(193*shown/E.length))).padStart(3,'0'),70,330,40,{w:700});
    [['QUI A BATTU QUI',9.6,300,1270,-.05],['QUAND',10.6,590,1310,.04],['À QUEL POINT',11.4,820,1250,-.03]].forEach(([s,t0,px,py,r])=>stamp(s,px,py,40,RED,t0,t,r,'#fffaf0'));
    mono('P(A > B) = σ(k·(sA − sB))',600,330,26,{c:GREY,a:seg(t,8,8.4)});x.restore()}
  // ---- 12,8-40 s : le réseau réel des liens
  const nA=t>12.7&&t<40.1?win(t,12.8,40.1,.15,.25):0;
  if(nA>0){network(t,nA);mono('tous les combats qui relient Minato et Itachi',W/2,300,28,{al:'center',w:700,a:nA*seg(t,13.2,13.6)});
    if(t>34){const a=win(t,34.1,40,.2,.25);[['5','LIENS RACONTÉS',INK],['60','CHEMINS DANS LE MODÈLE',RED],['193','COMBATS AU TOTAL',INK]].forEach(([n,l,c],i)=>{const t0=34.4+i*1.2;if(t<t0)return;stamp(n,180+i*360,1390,72,c,t0,t,(i-1)*.05,'#fffaf0');txt(l,180+i*360,1480,24,{f:'Zen',w:900,a})});
      mono('chaque combat est daté : le Kakashi de la partie 1 ≠ celui de la guerre',W/2,1555,24,{al:'center',c:GREY,a:seg(t,37.2,37.6)})}}
  // ---- 40-45,8 s : 4 000 combats simulés + jauge
  if(t>39.9&&t<45.9){const a=win(t,40,45.9,.2,.25);x.save();x.globalAlpha=a;const n=Math.round(4000*eo(seg(t,40.2,43.4)));mono('combats simulés : '+String(n).padStart(4,'0')+' / 4000',W/2,300,40,{al:'center',w:700});
    const cols=[[230,GOLD,'MINATO',.48],[540,GREY,'NUL',.14],[850,RED,'ITACHI',.38]];const R=rngS(5);const cnt=[0,0,0];
    for(let i=0;i<300;i++){const r=R();const b=r<.48?0:r<.62?1:2;const t0=40.3+i*.009;const u=seg(t,t0,t0+.4);if(u<=0)continue;const k=cnt[b]++;const cx=cols[b][0]+((k%12)-5.5)*19,cy=1150-Math.floor(k/12)*19;
      const px=lerp(W/2+(hash(i)-.5)*700,cx,eio(u)),py=lerp(380,cy,u*u);x.fillStyle=cols[b][1];x.beginPath();x.arc(px,py,8.5,0,7);x.fill()}
    cols.forEach(([cx,c,l,p])=>{txt(l,cx,1230,40,{c,stroke:8,sc:INK});txt(Math.round(p*100*seg(t,40.4,43.4))+' %',cx,1150-Math.ceil(p*300/12)*19-20,64,{c:INK})});
    stamp('VERDICT : MINATO',W/2,520,76,RED,41.6,t,-.06,'#fffaf0');x.restore()}
  // ---- 45,8-50 s : respect
  if(t>45.7&&t<50.1){const a=win(t,45.8,50.1,.2,.2);x.save();x.globalAlpha=a;pic('itachi_front',W/2,820,820,{boil:2,t:tq});enso(W/2,700,320,eo(seg(t,46,47.4))*.75,RED,44);
    txt('75 %',W/2,1330,150,{c:RED,stroke:22,sc:INK,a:seg(tq,46.9,47.2)});txt('du casting battu par Itachi',W/2,1410,40,{f:'Zen',w:900,a:seg(tq,47.1,47.4)});x.restore()}
  // ---- 50-55,5 s : « il trouve plus fort » + appel
  if(t>49.9&&t<55.6){const a=win(t,50,55.6,.15,.3);
    panel(40,170,1000,1380,(w,h)=>{x.fillStyle='#f4d78a';x.fillRect(0,0,w,h);speedLines(w*.5,h*.45,300,90,tq,INK,.55);pic('minato_fight',w*.5,h*.5,900,{boil:3,t:tq})},{a,rot:-.01});
    const k=back(seg(tq,52.2,52.45));x.save();x.translate(W/2,300);x.rotate(-.04);x.scale(lerp(2,1,k),lerp(2,1,k));txt("PAS D'ACCORD ?",0,0,96,{c:PAPER,stroke:18,sc:INK,a:cl(k)});x.restore();
    if(t>53){x.save();x.translate(W/2,1380);x.rotate(.02);x.fillStyle='#fffaf0';x.globalAlpha=seg(t,53,53.3);x.fillRect(-440,-60,880,96);x.lineWidth=7;x.strokeStyle=INK;x.strokeRect(-440,-60,880,96);mono('ton argument → commentaire → modèle',0,6,36,{al:'center',w:700});x.restore()}}
  // ---- 55,5-58 s : carte de fin, puis boucle
  if(t>55.4){const a=seg(t,55.5,55.8);x.save();x.globalAlpha=a;x.fillStyle=INK;x.fillRect(0,0,W,H);txt('LE VERDICT',W/2,880,120,{c:PAPER});mono('Itachi vs Madara : la prochaine',W/2,980,36,{al:'center',c:GOLD,w:700,a:seg(t,56,56.3)});x.restore()}

  // marque + sous-titres + impacts
  x.setTransform(1,0,0,1,sx,sy);if(t<55.5){txt('LE VERDICT',60,120,52,{al:'left',c:INK});mono('193 combats · modèle bayésien',62,150,22,{c:GREY});x.save();x.translate(1000,104);x.rotate(.08);x.fillStyle=RED;x.fillRect(-34,-34,68,68);txt('V',0,20,52,{c:PAPER});x.restore()}
  subtitle(t);
  [1.0,3.65,41.6,52.2].forEach(s=>{if(t>=s&&t<s+.08){x.setTransform(1,0,0,1,0,0);x.globalCompositeOperation='difference';x.fillStyle='#fff';x.fillRect(0,0,W,H);x.globalCompositeOperation='source-over'}});
}
