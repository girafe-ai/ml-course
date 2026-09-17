(() => {
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pdf=new URLSearchParams(location.search).has('pdf');
  const palette={ink:'#1e1e1f',line:'#d7d7d2',contour:'#8ca7b5',blue:'#3157b7',red:'#c63d4f',paper:'#fffdf7'};
  const configs={
    raw:{a:1,b:18,start:[-3.2,.45],maxSteps:12,plotMaxY:1.05,color:palette.blue},
    normalized:{a:1,b:1,start:[-3.2,1.909],maxSteps:11,plotMaxY:2.05,color:palette.blue},
    explode:{a:1,b:18,start:[-3,.72],maxSteps:8,plotMaxY:1.05,color:palette.red}
  };
  const clamp=(value,min,max)=>Math.max(min,Math.min(max,value));
  const comma=value=>Number(value).toFixed(3).replace('.',',');

  function createLab(root){
    const config=configs[root.dataset.scenario];
    const canvas=root.querySelector('canvas');
    const context=canvas.getContext('2d');
    const slider=root.querySelector('[data-gd-eta]');
    const etaOutput=root.querySelector('[data-gd-eta-output]');
    const gradientOutput=root.querySelector('[data-gd-gradient]');
    const iterationOutput=root.querySelector('[data-gd-iteration]');
    const playButton=root.querySelector('[data-gd-action="play"]');
    const maxX=4,maxY=config.plotMaxY,pad={left:42,right:24,top:24,bottom:34};
    const state={point:[...config.start],display:[...config.start],history:[[...config.start]],iteration:0,running:!reduced&&!pdf,segment:null,restartAt:0,range:[maxX,maxY]};

    const eta=()=>Number(slider.value);
    const nextPoint=point=>[point[0]*(1-eta()*config.a),point[1]*(1-eta()*config.b)];
    const gradientNorm=point=>Math.hypot(config.a*point[0],config.b*point[1]);
    // One scale for both axes: with different screen scales the kappa=1 surface was drawn as
    // ellipses, contradicting the slide that calls its curvature equal.
    const viewport=(width,height)=>{
      const innerWidth=width-pad.left-pad.right,innerHeight=height-pad.top-pad.bottom;
      const scale=Math.min(innerWidth/(2*maxX),innerHeight/(2*maxY));
      return {scale,cx:pad.left+innerWidth/2,cy:pad.top+innerHeight/2,rangeX:innerWidth/(2*scale),rangeY:innerHeight/(2*scale)};
    };
    const screen=(point,box)=>[box.cx+point[0]*box.scale,box.cy-point[1]*box.scale];

    function resize(){
      const rect=canvas.getBoundingClientRect();
      const dpr=window.devicePixelRatio||1;
      const width=Math.max(1,Math.round(rect.width*dpr));
      const height=Math.max(1,Math.round(rect.height*dpr));
      if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
      return {width:rect.width,height:rect.height,dpr};
    }

    function clipped(point,box){return [clamp(point[0],-box.rangeX,box.rangeX),clamp(point[1],-box.rangeY,box.rangeY)];}

    function drawArrow(ctx,from,to,color){
      const dx=to[0]-from[0],dy=to[1]-from[1],length=Math.hypot(dx,dy);
      if(length<2)return;
      const angle=Math.atan2(dy,dx),head=10;
      ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=4;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(from[0],from[1]);ctx.lineTo(to[0],to[1]);ctx.stroke();
      ctx.beginPath();ctx.moveTo(to[0],to[1]);ctx.lineTo(to[0]-head*Math.cos(angle-.48),to[1]-head*Math.sin(angle-.48));ctx.lineTo(to[0]-head*Math.cos(angle+.48),to[1]-head*Math.sin(angle+.48));ctx.closePath();ctx.fill();
    }

    function draw(){
      const {width,height,dpr}=resize();
      etaOutput.textContent=`η = ${comma(eta())}`;
      gradientOutput.textContent=gradientNorm(state.display).toFixed(2).replace('.',',');
      iterationOutput.textContent=String(state.iteration);
      playButton.textContent=state.running?'Пауза':'Запустить';
      if(width<100||height<100)return;
      context.setTransform(dpr,0,0,dpr,0,0);
      context.clearRect(0,0,width,height);
      context.fillStyle=palette.paper;context.fillRect(0,0,width,height);
      const box=viewport(width,height);
      const {cx,cy,scale}=box;
      state.range=[box.rangeX,box.rangeY];
      const aspect=Math.sqrt(config.a/config.b);

      context.strokeStyle=palette.line;context.lineWidth=2;
      context.beginPath();context.moveTo(pad.left,cy);context.lineTo(width-pad.right,cy);context.moveTo(cx,pad.top);context.lineTo(cx,height-pad.bottom);context.stroke();

      context.strokeStyle=palette.contour;context.lineWidth=2.5;
      [0.65,1.25,2.05,3.0,3.9].forEach(radius=>{
        context.beginPath();
        context.ellipse(cx,cy,radius*scale,radius*aspect*scale,0,0,Math.PI*2);
        context.stroke();
      });

      context.fillStyle=palette.ink;context.beginPath();context.arc(cx,cy,6,0,Math.PI*2);context.fill();
      context.font='600 22px Montserrat, Arial, sans-serif';context.fillText('min',cx+12,cy-12);

      const trail=state.history.map(point=>screen(clipped(point,box),box));
      const current=screen(clipped(state.display,box),box);
      if(trail.length){
        context.strokeStyle=config.color;context.lineWidth=5;context.lineJoin='round';context.lineCap='round';
        context.beginPath();context.moveTo(...trail[0]);trail.slice(1).forEach(point=>context.lineTo(...point));context.lineTo(...current);context.stroke();
        context.fillStyle=config.color;
        trail.forEach(point=>{context.beginPath();context.arc(point[0],point[1],5,0,Math.PI*2);context.fill();});
      }

      const candidate=screen(clipped(nextPoint(state.display),box),box);
      drawArrow(context,current,candidate,config.color);
      context.fillStyle=config.color;context.beginPath();context.arc(current[0],current[1],9,0,Math.PI*2);context.fill();

    }

    function reset({running=state.running}={}){
      state.point=[...config.start];state.display=[...config.start];state.history=[[...config.start]];state.iteration=0;state.segment=null;state.restartAt=0;state.running=running&&!reduced&&!pdf;draw();
    }

    function commitStep(){
      const target=nextPoint(state.point);
      state.point=target;state.display=target;state.history.push([...target]);state.iteration+=1;state.segment=null;
      const outside=Math.abs(target[0])>state.range[0]||Math.abs(target[1])>state.range[1];
      const done=gradientNorm(target)<.04||state.iteration>=config.maxSteps;
      if(outside||done){state.running=false;state.restartAt=performance.now()+1400;}
      draw();
    }

    function singleStep(){
      state.running=false;state.restartAt=0;
      const target=nextPoint(state.point);
      state.point=target;state.display=target;state.history.push([...target]);state.iteration+=1;state.segment=null;draw();
    }

    function advance(time){
      if(!root.closest('section')?.classList.contains('present'))return;
      if(state.restartAt&&time>=state.restartAt)reset({running:true});
      if(!state.running)return;
      if(!state.segment)state.segment={from:[...state.point],to:nextPoint(state.point),start:time};
      const progress=clamp((time-state.segment.start)/520,0,1);
      const eased=1-Math.pow(1-progress,3);
      state.display=[state.segment.from[0]+(state.segment.to[0]-state.segment.from[0])*eased,state.segment.from[1]+(state.segment.to[1]-state.segment.from[1])*eased];
      draw();
      if(progress>=1)commitStep();
    }

    function makeStatic(){
      reset({running:false});
      const steps=config===configs.normalized?7:config===configs.explode?4:8;
      for(let index=0;index<steps;index+=1){
        const target=nextPoint(state.point);state.point=target;state.display=target;state.history.push([...target]);state.iteration+=1;
        if(Math.abs(target[0])>state.range[0]||Math.abs(target[1])>state.range[1])break;
      }
      draw();
    }

    slider.addEventListener('input',()=>reset({running:true}));
    playButton.addEventListener('click',()=>{state.running=!state.running;state.restartAt=0;state.segment=null;draw();});
    root.querySelector('[data-gd-action="step"]').addEventListener('click',singleStep);
    root.querySelector('[data-gd-action="reset"]').addEventListener('click',()=>reset({running:!reduced&&!pdf}));
    window.addEventListener('resize',draw);
    if(reduced||pdf)makeStatic();else draw();
    return {advance,reset,draw,makeStatic};
  }

  const labs=[...document.querySelectorAll('[data-gd-lab]')].map(createLab);
  if(!labs.length)return;
  function frame(time){labs.forEach(lab=>lab.advance(time));requestAnimationFrame(frame);}
  if(!reduced&&!pdf)requestAnimationFrame(frame);
  window.deck?.on('slidechanged',()=>labs.forEach(lab=>lab.reset({running:true})));
})();

