// Switch between exact authored dot-product examples without changing the axes.
document.querySelectorAll('[data-template-choice]').forEach(button=>button.addEventListener('click',()=>{
 const index=button.dataset.templateChoice;
 document.querySelectorAll('[data-template-state]').forEach(state=>{state.hidden=state.dataset.templateState!==index;});
 document.querySelectorAll('[data-template-choice]').forEach(control=>control.setAttribute('aria-pressed',String(control===button)));
}));
