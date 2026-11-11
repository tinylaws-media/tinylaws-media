// ===================== V4 : dossiers Itachi / Minato, puis toile de tous les combats (rouge ↔ or) =====================
const MONO="JB";
function mono(s,px,py,size,{c=INK,al='left',a=1,rot=0,w=500}={}){txt(s,px,py,size,{f:MONO,w,c,al,a,rot})}
const WEB=JSON.parse(document.getElementById('web').textContent);
const CONST=JSON.parse(document.getElementById('const').textContent);
const P_MI=.45,P_D=.14,P_IT=.41;
const SUBS=[[0.15,3.4,"Votre gars Itachi, c'est *un ouf.* Sharingan, Tsukuyomi, Susanoo…"],
 [3.5,6.8,"Mais face à *l'Éclair jaune de Konoha*… votre boug *n'est pas au niveau.*"],
 [6.9,11.6,"Et c'est pas un avis. J'ai mis *les 193 combats* du manga dans un modèle mathématique : qui bat qui, quand, et à quel point."],
 [11.7,14.6,"D'abord, respect. Itachi débarque à Konoha : *Kakashi, Tsukuyomi.* Plié en une seconde."],
 [14.7,17.6,"Orochimaru veut lui voler son corps ? *Il ressort sans sa main.*"],
 [17.7,21.0,"Pendant la guerre, Nagato revient d'entre les morts : *Itachi le scelle.*"],
 [21.1,25.0,"Sa seule vraie défaite ? *Sasuke.* Et encore : Itachi était *malade*, et il se retenait."],
 [25.1,28.6,"Maintenant, Minato. 3e guerre : il tient tête au *Raikage ET à Killer B.* En même temps."],
 [28.7,32.4,"La nuit de Kyûbi, l'homme masqué contrôle le démon : *Minato le bat*, et libère Kurama."],
 [32.5,36.0,"Sa défaite ? Obito devenu *jinchûriki de Jûbi*… contre *quatre Hokage* à la fois."],
 [36.1,40.5,"Mais ça, c'est que leurs combats à eux. Le modèle, lui, *relie tout le monde.*"],
 [40.6,45.0,"En rouge, tout ce qu'Itachi a touché. En or, *tout ce que Minato a touché.* Combat après combat."],
 [45.1,49.5,"Et partout où ça se croise, *le modèle compare.* 122 persos, 250 liens, chacun *daté.*"],
 [49.6,55.0,"Verdict, sur 4 000 combats simulés : *Minato 45 %. Itachi 41 %.* Le reste, nul."],
 [55.1,59.0,"C'est serré, je te l'accorde. *Mais serré… ça reste Minato.*"],
 [59.1,62.8,"Et respect quand même : Itachi bat *3 persos sur 4* de tout Naruto."],
 [62.9,67.4,"Pas d'accord ? *Balance ton argument en commentaire*, je le passe dans le modèle."]];

// ---------- trame de points (fond de case)
function dots(w,h,col,step=18,r=3){x.fillStyle=col;for(let yy=0;yy<h;yy+=step)for(let xx=((yy/step)%2?step/2:0);xx<w;xx+=step){x.beginPath();x.arc(xx,yy,r,0,7);x.fill()}}

