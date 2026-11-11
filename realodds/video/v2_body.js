// ===================== V2 : « mi-manga, mi-modèle » =====================
const MONO="JB";
function mono(s,px,py,size,{c=INK,al='left',a=1,rot=0,w=500}={}){txt(s,px,py,size,{f:MONO,w,c,al,a,rot})}
// sous-titres (voix off)
const SUBS=[[0.2,3.4,"Itachi contre Minato. J'ai laissé *un réseau bayésien* trancher."],
 [3.5,6.9,"Itachi, c'est *un palmarès.*"],
 [7.0,10.0,"Kakashi plié en *un seul Tsukuyomi.*"],[10.0,12.4,"Orochimaru qui *perd un bras.*"],[12.4,14.5,"Nagato *scellé*, avec Naruto."],
 [14.5,18.9,"Chaque combat est une donnée. Itachi en a beaucoup : sa courbe est *étroite.*"],
 [19.0,23.9,"Minato, lui, a très peu de combats montrés. Alors le modèle lit *ce que le manga dit de lui.*"],
 [24.0,28.4,"Un : il devient *Hokage à la place d'Orochimaru*, un Sannin."],
 [28.5,32.9,"Deux : le Raikage l'avoue, sans Minato, *c'est lui le plus rapide.*"],
 [33.0,37.9,"Trois : à la 3e guerre, il tient tête au *Raikage ET à Killer B.* En même temps."],
 [38.0,44.9,"Et le détail qui tue : Itachi dit lui-même qu'à deux contre *Jiraiya*, ils y laisseraient la vie. Jiraiya, *le maître de Minato.*"],
 [45.0,49.9,"4 000 combats simulés : *Minato 48 %*, Itachi 38 %, 14 % de nuls."],
 [50.0,53.9,"Mais sa courbe est *plus large* : Minato est jugé sur sa réputation. Le modèle reste prudent."],
 [54.0,59.5,"Respect à Itachi : il bat *3 persos sur 4.* Toi, tu changes quoi dans le calcul ? *Dis-le en commentaire.*"]];

// graphe factoriel (couche « calcul ») : nœuds = forces latentes, carrés = données
const GN={itachi:[720,650,'f_itachi',RED,'s_Itachi'],minato:[330,650,'f_minato',GOLD,'s_Minato'],kakashi:[880,320,'f_kakashi',INK,'s_Kakashi'],orochimaru:[945,560,'p_orochimaru',INK,'s_Orochimaru'],
  nagato:[880,920,'p_nagato',INK,'s_Nagato'],jiraiya:[520,360,'p_jiraiya',INK,'s_Jiraiya'],raikage:[150,360,'raikage_f',INK,'s_A'],killerb:[150,900,'killer_f',INK,'s_B'],hokage:[340,940,null,INK,'titre']};
// données : [nœud A, nœud B, instant d'arrivée, étiquette du facteur, effet affiché]
const FACT=[['itachi','kakashi',9.0,'ch.142','+0.14'],['itachi','orochimaru',11.3,'ch.~180','+0.04'],['itachi','nagato',13.4,'ch.548','+0.05'],
  ['minato','hokage',26.8,'ch.450','+0.09'],['minato','raikage',31.4,'ch.541','A<M'],['minato','raikage',36.2,'ch.541','A+B'],['minato','killerb',36.2,'ch.541',''],['itachi','jiraiya',41.0,'ch.147','≈'],['minato','jiraiya',43.2,'maître','']];
const gaussPath=(m,s,X0,X1,Y,hpx,lo,hi)=>{const pts=[];for(let i=0;i<=120;i++){const v=lo+(hi-lo)*i/120;pts.push([X0+(v-lo)*(X1-X0)/(hi-lo),Y-hpx*.42/s*Math.exp(-.5*((v-m)/s)**2)])}return pts};
function bell(m,s,col,a,{dashed=false,label='',ldx=0,lal='center'}={}){if(a<=0)return;const X0=110,X1=990,Y=1480,lo=4.0,hi=7.5,pts=gaussPath(m,s,X0,X1,Y,170,lo,hi);x.save();x.globalAlpha*=a;
  if(!dashed){x.save();x.beginPath();x.moveTo(X0,Y);pts.forEach(p=>x.lineTo(p[0],p[1]));x.lineTo(X1,Y);x.closePath();x.clip();x.fillStyle=col;for(let yy=Y-500;yy<Y;yy+=11)for(let xx=X0+((yy/11)%2?5:0);xx<X1;xx+=11){x.beginPath();x.arc(xx,yy,3.1,0,7);x.fill()}x.restore()}
  x.lineWidth=dashed?5:7;x.strokeStyle=dashed?GREY:INK;if(dashed)x.setLineDash([14,10]);x.beginPath();pts.forEach((p,i)=>i?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1]));x.stroke();x.setLineDash([]);
  if(label){const px=X0+(m-lo)*(X1-X0)/(hi-lo),py=Y-170*.42/s-24;txt(label,px+ldx,py,34,{c:col,stroke:7,sc:INK,al:lal})}x.restore()}
