/* Offline, deterministic 3D helpers. Row vectors multiply matrices on the right. */
(function (global) {
  'use strict';
  const T = 1e-10;
  const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
  const norm = a => Math.sqrt(dot(a, a));
  const sub = (a, b) => a.map((x, i) => x - b[i]);
  const add = (a, b) => a.map((x, i) => x + b[i]);
  const scale = (a, s) => a.map(x => x * s);
  const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
  const unit = a => scale(a, 1 / norm(a));
  const transpose = A => A[0].map((_, j) => A.map(row => row[j]));
  const mul = (A, B) => A.map(row => B[0].map((_, j) => dot(row, B.map(b => b[j]))));
  const vec = (x, R) => R[0].map((_, j) => x.reduce((s, v, i) => s + v * R[i][j], 0));
  const det = M => M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]);
  const I = () => [[1,0,0],[0,1,0],[0,0,1]];
  function rotation(yaw, pitch, roll) {
    const y=yaw*Math.PI/180, p=pitch*Math.PI/180, r=roll*Math.PI/180;
    const cy=Math.cos(y), sy=Math.sin(y), cp=Math.cos(p), sp=Math.sin(p), cr=Math.cos(r), sr=Math.sin(r);
    const Rz=[[cy,sy,0],[-sy,cy,0],[0,0,1]];
    const Ry=[[cp,0,-sp],[0,1,0],[sp,0,cp]];
    const Rx=[[1,0,0],[0,cr,sr],[0,-sr,cr]];
    return mul(mul(Rz,Ry),Rx);
  }
  function rng(seed) { let s=seed>>>0; return () => ((s=(1664525*s+1013904223)>>>0)/4294967296); }
  function gaussian(rand) { return Math.sqrt(-2*Math.log(Math.max(rand(),1e-12)))*Math.cos(2*Math.PI*rand()); }
  function cloud(seed=20260928) {
    const rand=rng(seed);
    const centers=[[-1.65,-.80,-.45],[-.95,1.12,.68],[.25,-1.18,.97],[1.48,-.36,-.82],[.92,1.35,-.12],[-.46,.18,-1.38]];
    return Array.from({length:48},(_,i)=>{
      const c=centers[Math.floor(i/8)];
      return {id:'w'+String(i+1).padStart(2,'0'), group:Math.floor(i/8), xyz:c.map(v=>v+.38*gaussian(rand))};
    });
  }
  function eigenSym3(input) {
    const A=input.map(r=>r.slice()), V=I();
    for(let k=0;k<60;k++) {
      let p=0,q=1,max=Math.abs(A[0][1]);
      for(const [i,j] of [[0,2],[1,2]]) if(Math.abs(A[i][j])>max){p=i;q=j;max=Math.abs(A[i][j]);}
      if(max<1e-13) break;
      const tau=(A[q][q]-A[p][p])/(2*A[p][q]);
      const t=(tau>=0?1:-1)/(Math.abs(tau)+Math.sqrt(1+tau*tau));
      const c=1/Math.sqrt(1+t*t), s=t*c;
      const app=A[p][p], aqq=A[q][q], apq=A[p][q];
      A[p][p]=app-t*apq; A[q][q]=aqq+t*apq; A[p][q]=A[q][p]=0;
      for(let i=0;i<3;i++) if(i!==p&&i!==q) {
        const aip=A[i][p], aiq=A[i][q];
        A[i][p]=A[p][i]=c*aip-s*aiq;
        A[i][q]=A[q][i]=s*aip+c*aiq;
      }
      for(let i=0;i<3;i++) { const vip=V[i][p],viq=V[i][q]; V[i][p]=c*vip-s*viq;V[i][q]=s*vip+c*viq; }
    }
    const order=[0,1,2].sort((i,j)=>A[j][j]-A[i][i]);
    return {values:order.map(i=>A[i][i]), vectors:order.map(j=>V.map(row=>row[j]))};
  }
  function procrustes(source, target) {
    if(source.length!==target.length || source.length<3) return {ok:false, reason:'Выберите от 3 до 5 известных пар.'};
    const mean=P=>[0,1,2].map(j=>P.reduce((s,p)=>s+p[j],0)/P.length);
    const a0=mean(source), b0=mean(target);
    const A=source.map(p=>sub(p,a0)), B=target.map(p=>sub(p,b0));
    const M=mul(transpose(A),B); // A^T B
    const eig=eigenSym3(mul(transpose(M),M));
    const sigma=eig.values.map(x=>Math.sqrt(Math.max(0,x)));
    const spread=Math.sqrt(A.reduce((s,p)=>s+dot(p,p),0));
    if(spread<T || sigma[1]<Math.max(1e-8,sigma[0]*1e-3)) return {ok:false, reason:'Якоря почти лежат на одной прямой. Выберите разнесённые пары из разных областей.'};
    const v1=eig.vectors[0],v2=eig.vectors[1],v3=unit(cross(v1,v2));
    const u1=unit(vec(v1,transpose(M)));
    const u2raw=vec(v2,transpose(M));
    const u2=unit(sub(u2raw,scale(u1,dot(u2raw,u1))));
    const u3pos=unit(cross(u1,u2));
    // A full-rank SVD may have det(U V^T) < 0; correct its last sign.
    const u3raw=sigma[2]>Math.max(1e-8,sigma[0]*1e-8)?unit(vec(v3,transpose(M))):u3pos;
    const rawSign=Math.sign(dot(u3raw,u3pos)) || 1;
    const U=transpose([u1,u2,u3raw]);
    const V=transpose([v1,v2,v3]);
    const D=[[1,0,0],[0,1,0],[0,0,rawSign]];
    const R=mul(mul(U,D),transpose(V));
    const t=sub(b0,vec(a0,R));
    const transform=p=>add(vec(p,R),t);
    const residual=Math.sqrt(source.reduce((s,p,i)=>s+dot(sub(transform(p),target[i]),sub(transform(p),target[i])),0)/source.length);
    return {ok:true,R,t,residual,singularValues:sigma,detR:det(R),detCorrection:rawSign,transform};
  }
  function nearest(query, points, exclude=-1, metric='euclidean') {
    let best=-1, score=Infinity;
    points.forEach((p,i)=>{
      if(i===exclude)return;
      const d=metric==='cosine' ? 1-dot(query,p)/(norm(query)*norm(p)) : dot(sub(query,p),sub(query,p));
      if(d<score){score=d;best=i;}
    });
    return best;
  }
  function render(svg, sets, opts={}) {
    const w=800,h=500, yaw=-32*Math.PI/180,pitch=23*Math.PI/180;
    const project=p=>{
      const x=p[0]*Math.cos(yaw)-p[1]*Math.sin(yaw), y=p[0]*Math.sin(yaw)+p[1]*Math.cos(yaw), z=p[2];
      return [w/2+(x*58),h/2-(y*Math.sin(pitch)+z*Math.cos(pitch))*58,y*Math.cos(pitch)-z*Math.sin(pitch)];
    };
    const axis=[[[0,0,0],[2.5,0,0],'x'],[[0,0,0],[0,2.5,0],'y'],[[0,0,0],[0,0,2.5],'z']];
    let html='<g class="axes">';
    axis.forEach(([a,b,label])=>{const p=project(a),q=project(b);html+=`<line x1="${p[0]}" y1="${p[1]}" x2="${q[0]}" y2="${q[1]}" stroke="#7790a8" stroke-width="2"/><text x="${q[0]+7}" y="${q[1]-6}" fill="#b4c4d9" font-size="20" font-family="Arial" font-weight="700">${label}</text>`;});
    html+='</g>';
    const marks=[];
    sets.forEach((set,si)=>set.points.forEach((p,i)=>{const xyz=p.xyz||p, xy=project(xyz);marks.push({xy,si,i,set,p});}));
    marks.sort((a,b)=>a.xy[2]-b.xy[2]);
    marks.forEach(m=>{
      const selected=m.set.selected?.includes(m.i);
      const r=selected?9:5.2;
      const label=m.set.labels?.[m.i];
      html+=`<circle class="mark set${m.si}${selected?' selected':''}" cx="${m.xy[0].toFixed(2)}" cy="${m.xy[1].toFixed(2)}" r="${r}" fill="${selected?'#a9e879':m.si?'#ffad64':'#59d6e6'}" stroke="${selected?'#ffffff':'#122332'}" stroke-width="${selected?2.5:1.2}" opacity="${selected?1:.8}"/>`;
      if(label) html+=`<text class="point-label" x="${(m.xy[0]+11).toFixed(2)}" y="${(m.xy[1]+(m.si?22:-9)).toFixed(2)}" fill="#ffffff" font-size="17" font-family="Arial" font-weight="700">${label}</text>`;
    });
    svg.innerHTML=html;
  }
  global.Lecture3D={dot,norm,sub,add,scale,cross,transpose,mul,vec,det,rotation,rng,gaussian,cloud,eigenSym3,procrustes,nearest,render};
})(window);
