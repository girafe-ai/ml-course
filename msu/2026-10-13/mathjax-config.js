/* MathJax 3.2.2 loaded from its pinned CDN release. */
window.MathJax = {
  loader: {load: ['[tex]/boldsymbol'], paths: {tex: 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/input/tex/extensions'}},
  tex: {inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']], packages: ['base', 'ams', 'newcommand', 'boldsymbol'], processEscapes: true},
  svg: {fontCache: 'local'},
  options: {enableMenu: false, enableAssistiveMml: false, skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']},
  startup: {pageReady: function () {return MathJax.startup.defaultPageReady().then(function () {document.documentElement.dataset.mathReady = 'true';});}}
};