function plotFrame(a){if(a<=0)return;x.save();x.globalAlpha*=a;const X0=110,X1=990,Y=1480;
  x.strokeStyle='rgba(24,20,15,.10)';x.lineWidth=1;for(let xx=60;xx<1030;xx+=30){x.beginPath();x.moveTo(xx,1150);x.lineTo(xx,1520);x.stroke()}for(let yy=1150;yy<1520;yy+=30){x.beginPath();x.moveTo(60,yy);x.lineTo(1020,yy);x.stroke()}
  brush([[X0-10,Y+2],[X1+20,Y+2]],1,8,INK,77);[4,5,6,7].forEach(v=>{const px=X0+(v-4)*(X1-X0)/3.5;x.fillStyle=INK;x.fillRect(px-2,Y,4,14);mono(String(v),px,Y+44,26,{al:'center'})});
  mono('FORCE LATENTE s',X1,Y+44,22,{al:'right',c:GREY});mono('p(s | toutes les données)',70,1180,26,{c:INK,w:700});x.restore()}
// carte « donnée » façon case de manga
function evCard(t,t0,t1,img,title,sub,tag,eff,col,target){if(t<t0||t>t1+.5)return;const inn=back(seg(t,t0,t0+.3)),out=eio(seg(t,t1,t1+.45));const tx=target?target[0]:W/2,ty=target?target[1]:600;
  const cx=lerp(W/2,tx,out),cy=lerp(560,ty,out),s=lerp(1,.12,out)*lerp(1.3,1,inn);if(s<=0)return;x.save();x.translate(cx,cy);x.scale(s,s);x.rotate((hash(t0)-.5)*.04);x.globalAlpha=cl(inn);
  x.fillStyle='#fffaf0';x.fillRect(-450,-260,900,520);x.lineWidth=12;x.strokeStyle=INK;x.strokeRect(-450,-260,900,520);
  x.save();x.beginPath();x.rect(-450,-260,380,520);x.clip();x.fillStyle=col==='#fffaf0'?INK:col;x.fillRect(-450,-260,380,520);speedLines(-260,0,120,40,q12(t),INK,.35);if(IMG[img]){const im=IMG[img];const h=img.startsWith('p_')||img.startsWith('f_')?380:500;const w=im.width*h/im.height;x.drawImage(im,-260-w/2,-h/2+(img.startsWith('p_')?0:20),w,h)}x.restore();
  x.lineWidth=8;x.beginPath();x.moveTo(-70,-260);x.lineTo(-70,260);x.stroke();
  mono('DONNÉE · '+tag,-40,-195,26,{c:GREY,w:700});
  const lines=title.split('|');x.font='400 54px Dela';const fs=Math.min(54,54*480/Math.max(...lines.map(l=>x.measureText(l).width)));lines.forEach((l,i)=>txt(l,-40,-120+i*(fs+12),fs,{al:'left',c:INK}));txt(sub,-40,-120+lines.length*(fs+12)+20,32,{f:'Zen',w:900,al:'left',c:GREY});
  if(eff){x.save();x.translate(250,180);x.rotate(-.06);x.lineWidth=5;x.strokeStyle=col===INK?RED:col;x.strokeRect(-150,-46,300,82);mono('Δs '+eff,0,14,40,{al:'center',c:col===INK?RED:col,w:700});x.restore()}x.restore()}