// ---------- un combat du dossier : case du héros en haut, case de l'adversaire en bas, tampon au milieu
// o = {hero:'itachi'|'minato', hp: image du héros, foes:[[img,dx,h,flip]], bg: fond adversaire, name, ref, res, resCol, loss}
function bout(t,t0,t1,o){if(t<t0-.05||t>t1+.05)return;const tq=q12(t),a=win(t,t0,t1,.06,.12);const it=o.hero==='itachi';const hc=it?RED:GOLD;
  // case du héros (entre depuis la gauche)
  const kh=eo(seg(tq,t0,t0+.3));
  panel(40+lerp(-1100,0,kh),280,1000,620,(w,h)=>{x.fillStyle=it?INK:'#f4d78a';x.fillRect(0,0,w,h);speedLines(w*.5,h*.5,260,80,tq,it?hc:INK,.75);
    pic(o.hp,w*.5+lerp(-120,0,eo(seg(tq,t0,t0+.6))),h*.62,h*1.35,{boil:3,t:tq,flip:o.hflip})},{a,rot:-.018});
  // case de l'adversaire (entre depuis la droite, un poil après)
  const kf=eo(seg(tq,t0+.15,t0+.45));
  panel(40+lerp(1100,0,kf),930,1000,630,(w,h)=>{if(o.bg&&IMG[o.bg]){cover(o.bg,w,h);x.fillStyle='rgba(239,230,210,.55)';x.fillRect(0,0,w,h)}else{x.fillStyle=PAPER;x.fillRect(0,0,w,h)}dots(w,h,'rgba(24,20,15,.16)');
    o.foes.forEach(([n,dx,hh,fl],i)=>pic(n,w*.5+dx+lerp(160,0,eo(seg(tq,t0+.2+i*.12,t0+.7+i*.12))),h*.6,hh,{boil:2,t:tq,flip:fl}));
    if(o.loss){x.fillStyle='rgba(179,18,30,.18)';x.fillRect(0,0,w,h)}
    box(o.name,30+o.name.length*12,58,{size:38,a:seg(tq,t0+.4,t0+.55),rot:-.02,bg:it?'#fffaf0':'#fff6dc'});mono(o.ref,w-24,h-24,24,{al:'right',c:INK,a:seg(tq,t0+.5,t0+.65)})},{a,rot:.014});
  // éclair diagonal + tampon du résultat
  if(t>t0+.55){x.save();x.globalAlpha=a;brush([[60,960],[540,900],[1020,850]],eo(seg(t,t0+.55,t0+.75)),26,o.resCol,t0);x.restore()}
  stamp(o.res,W/2,915,o.res.length>14?54:70,o.resCol,t0+.8,t,o.loss?.05:-.06,'#fffaf0');
  if(o.sfx)sfx(o.sfx,900,1120,120,o.resCol,t,a*seg(t,t0+.85,t0+1))}

// en-tête du dossier + bilan qui se remplit
function dossier(t,who,t0,t1,beats){const a=win(t,t0,t1,.1,.15);if(a<=0)return;const it=who==='itachi';
  x.save();x.globalAlpha=a;x.fillStyle=INK;x.fillRect(40,190,1000,70);txt('DOSSIER '+who.toUpperCase(),70,245,46,{al:'left',c:it?RED:GOLD});
  beats.forEach(([tb,r],i)=>{if(t<tb+.8)return;const k=back(seg(t,tb+.8,tb+1));x.save();x.translate(760+i*68,225);x.scale(k,k);x.fillStyle=r==='V'?(it?RED:GOLD):r==='N'?GREY:PAPER;x.fillRect(-28,-28,56,56);
    txt(r,0,14,40,{c:r==='D'?INK:PAPER});x.restore()});x.restore()}

// ---------- la toile : tous les combats du manga
const WN=WEB.nodes,WE=WEB.edges;
const HOP0=41.0,HOPD=.62;                         // départ de la propagation, durée d'un saut
const tI=n=>HOP0+WN[n][3]*HOPD,tM=n=>HOP0+WN[n][4]*HOPD;
const WPORT={itachi:'f_itachi',minato:'f_minato',kakashi:'f_kakashi',obito:'f_obito',a4:'raikage_f',killer_b:'killer_f',madara:'p_madara',naruto:'p_naruto',sasuke:'p_sasuke',jiraiya:'p_jiraiya',orochimaru:'p_orochimaru',nagato:'p_nagato',kisame:'p_kisame',hashirama:'p_hashirama',gai:'p_gai',tsunade:'p_tsunade'};
function wcurve(u,v,n=14){const A=WN[u],B=WN[v];const b=(hash(A[0]+B[1])-.5)*.25;const mx=(A[0]+B[0])/2+(B[1]-A[1])*b,my=(A[1]+B[1])/2-(B[0]-A[0])*b;const out=[];
  for(let i=0;i<=n;i++){const s=i/n;out.push([(1-s)*(1-s)*A[0]+2*(1-s)*s*mx+s*s*B[0],(1-s)*(1-s)*A[1]+2*(1-s)*s*my+s*s*B[1]])}return out}
