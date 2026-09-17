/* Local-only Reveal.js presentation; no network dependencies. */
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const pdf = new URLSearchParams(location.search).has('pdf');
window.deck = new Reveal(document.querySelector('.reveal'), {
  width:1600,height:900,margin:0.015,minScale:0.1,maxScale:2,
  controls:true,progress:true,hash:true,history:true,center:false,
  transition:reduced?'none':'fade',transitionSpeed:'fast',
  backgroundTransition:'none',autoAnimateDuration:reduced?0:0.65,
  autoAnimateEasing:'ease-in-out',keyboard:!pdf,touch:!pdf,
  pdfSeparateFragments:false,help:true
});
window.deck.initialize().then(()=>{
 document.documentElement.dataset.ready='true';
 if(pdf){document.querySelectorAll('.fragment').forEach(e=>e.classList.add('visible'));}
});