function renderAt(T){
  const t=T,tq=q12(T);x.setTransform(1,0,0,1,0,0);
  if(IMG.paper)x.drawImage(IMG.paper,0,0,W,H);else{x.fillStyle=PAPER;x.fillRect(0,0,W,H)}
  let shake=0;[1.6,9.0,31.4,36.2,41.0,49.0].forEach(s=>{const u=t-s;if(u>=0&&u<.3)shake=Math.max(shake,1-u/.3)});const sx=(hash(Math.floor(t*24))-.5)*26*shake,sy=(hash(Math.floor(t*24)+9)-.5)*18*shake;x.translate(sx,sy);
  // annotations « cahier de nerd » dans les marges
  const eqA=t>6&&t<45?win(t,6.2,45,.5,.5)*.55:0;
  mono('P(A > B) = σ(k·(sA − sB))',70,1120,26,{c:GREY,a:eqA,rot:-.02});mono('posterior ∝ vraisemblance × prior',600,1125,24,{c:GREY,a:eqA*seg(t,19,19.6),rot:.015});

  // ---- 0-3,5 s : accroche
  if(t<3.6){const a=1-seg(t,3.4,3.6);
    x.save();x.globalAlpha=a;x.save();x.beginPath();x.moveTo(40,170);x.lineTo(1040,170);x.lineTo(1040,560);x.lineTo(40,840);x.closePath();x.clip();x.fillStyle='#f4d78a';x.fillRect(0,0,W,H);speedLines(700,480,260,70,tq,INK,.5);pic('minato_fight',560,520,760,{boil:3,t:tq});x.restore();
    x.lineWidth=12;x.strokeStyle=INK;x.beginPath();x.moveTo(40,170);x.lineTo(1040,170);x.lineTo(1040,560);x.lineTo(40,840);x.closePath();x.stroke();
    x.save();x.beginPath();x.moveTo(40,890);x.lineTo(1040,610);x.lineTo(1040,1500);x.lineTo(40,1500);x.closePath();x.clip();x.fillStyle=INK;x.fillRect(0,0,W,H);speedLines(380,1150,260,70,tq,RED,.6);pic('itachi_fight',520,1120,780,{boil:3,t:tq});x.restore();
    x.lineWidth=12;x.beginPath();x.moveTo(40,890);x.lineTo(1040,610);x.lineTo(1040,1500);x.lineTo(40,1500);x.closePath();x.stroke();
    // surcouche « calcul » : graphe qui se trace par-dessus le manga
    const g=eo(seg(t,.6,2.2));[[200,300,820,1250],[820,330,260,1300],[540,700,540,1100]].forEach(([a1,b1,a2,b2],k)=>brush([[a1,b1],[(a1+a2)/2+60,(b1+b2)/2],[a2,b2]],g,5,RED,k+20));
    const k=back(seg(tq,1.2,1.45));x.save();x.translate(W/2,740);x.rotate(-.18);x.scale(lerp(3,1,k),lerp(3,1,k));txt('VS',0,40,170,{c:PAPER,stroke:28,sc:INK,a:cl(k)});x.restore();
    const k2=seg(tq,1.9,2.1);x.save();x.translate(W/2,1440);x.rotate(-.02);x.fillStyle='#fffaf0';x.globalAlpha=a*k2;x.fillRect(-440,-60,880,96);x.lineWidth=7;x.strokeStyle=INK;x.strokeRect(-440,-60,880,96);mono('P( Minato > Itachi ) = ?',0,6,48,{al:'center',w:700});x.restore();
    sfx('ゴゴゴ',960,300,100,RED,t,a*seg(t,.1,.3),true);x.restore()}

  // ---- couche graphe (3,5-45 s) : nœuds + facteurs qui arrivent
  const gA=t>3.4&&t<45.4?win(t,3.5,45.4,.3,.4):0;
  if(gA>0){x.save();x.globalAlpha=gA;
    // arêtes et facteurs
    FACT.forEach(([A,B,ta,lab,eff],i)=>{if(t<ta)return;const pa=GN[A],pb=GN[B];const p=eo(seg(t,ta,ta+.4));const mx=(pa[0]+pb[0])/2,my=(pa[1]+pb[1])/2;
      brush([[pb[0],pb[1]],[mx,my]],p,7,INK,i);brush([[mx,my],[pa[0],pa[1]]],seg(t,ta+.2,ta+.6),7,INK,i+50);
      x.fillStyle=INK;x.fillRect(mx-26,my-26,52,52);if(lab)mono(lab,mx,my+56,22,{al:'center',w:700,c:INK});
      // message qui file vers le nœud évalué
      const u=seg(t,ta+.3,ta+1.1);if(u>0&&u<1){x.fillStyle=pa[3]===INK?RED:pa[3];x.beginPath();x.arc(lerp(mx,pa[0],u),lerp(my,pa[1],u),12,0,7);x.fill()}});
    // nœuds
    Object.entries(GN).forEach(([k,[px,py,img,col,lab]])=>{const tIn=k==='itachi'?3.7:k==='minato'?19.2:k==='jiraiya'?38.4:k==='hokage'?26.2:FACT.find(f=>f[1]===k)?FACT.find(f=>f[1]===k)[2]-.6:99;
      const s=back(seg(tq,tIn,tIn+.3));if(s<=0)return;x.save();x.translate(px,py);x.scale(s,s);const big=k==='itachi'||k==='minato';const R=big?118:74;
      if(k==='hokage'){x.fillStyle='#fffaf0';x.fillRect(-120,-44,240,88);x.lineWidth=7;x.strokeStyle=INK;x.strokeRect(-120,-44,240,88);txt('火影',0,22,60,{c:RED});x.restore();return}
      x.beginPath();x.arc(0,0,R,0,7);x.fillStyle=col===INK?'#d8cdb5':col;x.fill();
      if(IMG[img]){x.save();x.beginPath();x.arc(0,0,R-10,0,7);x.clip();const im=IMG[img];const sc=(2*(R-10))/Math.min(im.width,im.height);x.drawImage(im,-im.width*sc/2,-im.height*sc/2,im.width*sc,im.height*sc);x.restore()}
      x.lineWidth=big?11:8;x.strokeStyle=INK;x.beginPath();x.arc(0,0,R,0,7);x.stroke();mono(lab,0,R+38,big?30:22,{al:'center',w:700,c:col===INK?INK:col});x.restore()});
    x.restore()}

  // ---- cartes « données »
  evCard(t,7.0,9.0,'f_kakashi','ITACHI PLIE|KAKASHI','un seul Tsukuyomi','ch. 142-144','+0.14',RED,GN.kakashi);
  evCard(t,10.0,11.3,'p_orochimaru','OROCHIMARU|PERD UN BRAS','il voulait le corps d’Itachi','ch. ~180','+0.04',RED,GN.orochimaru);
  evCard(t,12.3,13.4,'p_nagato','NAGATO|SCELLÉ','Itachi + Naruto (4e guerre)','ch. 548','+0.05',RED,GN.nagato);
  evCard(t,19.4,22.6,'minato_right','MINATO :|PEU DE COMBATS','le modèle lit le manga','prior large','',GOLD,null);
  evCard(t,24.0,26.8,'minato_right','HOKAGE À LA|PLACE D’OROCHIMARU','choisi pour ses exploits','ch. 450','+0.09',GOLD,[GN.hokage[0],GN.hokage[1]]);
  evCard(t,28.5,31.4,'raikage','« SANS MINATO,|C’EST MOI »','le Raikage, le plus rapide','ch. 541','A < M',GOLD,GN.raikage);
  evCard(t,33.0,36.2,'killer_b','RAIKAGE + B|EN MÊME TEMPS','il tient tête aux deux','ch. 541','',GOLD,GN.killerb);
  evCard(t,38.0,41.0,'p_jiraiya','« À DEUX, ON Y|LAISSERAIT LA VIE »','Itachi, à propos de Jiraiya','ch. 147','I ≈ J',INK,GN.jiraiya);
  if(t>33.4&&t<36.2)sfx('ドドド',90,860,100,GOLD,t,win(t,33.6,36.1,.05,.2),true);
  if(t>41.3&&t<44.9){const a=win(t,41.4,44.9,.2,.3);brush([[620,250],[540,300]],0,0);txt('MAÎTRE',400,500,40,{c:GOLD,stroke:8,sc:INK,a,rot:-.95});txt('≈',650,480,90,{c:RED,stroke:12,sc:INK,a})}

  // ---- courbes a posteriori (bas de page), qui se mettent à jour avec les données
  const pA=t>6.6&&t<54?win(t,6.7,54,.4,.4):0;plotFrame(pA);
  const KI=[[6.8,5.5,.9],[8.8,5.5,.9],[9.4,5.6,.62],[11.1,5.6,.62],[11.7,5.65,.48],[13.2,5.65,.48],[13.8,5.673,.382]];
  const KM=[[19.5,5.5,1.05],[26.6,5.5,1.05],[27.3,5.72,.82],[31.2,5.72,.82],[31.9,5.8,.71],[36.0,5.8,.71],[36.7,5.84,.634]];
  const interp=(K)=>{let v=[K[0][1],K[0][2]];for(let i=1;i<K.length;i++){if(t>=K[i-1][0]){const u=eio(seg(t,K[i-1][0],K[i][0]));v=[lerp(K[i-1][1],K[i][1],u),lerp(K[i-1][2],K[i][2],u)]}}return v};
  if(pA>0){const [mi,si]=interp(KI);bell(mi,si,RED,pA*seg(t,6.8,7.3),{label:'ITACHI'});
    if(t>19.4){const [mm,sm]=interp(KM);bell(mm,sm,GOLD,pA*seg(t,19.5,20),{label:'MINATO',ldx:70,lal:'left'})}
    if(t>38.6&&t<45)bell(5.435,.626,GREY,pA*win(t,38.7,45,.3,.3),{dashed:true,label:'JIRAIYA',ldx:-80,lal:'right'});
    if(t>15&&t<19){const a=win(t,15.1,19,.2,.2);mono('σ = 0.38 → beaucoup de combats',560,1250,28,{c:RED,a,w:700})}
    if(t>50&&t<54){const a=win(t,50.1,54,.2,.2);mono('σ_Minato = 0.63',150,1250,30,{c:GOLD,a,w:700});mono('σ_Itachi = 0.38',650,1250,30,{c:RED,a,w:700});stamp('PRUDENCE',W/2,1075,58,INK,50.4,t,-.05,'#fffaf0')}}

  // ---- 45-50 s : Monte Carlo (on tire des paires dans les deux courbes)
  if(t>44.9&&t<54.2){const a=win(t,45,54.2,.2,.3);x.save();x.globalAlpha=a;const n=Math.round(4000*eo(seg(t,45.2,48.8)));
    mono('tirage '+String(n).padStart(4,'0')+' / 4000',W/2,260,40,{al:'center',w:700});
    const cols=[[230,GOLD,'MINATO',.48],[540,GREY,'NUL',.14],[850,RED,'ITACHI',.38]];const R=rngS(5);const cnt=[0,0,0];
    for(let i=0;i<300;i++){const r=R();const b=r<.48?0:r<.62?1:2;const t0=45.3+i*.011;const u=seg(t,t0,t0+.4);if(u<=0)continue;const k=cnt[b]++;const cx=cols[b][0]+((k%12)-5.5)*19,cy=880-Math.floor(k/12)*19;
      const sx0=b===2?720:380;const px=lerp(sx0+(hash(i)-.5)*160,cx,eio(u)),py=lerp(1300,cy,eio(u));x.fillStyle=cols[b][1];x.beginPath();x.arc(px,py,8.5,0,7);x.fill()}
    cols.forEach(([cx,c,l,p])=>{txt(l,cx,950,40,{c,stroke:8,sc:INK});txt(Math.round(p*100*seg(t,45.6,48.8))+' %',cx,880-Math.ceil(p*300/12)*19-20,62,{c:INK})});
    if(t>49)stamp('VERDICT : MINATO',W/2,430,70,RED,49.0,t,-.06,'#fffaf0');x.restore()}

  // ---- 54-60 s : respect + question
  if(t>53.9&&t<59.7){const a=win(t,54,59.7,.2,.25);x.save();x.globalAlpha=a;pic('itachi_front',W/2,900,820,{boil:2,t:tq});enso(W/2,780,320,eo(seg(t,54.3,55.7))*.75,RED,44);
    txt('75 %',W/2,1380,140,{c:RED,stroke:20,sc:INK,a:seg(tq,55.3,55.6)});txt('du casting battu par Itachi',W/2,1460,38,{f:'Zen',w:900,a:seg(tq,55.5,55.8)});
    const k=back(seg(tq,57,57.25));x.save();x.translate(W/2,300);x.rotate(-.03);x.scale(lerp(2,1,k),lerp(2,1,k));txt('TU CHANGES QUOI ?',0,0,74,{c:GOLD,stroke:16,sc:INK,a:cl(k)});x.restore();
    mono('# ton argument → commentaire',W/2,400,36,{al:'center',w:700,a:seg(tq,57.4,57.6)});x.restore()}

  // marque + sous-titres + impacts + boucle
  x.setTransform(1,0,0,1,sx,sy);txt('LE VERDICT',60,120,52,{al:'left',c:INK});mono('modèle bayésien · 193 combats',62,150,22,{c:GREY});x.save();x.translate(1000,104);x.rotate(.08);x.fillStyle=RED;x.fillRect(-34,-34,68,68);txt('V',0,20,52,{c:PAPER});x.restore();
  subtitle(t);
  [1.6,9.0,31.4,49.0].forEach(s=>{if(t>=s&&t<s+.08){x.setTransform(1,0,0,1,0,0);x.globalCompositeOperation='difference';x.fillStyle='#fff';x.fillRect(0,0,W,H);x.globalCompositeOperation='source-over'}});
  if(t>59.6){x.setTransform(1,0,0,1,0,0);x.globalAlpha=seg(t,59.6,59.95);x.fillStyle=INK;x.fillRect(0,0,W,H);x.globalAlpha=1}
}
