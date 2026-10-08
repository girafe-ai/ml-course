/* Offline slide navigation, mathematics and presenter notes. */
document.querySelectorAll('[data-tex]').forEach(node => {
  window.katex.render(node.getAttribute('data-tex'),node,{throwOnError:true,displayMode:node.tagName==='DIV',output:'htmlAndMathml'});
});
const deck = new Reveal({hash:true,controls:true,progress:true,center:false,transition:'none',width:1600,height:900,margin:0});
deck.initialize();
window.lectureDeck=deck;

document.addEventListener("keydown",event=>{if(event.key.toLowerCase()==="f"&&!event.metaKey&&!event.ctrlKey)document.documentElement.requestFullscreen?.()});
