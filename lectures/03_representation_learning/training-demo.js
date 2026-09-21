// The checkpoints are produced by real deterministic SGNS optimization in training-demo.mjs.
(()=>{
 const dataNode=document.querySelector('#sgns-training-data');
 const slider=document.querySelector('#sgns-training-step');
 if(!dataNode||!slider)return;
 const data=JSON.parse(dataNode.textContent),plot=document.querySelector('[data-sgns-plot="current"]');
 const fmt=value=>value.toFixed(3).replace('.',','),scale=130/data.extent,cx=x=>300+scale*x,cy=y=>210-scale*y;
 function update(){
  const checkpoint=data.checkpoints[Number(slider.value)];
  checkpoint.central.forEach(([x,y],i)=>{
   const group=plot.querySelector(`[data-word-index="${i}"]`),circle=group.querySelector('circle'),line=group.querySelector('line');
   circle.setAttribute('cx',cx(x));circle.setAttribute('cy',cy(y));line.setAttribute('x1',cx(x));line.setAttribute('y1',cy(y));
  });
  const index=Number(slider.value),last=data.checkpoints.length-1;
  document.querySelector('#sgns-panel-label').textContent=index===0?'До обучения':index===last?'После обучения':'Во время обучения';
  document.querySelector('#sgns-step-label').textContent=`шаг ${checkpoint.step}`;
  document.querySelector('#sgns-objective').textContent=fmt(checkpoint.objective);
 }
 slider.addEventListener('input',update);
 slider.addEventListener('keydown',event=>event.stopPropagation());
 update();
})();
