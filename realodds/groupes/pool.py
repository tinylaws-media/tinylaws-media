import json,glob,math,sys
P0=0.5;M0=0.0;rows=[]
for f in sorted(glob.glob(sys.argv[1]+'_*.json')):
    m=json.load(open(f))['meta'];mu=math.log(m['eta']);sd=m['eta_log_sd']
    pm,ps=m['eta_prior']
    pl=1/sd**2-1/ps**2
    if pl<=1e-6: rows.append((f,None,None));continue
    ml=(mu/sd**2-pm/ps**2)/pl
    rows.append((f.split('_',1)[1][:-5],ml,1/math.sqrt(pl)))
ok=[r for r in rows if r[1] is not None]
w=[1/s**2 for _,_,s in ok];mf=sum(wi*m for wi,(_,m,_) in zip(w,ok))/sum(w)
Q=sum(wi*(m-mf)**2 for wi,(_,m,_) in zip(w,ok));k=len(ok)
tau2=max(0,(Q-(k-1))/(sum(w)-sum(x*x for x in w)/sum(w)))
wr=[1/(s**2+tau2) for _,_,s in ok];mr=sum(wi*m for wi,(_,m,_) in zip(wr,ok))/sum(wr);ser=1/math.sqrt(sum(wr))
for n,m,s in ok: print(n.ljust(14),'vraisemblance seule : eta =',round(math.exp(m),2),'(log-sd',round(s,2),')')
print('Q',round(Q,2),'df',k-1,'tau',round(math.sqrt(tau2),3))
print('commun : eta =',round(math.exp(mr),3),'IC95',round(math.exp(mr-1.96*ser),2),'-',round(math.exp(mr+1.96*ser),2),'| log mu',round(mr,3),'se',round(ser,3))
json.dump(dict(mu=mr,se=ser,tau=math.sqrt(tau2),Q=Q,k=k,per=[dict(v=n,mu=m,sd=s) for n,m,s in ok]),open('pool_'+sys.argv[1]+'.json','w'))
