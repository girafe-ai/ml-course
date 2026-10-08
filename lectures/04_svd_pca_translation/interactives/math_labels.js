/* Local math labels; numerical state keeps its existing internal row convention. */
document.querySelectorAll('[data-tex]').forEach(element => {
  katex.render(element.dataset.tex, element, {throwOnError: true, output: 'htmlAndMathml'});
});
