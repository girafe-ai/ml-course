// No automatic animation: the teacher controls the orientation explicitly.
(()=>{
 const slider=document.querySelector('#model-angle');if(!slider)return;
 const observations=[[-1.5,-1,0],[-1,.8,0],[-.5,-.7,0],[.6,.5,1],[1,-.8,1],[1.5,1,1]];
 function update(){
  const degrees=Number(slider.value),a=degrees*Math.PI/180,w=[2*Math.cos(a),2*Math.sin(a)];
  let logL=0;for(const [x1,x2,y]of observations){const z=w[0]*x1+w[1]*x2;logL-=Math.log1p(Math.exp(-(2*y-1)*z));}
  // Equal axis scales preserve the geometry of the separating line.
  const dx=-Math.sin(a)*10,dy=Math.cos(a)*10;
  document.querySelector('.model-boundary').setAttribute('d',`M${340+130*dx} ${225-130*dy}L${340-130*dx} ${225+130*dy}`);
  document.querySelector('#angle-value').textContent=`${degrees}°`;
  document.querySelector('#likelihood-value').textContent=Math.exp(logL).toFixed(5).replace('.',',');
  document.querySelectorAll('[data-model-angle]').forEach(e=>e.classList.toggle('selected-model',Number(e.dataset.modelAngle)===degrees));
  document.querySelectorAll('[data-angle]').forEach(e=>e.setAttribute('aria-pressed',String(Number(e.dataset.angle)===degrees)));
 }
 slider.addEventListener('input',update);
 slider.addEventListener('keydown',e=>e.stopPropagation());
 document.querySelectorAll('[data-angle]').forEach(button=>button.addEventListener('click',()=>{slider.value=button.dataset.angle;update();}));
 update();
})();
