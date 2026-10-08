/* Pinned local MathJax 3.2.2. No CDN, optional remote components or fonts. */
window.MathJax = {
  tex: {inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']], packages: ['base', 'ams', 'newcommand', 'boldsymbol'], processEscapes: true},
  svg: {fontCache: 'local'},
  options: {enableMenu: false, enableAssistiveMml: false, skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']},
  startup: {pageReady: function () {return MathJax.startup.defaultPageReady().then(function () {document.documentElement.dataset.mathReady = 'true';});}}
};
