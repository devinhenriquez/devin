import numpy as np, subprocess, sys, json
def load(f, sr=22050):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(sr),'-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.int16).astype(float)/32768, sr
def frames(a,sr,hop=0.05,n=4096):
    h=int(sr*hop);win=np.hanning(n);fr=np.fft.rfftfreq(n,1/sr);band=(fr>150)&(fr<1500)
    T=[];M=[];E=[];C=[];Cen=[]
    for i in range(0,len(a)-n,h):
        x=a[i:i+n]; s=np.abs(np.fft.rfft(x*win)); hp=s.copy()
        for k in (2,3): d=s[::k]; hp[:len(d)]*=d
        hb=hp*band; j=np.argmax(hb); f=fr[j]
        conf=hb[j]/(np.mean(hb[band])+1e-12)
        T.append(i/sr); M.append(12*np.log2(max(f,1)/440)+69); E.append(20*np.log10(np.sqrt(np.mean(x**2))+1e-9)); C.append(np.log10(conf+1e-9))
        Cen.append(np.sum(fr*s)/(np.sum(s)+1e-12))
    return map(np.array,(T,M,E,C,Cen))
if __name__=='__main__':
    out={}
    for f in sys.argv[1:]:
        a,sr=load(f); T,M,E,C,Cen=frames(a,sr)
        # per-second summaries
        sec=int(T[-1]); es=[];cs=[];vs=[]
        for s in range(sec):
            m=(T>=s)&(T<s+1); es.append(E[m].mean()); cs.append(C[m].mean())
        es=np.array(es); cs=np.array(cs)
        # best 21s window: loud enough, clear melody, pitch varies (interesting line)
        best=None
        for s in range(0,sec-21):
            m=(T>=s)&(T<s+21)
            e=E[m]; c=C[m]; mm=M[m][E[m]>-35]
            if len(mm)<50: continue
            score=c.mean()*1.0 + min(np.std(mm),5)*0.15 - max(0,-24-e.mean())*0.1
            # prefer starting on a quiet-ish moment (phrase start)
            score+= -0.02*(es[s]-es.min())
            if best is None or score>best[0]: best=(score,s,e.mean(),c.mean(),np.std(mm))
        name=f.split('_-_')[-1][:-4]
        out[name]=dict(file=f,best=best[1],score=round(best[0],2),loud=round(best[2],1),clar=round(best[3],2),spread=round(best[4],1),cent=round(float(np.median(Cen)),0),dur=round(T[-1]))
        print(name,out[name]['best'],out[name]['score'],out[name]['loud'],out[name]['clar'],out[name]['spread'],out[name]['cent'], ' '.join(f'{x:.0f}' for x in es))
    json.dump(out,open('analysis.json','w'),indent=1)
