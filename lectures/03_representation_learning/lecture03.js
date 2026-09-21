(()=>{const finish=()=>document.documentElement.dataset.ready='true'; if(document.fonts?.ready)document.fonts.ready.then(()=>requestAnimationFrame(finish));else finish();})();
