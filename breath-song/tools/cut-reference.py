import numpy as np, json, subprocess, sys
sys.path.insert(0,'..'); from analyze import load, frames
cuts=json.load(open('cuts.json'))
MAP={'Saru':'monkey','Neko':'cat','Shika':'deer','Shadows_In_The_Fog':'fox','Ghost_of_Kozakura':'owl','The_Lament_of_The_Storm':'crane','Kanashi_Uta':'spare-kanashi-uta'}
def contour(path):
    a,sr=load(path); t,m,e,c,_=frames(a,sr)
    for i in range(1,len(m)):
        if e[i]<-35 or c[i]<1.6: m[i]=m[i-1]
    med=np.median(m)
    m=np.where(np.abs(m-med)>8, m-12*np.round((m-med)/12), m)   # fold octave slips back into the main register
    k=7; mp=np.pad(m,k//2,mode='edge'); m=np.array([np.median(mp[i:i+k]) for i in range(len(m))])
    lo,hi=np.percentile(m,3),np.percentile(m,97); v=np.clip((m-lo)/max(hi-lo,1),0,1)
    dur=len(a)/sr; T=np.arange(0,dur,0.1); vv=np.interp(T,t,v)
    g=np.exp(-np.linspace(-2,2,9)**2); g/=g.sum(); vv=np.convolve(np.pad(vv,4,mode='edge'),g,'valid')
    vv=0.15+0.7*vv
    def slew(x,lim=.07):
        y=x.copy()
        for i in range(1,len(y)): y[i]=y[i-1]+np.clip(y[i]-y[i-1],-lim,lim)
        return y
    vv=(slew(vv)+slew(vv[::-1])[::-1])/2   # no cliffs: the line can't move faster than a hand can tilt
    return [round(float(x),3) for x in vv]
for name,cfo in cuts.items():
    key=MAP[name]; s=cfo['start']; d=cfo['end']-s
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{s:.2f}','-t',f'{d:.2f}','-i',cfo['file'],'-vn','-af',f'afade=t=in:d=0.25,afade=t=out:st={d-1.0:.2f}:d=1.0,loudnorm=I=-16:TP=-1.5','-ar','44100','-ac','2','-b:a','128k',f'{key}.mp3'],check=True)
    cv=contour(f'{key}.mp3'); json.dump(cv,open(f'{key}-contour.json','w'))
    print(key, name, f'{s:.2f}s +{d:.1f}s', len(cv), ' '.join(f'{x:.1f}' for x in cv[::10]))