(() => {
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pdf=new URLSearchParams(location.search).has('pdf');
  const palette={ink:'#1e1e1f',muted:'#6f6f6a',line:'#d7d7d2',blue:'#3157b7',red:'#c63d4f',paper:'#fffdf7'};
  const roots=[...document.querySelectorAll('[data-loss-compare]')];
  if(!roots.length)return;

  function createComparison(root){
    const canvas=root.querySelector('canvas');
    const context=canvas.getContext('2d');
    const iterationOutput=root.querySelector('[data-loss-iteration]');
    const playButton=root.querySelector('[data-loss-action="play"]');
    const eta=.25,maxIteration=10;
    const series=[];
    let mseError=2,maeError=2;
    for(let iteration=0;iteration<=maxIteration;iteration+=1){
      series.push({iteration,mseLoss:mseError**2,maeLoss:Math.abs(maeError),mseGradient:2*Math.abs(mseError),maeGradient:Math.abs(maeError)<1e-9?0:1});
      mseError-=eta*2*mseError;
      maeError-=eta*Math.sign(maeError);
      if(Math.abs(maeError)<1e-9)maeError=0;
    }
    const state={iteration:reduced||pdf?maxIteration:0,running:!reduced&&!pdf,lastStep:0};

    function resize(){
      const rect=canvas.getBoundingClientRect();
      const dpr=window.devicePixelRatio||1;
      const width=Math.max(1,Math.round(rect.width*dpr));
      const height=Math.max(1,Math.round(rect.height*dpr));
      if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
      return {width:rect.width,height:rect.height,dpr};
    }

    function arrow(ctx,x1,y1,x2,y2){
      ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
      ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-9,y2-5);ctx.lineTo(x2-9,y2+5);ctx.closePath();ctx.fill();
    }

    function drawPanel({x,y,width,height,title,keyMse,keyMae,maxY}){
      const pad={left:58,right:18,top:66,bottom:48};
      const sx=value=>x+pad.left+value/maxIteration*(width-pad.left-pad.right);
      const sy=value=>y+pad.top+(1-value/maxY)*(height-pad.top-pad.bottom);
      context.fillStyle=palette.ink;context.font='600 24px Montserrat, Arial, sans-serif';context.textAlign='center';context.fillText(title,x+width/2,y+25);
      // The experiment is a scalar toy, not model training: say so on the canvas itself.
      context.fillStyle=palette.muted;context.font='500 18px Montserrat, Arial, sans-serif';
      context.fillText(`скалярная задача min ℓ(r) · r₀ = 2 · η = ${eta.toFixed(2).replace('.',',')}`,x+width/2,y+50);
      context.strokeStyle=palette.line;context.fillStyle=palette.line;context.lineWidth=2;
      arrow(context,x+pad.left,y+height-pad.bottom,x+width-pad.right+5,y+height-pad.bottom);
      context.beginPath();context.moveTo(x+pad.left,y+height-pad.bottom);context.lineTo(x+pad.left,y+pad.top-5);context.stroke();
      context.beginPath();context.moveTo(x+pad.left,y+pad.top-5);context.lineTo(x+pad.left-5,y+pad.top+4);context.lineTo(x+pad.left+5,y+pad.top+4);context.closePath();context.fill();
      context.fillStyle=palette.muted;context.font='500 18px Montserrat, Arial, sans-serif';context.textAlign='center';
      [0,2,4,6,8,10].forEach(value=>{const px=sx(value);context.beginPath();context.moveTo(px,y+height-pad.bottom);context.lineTo(px,y+height-pad.bottom+6);context.stroke();context.fillText(String(value),px,y+height-pad.bottom+26);});
      context.fillText('итерация t',x+width/2,y+height-3);
      context.textAlign='right';
      [0,maxY/2,maxY].forEach(value=>{const py=sy(value);context.beginPath();context.moveTo(x+pad.left-6,py);context.lineTo(x+pad.left,py);context.stroke();context.fillText(String(value).replace('.',','),x+pad.left-10,py+6);});

      const shown=series.slice(0,state.iteration+1);
      [[keyMse,palette.blue],[keyMae,palette.red]].forEach(([key,color])=>{
        context.strokeStyle=color;context.fillStyle=color;context.lineWidth=4;context.lineJoin='round';context.lineCap='round';
        context.beginPath();shown.forEach((item,index)=>{const point=[sx(item.iteration),sy(item[key])];if(index===0)context.moveTo(...point);else context.lineTo(...point);});context.stroke();
        shown.forEach(item=>{context.beginPath();context.arc(sx(item.iteration),sy(item[key]),5,0,Math.PI*2);context.fill();});
      });
    }

    function draw(){
      const {width,height,dpr}=resize();
      iterationOutput.textContent=String(state.iteration);
      playButton.textContent=state.running?'Пауза':'Запустить';
      if(width<100||height<100)return;
      context.setTransform(dpr,0,0,dpr,0,0);context.clearRect(0,0,width,height);context.fillStyle=palette.paper;context.fillRect(0,0,width,height);
      const gap=34,panelWidth=(width-gap)/2;
      drawPanel({x:0,y:0,width:panelWidth,height,title:'Модуль производной по r',keyMse:'mseGradient',keyMae:'maeGradient',maxY:4});
      drawPanel({x:panelWidth+gap,y:0,width:panelWidth,height,title:'Значение потери ℓ(r)',keyMse:'mseLoss',keyMae:'maeLoss',maxY:4});
    }

    function reset({running=!reduced&&!pdf}={}){state.iteration=reduced||pdf?maxIteration:0;state.running=running&&!reduced&&!pdf;state.lastStep=0;draw();}
    function step(){state.running=false;state.iteration=Math.min(maxIteration,state.iteration+1);draw();}
    function advance(time){
      if(!root.closest('section')?.classList.contains('present')||!state.running)return;
      if(!state.lastStep)state.lastStep=time;
      if(time-state.lastStep<520)return;
      state.lastStep=time;state.iteration+=1;
      if(state.iteration>=maxIteration){state.iteration=maxIteration;state.running=false;}
      draw();
    }

    playButton.addEventListener('click',()=>{state.running=!state.running;state.lastStep=0;draw();});
    root.querySelector('[data-loss-action="step"]').addEventListener('click',step);
    root.querySelector('[data-loss-action="reset"]').addEventListener('click',()=>reset());
    window.addEventListener('resize',draw);draw();
    return {advance,reset};
  }

  const comparisons=roots.map(createComparison);
  function frame(time){comparisons.forEach(comparison=>comparison.advance(time));requestAnimationFrame(frame);}
  if(!reduced&&!pdf)requestAnimationFrame(frame);
  window.deck?.on('slidechanged',()=>comparisons.forEach(comparison=>comparison.reset()));
})();
