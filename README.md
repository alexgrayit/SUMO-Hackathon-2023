<script type="text/javascript"
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [['$','$'], ['\\(','\\)']],
      processEscapes: true},
      jax: ["input/TeX","input/MathML","input/AsciiMath","output/CommonHTML"],
      extensions: ["tex2jax.js","mml2jax.js","asciimath2jax.js","MathMenu.js","MathZoom.js","AssistiveMML.js", "[Contrib]/a11y/accessibility-menu.js"],
      TeX: {
      extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"],
      equationNumbers: {
      autoNumber: "AMS"
      }
    }
  });
</script>

# SUMO Hackathon 2023

## Problem 1
### Definitions and Parameters
For this problem we define that the input file will be in the form
```
<N_laps>, <n_sensors>
<x_1>, <y_1>, <t_1>, <t_2>,... , <t_N>
<x_2>, <y_2>, <t_1>, <t_2>,... , <t_N>
.
.
.
<x_n>, <y_n>, <t_1>, <t_2>,... , <t_N>
```
Where the first line defines the number of laps (measurements made by each sensor) each subsequent
line corresponds to sensor $n$ and has an $$x$$ and a $$y$$ coordinate for that sensor as its first two items,
and then the following $$N$$ items are the times at which the car passed that sensor (in chronological order).