const WC=WE.map(([u,v])=>[wcurve(u,v)]);
const EORD=WE.map((e,i)=>i).sort((i,j)=>{const d=k=>Math.hypot(WN[WE[k][0]][0]-540,WN[WE[k][0]][1]-930);return d(i)-d(j)});
const ERANK={};EORD.forEach((e,r)=>ERANK[e]=r);
function line(pts,p,col,wd){if(p<=0)return;const n=Math.max(1,Math.round((pts.length-1)*cl(p)));x.strokeStyle=col;x.lineWidth=wd;x.lineCap='round';x.beginPath();x.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<=n;i++)x.lineTo(pts[i][0],pts[i][1]);x.stroke()}
// une couleur se propage le long d'une arête depuis l'extrémité la plus proche de sa source
function shift(pts,i,o){const [u,v]=WE[i];const A=WN[u],B=WN[v];const L=Math.hypot(B[0]-A[0],B[1]-A[1])||1;const nx=-(B[1]-A[1])/L*o,ny=(B[0]-A[0])/L*o;return pts.map(([a,b])=>[a+nx,b+ny])}
const WCR=WC.map(([f],i)=>[shift(f,i,3.2)]),WCG=WC.map(([f],i)=>[shift(f,i,-3.2)]);
function spread(t,i,hk,tf,col,wd){const pts=(hk===3?WCR:WCG)[i][0];const [u,v]=WE[i];const hu=WN[u][hk],hv=WN[v][hk];
  if(hu===hv){const p=seg(t,tf(u),tf(u)+HOPD);if(p>0){const m=Math.floor(pts.length/2);line(pts.slice(0,m+1),p,col,wd);line(pts.slice(m).reverse(),p,col,wd)}return}
  const fromU=hu<hv;const p=seg(t,tf(fromU?u:v),tf(fromU?u:v)+HOPD);if(p<=0)return;line(fromU?pts:pts.slice().reverse(),p,col,wd)}
function web(t,a){if(a<=0)return;const tq=q12(t);x.save();x.globalAlpha*=a;
  // 1) la toile grise s'encre (du centre vers l'extérieur)
  WE.forEach((e,i)=>{const t0=36.3+ERANK[i]*.012;const p=eo(seg(t,t0,t0+.4));if(p<=0)return;line(WC[i][0],p,'rgba(24,20,15,.38)',2+Math.min(3,e[2]))});
  // 2) propagation rouge (Itachi) et or (Minato)
  if(t>HOP0){WE.forEach((e,i)=>{spread(t,i,3,tI,RED,4.5);spread(t,i,4,tM,GOLD,4.5)})}
  // 3) impulsions qui voyagent une fois tout allumé
  if(t>45){const f=t*.7;WE.forEach((e,i)=>{if(hash(i*1.7)<.55)return;const s=(f+hash(i))%1;const pts=WC[i][0];const k=Math.floor(s*(pts.length-1));const col=hash(i*2.3)<.5?RED:GOLD;x.fillStyle=col;x.beginPath();x.arc(pts[k][0],pts[k][1],6,0,7);x.fill()})}
  // 4) nœuds
  Object.entries(WN).forEach(([n,[px,py,name,hi,hm]],j)=>{const big=n==='itachi'||n==='minato';const tIn=big?36.15:36.4+Math.hypot(px-540,py-930)/700*1.6;const k=back(seg(tq,tIn,tIn+.25));if(k<=0)return;
    const ri=t>=tI(n)+.05,rm=t>=tM(n)+.05;const both=ri&&rm;const R=big?78:(WPORT[n]?30:11);
    // éclat là où les deux couleurs se rejoignent
    if(both&&!big){const tb=Math.max(tI(n),tM(n))+.05;const u=seg(t,tb,tb+.5);if(u<1){x.save();x.globalAlpha*=1-u;x.strokeStyle='#fff3c4';x.lineWidth=8;x.beginPath();x.arc(px,py,R+10+u*44,0,7);x.stroke();x.restore()}}
    x.save();x.translate(px,py);x.scale(k,k);x.beginPath();x.arc(0,0,R,0,7);
    x.fillStyle=n==='itachi'?RED:n==='minato'?GOLD:ri?RED:rm?GOLD:'#e7dcc4';x.fill();if(both&&!big){x.beginPath();x.moveTo(0,0);x.arc(0,0,R,-Math.PI/2,Math.PI/2);x.closePath();x.fillStyle=GOLD;x.fill()}
    if(WPORT[n]&&IMG[WPORT[n]]&&R>20){x.save();x.beginPath();x.arc(0,0,R-5,0,7);x.clip();const im=IMG[WPORT[n]];const sc=2*(R-5)/Math.min(im.width,im.height);x.drawImage(im,-im.width*sc/2,-im.height*sc/2,im.width*sc,im.height*sc);x.restore()}
    x.lineWidth=big?9:(R>20?5:3);x.strokeStyle=INK;x.beginPath();x.arc(0,0,R,0,7);x.stroke();x.restore();
  });
  ['itachi','minato'].forEach(n=>{const [px,py,name]=WN[n];const k=back(seg(tq,36.15,36.4));if(k>0)txt(name.toUpperCase(),px,py+78+48,42,{c:n==='minato'?'#8a6400':RED,stroke:12,sc:PAPER,a:cl(k)})});
  // compteurs
  if(t>HOP0){const cI=Object.keys(WN).filter(n=>t>=tI(n)).length,cM=Object.keys(WN).filter(n=>t>=tM(n)).length,cB=Object.keys(WN).filter(n=>t>=tI(n)&&t>=tM(n)).length;
    x.fillStyle='#fffaf0';x.fillRect(60,1500,960,92);x.lineWidth=6;x.strokeStyle=INK;x.strokeRect(60,1500,960,92);
    mono('ITACHI '+String(cI).padStart(3,'0'),100,1560,34,{c:RED,w:700});mono('MINATO '+String(cM).padStart(3,'0'),540,1560,34,{c:'#8a6400',w:700,al:'center'});mono('LES DEUX '+String(cB).padStart(3,'0'),980,1560,34,{c:INK,w:700,al:'right'})}
  x.restore()}

function renderAt(T){
  const t=T,tq=q12(T);x.setTransform(1,0,0,1,0,0);
  if(IMG.paper)x.drawImage(IMG.paper,0,0,W,H);else{x.fillStyle=PAPER;x.fillRect(0,0,W,H)}
  let shake=0;[1.0,3.65,12.5,15.5,18.5,21.9,25.9,29.5,33.3,51.8,64.2].forEach(s=>{const u=t-s;if(u>=0&&u<.32)shake=Math.max(shake,1-u/.32)});const sx=(hash(Math.floor(t*24))-.5)*28*shake,sy=(hash(Math.floor(t*24)+9)-.5)*20*shake;x.translate(sx,sy);

  // ---- 0-3,5 s : « Votre gars Itachi, c'est un ouf » — grosses cases qui surgissent
  if(t<3.75){const a=1-seg(t,3.6,3.75);
    panel(40,170,1000,1380,(w,h)=>{x.fillStyle=INK;x.fillRect(0,0,w,h);speedLines(w/2,h*.45,360,96,tq,PAPER,.9);pic('itachi_front',w/2,h*.6+lerp(240,0,eo(seg(tq,0,.5))),1180,{boil:3,t:tq})},{a,rot:-.012});
    [[1.7,'itachi_left',60,820,420,560,.05,'bg_tsukuyomi'],[2.3,'itachi_fight',600,760,430,600,-.04,null]].forEach(([t0,n,px,py,w,h,r,bg])=>{const k=back(seg(tq,t0,t0+.2));if(k<=0)return;x.save();x.translate(px+w/2,py+h/2);x.scale(k,k);x.translate(-px-w/2,-py-h/2);
      panel(px,py,w,h,(ww,hh)=>{if(bg)cover(bg,ww,hh);else{x.fillStyle=RED;x.fillRect(0,0,ww,hh)}speedLines(ww/2,hh/2,120,50,tq,INK,.5);pic(n,ww/2,hh*.62,hh*1.25,{boil:2,t:tq})},{a,rot:r,border:9});x.restore()});
    sfx('ゴゴゴ',930,330,100,RED,t,a*seg(t,.1,.3),true);
    txt('VOTRE GARS ITACHI,',W/2,300,74,{c:PAPER,stroke:14,sc:INK,a:a*seg(tq,.1,.25),rot:-.03});
    const k=back(seg(tq,1.0,1.25));x.save();x.translate(W/2,1440);x.rotate(-.05);x.scale(lerp(2.4,1,k),lerp(2.4,1,k));txt("C'EST UN OUF.",0,0,100,{c:RED,stroke:22,sc:INK,a:a*cl(k)});x.restore()}
  // ---- 3,5-6,9 s : l'Éclair jaune arrive
  if(t>3.55&&t<7.1){const a=win(t,3.6,7.1,.02,.2);const kp=seg(t,3.55,3.75);if(kp<1)pic('kunai',lerp(-200,1300,kp),lerp(1500,500,kp),240,{rot:-.6});
    panel(40,170,1000,1380,(w,h)=>{x.fillStyle='#f4d78a';x.fillRect(0,0,w,h);speedLines(w*.55,h*.42,280,100,tq,INK,.7);pic('minato_fight',w*.5+lerp(500,0,eo(seg(tq,3.7,4.0))),h*.45,980,{boil:3,t:tq})},{a,rot:.01});
    const k=back(seg(tq,4.6,4.8));if(k>0){x.save();x.translate(760,560);x.scale(k,k);x.translate(-760,-560);panel(560,330,400,460,(w,h)=>{cover('bg_kyubi',w,h);pic('minato_right',w/2,h*.6,h*1.2,{boil:2,t:tq})},{a,rot:.05,border:9});x.restore()}
    [[5.0,150,700],[5.25,930,1050],[5.5,200,1180]].forEach(([t0,px,py])=>{const u=seg(t,t0,t0+.12);if(u>0&&u<1)pic('kunai',px,py,160,{rot:-.6,a:1-u})});
    txt("L'ÉCLAIR JAUNE",W/2,300,84,{c:GOLD,stroke:16,sc:INK,a:a*seg(tq,3.8,4.0),rot:-.03});
    stamp('PAS AU NIVEAU.',W/2,1330,90,RED,5.4,t,-.07,'#fffaf0');sfx('ドン',880,560,150,RED,t,win(t,3.7,6.5,.05,.3))}
  // ---- 6,9-11,6 s : la méthode (tous les combats du manga à l'encre)
  if(t>6.8&&t<11.8){const a=win(t,6.9,11.8,.15,.2);x.save();x.globalAlpha=a;
    const N=CONST.N,E=CONST.E,ord=CONST.order;const CX0=90,CX1=990,CY0=380,CY1=1180;const P=N.map(([ar,m,c])=>[CX0+(ar+.12+.76*hash(c.length*7.7+ar))/CONST.narcs*(CX1-CX0),CY1-(m+1)/10*(CY1-CY0)]);
    const shown=Math.floor(eo(seg(t,7.1,10.0))*E.length);for(let r=0;r<shown;r++){const e=E[ord[r]];const A=P[e[0]],B=P[e[1]];x.strokeStyle=r>shown-8?RED:'rgba(24,20,15,.55)';x.lineWidth=r>shown-8?4:2;x.beginPath();x.moveTo(A[0],A[1]);x.quadraticCurveTo((A[0]+B[0])/2,(A[1]+B[1])/2-30,B[0],B[1]);x.stroke()}
    P.forEach(([px,py])=>{x.fillStyle=INK;x.beginPath();x.arc(px,py,4,0,7);x.fill()});
    mono('combats codés : '+String(Math.min(193,Math.round(193*shown/E.length))).padStart(3,'0'),70,330,40,{w:700});
    [['QUI BAT QUI',9.4,300,1270,-.05],['QUAND',10.2,590,1310,.04],['À QUEL POINT',10.9,820,1250,-.03]].forEach(([s,t0,px,py,r])=>stamp(s,px,py,40,RED,t0,t,r,'#fffaf0'));x.restore()}

  // ---- 11,7-25 s : dossier Itachi
  dossier(t,'itachi',11.6,25.05,[[11.7,'V'],[14.7,'V'],[17.7,'V'],[21.1,'D']]);
  bout(t,11.7,14.65,{hero:'itachi',hp:'itachi_front',foes:[['kakashi',0,560,false]],bg:'bg_tsukuyomi',name:'KAKASHI',ref:'ch. 142-143',res:'PLIÉ EN 1 SECONDE',resCol:RED,sfx:'月読'});
  bout(t,14.7,17.65,{hero:'itachi',hp:'itachi_left',foes:[['p_orochimaru',0,600,false]],name:'OROCHIMARU',ref:'Akatsuki · flashback',res:'SANS SA MAIN',resCol:RED,sfx:'ザン'});
  bout(t,17.7,21.05,{hero:'itachi',hp:'itachi_fight',foes:[['p_nagato',0,600,false]],name:'NAGATO',ref:'4e grande guerre',res:'SCELLÉ',resCol:RED,sfx:'封'});
  bout(t,21.1,25.05,{hero:'itachi',hp:'itachi_front',hflip:true,foes:[['p_sasuke',0,600,false]],name:'SASUKE',ref:'Partie 2 · combat final',res:'DÉFAITE*',resCol:INK,loss:true});
  if(t>22.6&&t<25.05)box('* malade, et il se retenait',W/2,1520,{size:34,a:win(t,22.6,25.05,.15,.12),rot:.02});
  // ---- 25-36 s : dossier Minato
  dossier(t,'minato',25.0,36.05,[[25.1,'N'],[28.7,'V'],[32.5,'D']]);
  bout(t,25.1,28.65,{hero:'minato',hp:'minato_fight',foes:[['raikage',-210,600,false],['killer_b',220,600,true]],name:'RAIKAGE + KILLER B',ref:'ch. 541 · 3e guerre',res:'À 1 CONTRE 2 : TIENT',resCol:'#8a6400',sfx:'ドン'});
  bout(t,28.7,32.45,{hero:'minato',hp:'minato_right',foes:[['obito',0,600,false]],bg:'bg_kyubi',name:"L'HOMME MASQUÉ",ref:'ch. 501-503',res:'BATTU. KURAMA LIBÉRÉ',resCol:'#8a6400',sfx:'閃'});
  bout(t,32.5,36.05,{hero:'minato',hp:'minato_fight',hflip:true,foes:[['obito',-180,600,true],['p_hashirama',270,380,false]],bg:'bg_kamui',name:'OBITO JÛBI',ref:'ch. 638-643',res:'DÉFAITE*',resCol:INK,loss:true});
  if(t>33.8&&t<36.05)box('* à 4 Hokage contre un jinchûriki de Jûbi',W/2,1520,{size:32,a:win(t,33.8,36.05,.15,.12),rot:-.02});

  // ---- 36-49,5 s : la toile de tous les combats
  const wa=t>36&&t<49.7?win(t,36.1,49.7,.2,.25):0;
  if(wa>0){web(t,wa);mono('chaque trait = un combat du manga',W/2,300,30,{al:'center',w:700,a:wa*seg(t,36.6,37)});
    if(t>45.2){[['122','PERSOS',INK,45.4],['250','LIENS',RED,46.4],['1','SEULE TOILE',INK,47.4]].forEach(([n,l,c,t0],i)=>{if(t<t0)return;stamp(n,200+i*340,400,64,c,t0,t,(i-1)*.05,'#fffaf0');txt(l,200+i*340,480,26,{f:'Zen',w:900,a:wa})})}}

  // ---- 49,6-55 s : 4 000 combats simulés
  if(t>49.5&&t<55.1){const a=win(t,49.6,55.1,.2,.25);x.save();x.globalAlpha=a;const n=Math.round(4000*eo(seg(t,49.8,53)));mono('combats simulés : '+String(n).padStart(4,'0')+' / 4000',W/2,300,40,{al:'center',w:700});
    const cols=[[230,GOLD,'MINATO',P_MI],[540,GREY,'NUL',P_D],[850,RED,'ITACHI',P_IT]];const R=rngS(5);const cnt=[0,0,0];
    for(let i=0;i<300;i++){const r=R();const b=r<P_MI?0:r<P_MI+P_D?1:2;const t0=49.9+i*.009;const u=seg(t,t0,t0+.4);if(u<=0)continue;const k=cnt[b]++;const cx=cols[b][0]+((k%12)-5.5)*19,cy=1150-Math.floor(k/12)*19;
      const px=lerp(W/2+(hash(i)-.5)*700,cx,eio(u)),py=lerp(380,cy,u*u);x.fillStyle=cols[b][1];x.beginPath();x.arc(px,py,8.5,0,7);x.fill()}
    cols.forEach(([cx,c,l,p])=>{txt(l,cx,1230,40,{c,stroke:8,sc:INK});txt(Math.round(p*100*seg(t,50,53))+' %',cx,1150-Math.ceil(p*300/12)*19-20,64,{c:INK})});
    stamp('VERDICT : MINATO',W/2,520,76,RED,51.8,t,-.06,'#fffaf0');x.restore()}
  // ---- 55-59 s : « serré… mais Minato » — deux cases, celle de Minato prend la place
  if(t>55&&t<59.1){const a=win(t,55.1,59.1,.15,.2);const g=eo(seg(tq,56.6,57.2));
    panel(40,280,lerp(490,330,g),1100,(w,h)=>{x.fillStyle=INK;x.fillRect(0,0,w,h);pic('itachi_left',w/2,h*.55,h*.95,{boil:2,t:tq})},{a,rot:-.012});
    panel(lerp(550,390,g),280,lerp(490,650,g),1100,(w,h)=>{x.fillStyle='#f4d78a';x.fillRect(0,0,w,h);speedLines(w/2,h*.45,220,70,tq,INK,.6*g);pic('minato_fight',w/2,h*.5,h*.95,{boil:3,t:tq})},{a,rot:.012});
    txt('41 %',lerp(285,205,g),1330,80,{c:RED,stroke:14,sc:INK,a});txt('45 %',lerp(795,715,g),1330,lerp(80,120,g),{c:GOLD,stroke:16,sc:INK,a});
    txt('SERRÉ…',W/2,230,70,{c:INK,a:a*seg(tq,55.3,55.5)});stamp('MAIS MINATO.',W/2,800,86,RED,57.3,t,-.07,'#fffaf0')}
  // ---- 59-63 s : respect
  if(t>59&&t<63){const a=win(t,59.1,63,.2,.2);x.save();x.globalAlpha=a;pic('itachi_front',W/2,820,820,{boil:2,t:tq});enso(W/2,700,320,eo(seg(t,59.3,60.7))*.76,RED,44);
    txt('3 SUR 4',W/2,1330,140,{c:RED,stroke:22,sc:INK,a:seg(tq,60.2,60.5)});txt('du casting battu par Itachi',W/2,1410,40,{f:'Zen',w:900,a:seg(tq,60.4,60.7)});x.restore()}
  // ---- 63-67,5 s : « pas d'accord ? » + appel
  if(t>62.8&&t<67.6){const a=win(t,62.9,67.6,.15,.3);
    panel(40,170,1000,1380,(w,h)=>{x.fillStyle='#f4d78a';x.fillRect(0,0,w,h);speedLines(w*.5,h*.45,300,90,tq,INK,.55);pic('minato_fight',w*.5,h*.5,900,{boil:3,t:tq})},{a,rot:-.01});
    const k=back(seg(tq,64.2,64.45));x.save();x.translate(W/2,300);x.rotate(-.04);x.scale(lerp(2,1,k),lerp(2,1,k));txt("PAS D'ACCORD ?",0,0,96,{c:PAPER,stroke:18,sc:INK,a:cl(k)});x.restore();
    if(t>65){x.save();x.translate(W/2,1380);x.rotate(.02);x.fillStyle='#fffaf0';x.globalAlpha=seg(t,65,65.3);x.fillRect(-440,-60,880,96);x.lineWidth=7;x.strokeStyle=INK;x.strokeRect(-440,-60,880,96);mono('ton argument → commentaire → modèle',0,6,36,{al:'center',w:700});x.restore()}}
  // ---- 67,5-70 s : carte de fin
  if(t>67.4){const a=seg(t,67.5,67.8);x.save();x.globalAlpha=a;x.fillStyle=INK;x.fillRect(0,0,W,H);txt('LE VERDICT',W/2,880,120,{c:PAPER});mono('Itachi vs Madara : la prochaine',W/2,980,36,{al:'center',c:GOLD,w:700,a:seg(t,68,68.3)});x.restore()}

  // marque + sous-titres + impacts
  x.setTransform(1,0,0,1,sx,sy);if(t<67.5){txt('LE VERDICT',60,120,52,{al:'left',c:INK});mono('193 combats · modèle bayésien',62,150,22,{c:GREY});x.save();x.translate(1000,104);x.rotate(.08);x.fillStyle=RED;x.fillRect(-34,-34,68,68);txt('V',0,20,52,{c:PAPER});x.restore()}
  subtitle(t);
  [1.0,3.65,12.5,29.5,51.8,57.3,64.2].forEach(s=>{if(t>=s&&t<s+.08){x.setTransform(1,0,0,1,0,0);x.globalCompositeOperation='difference';x.fillStyle='#fff';x.fillRect(0,0,W,H);x.globalCompositeOperation='source-over'}});
}
