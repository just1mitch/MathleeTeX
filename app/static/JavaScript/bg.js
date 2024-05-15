
function addEquation() {
  const equation = document.createElement('div');
  equation.className = 'equation';

  // Use KaTeX to render the random equation immediately upon creation
  const equationText = generateRandomEquation();
  katex.render(equationText, equation);

  // Append first, then position
  document.getElementById('equation-background').appendChild(equation);

  const startFromLeft = Math.random() < 0.5;
  let startX = randomPercentage(700, 200, startFromLeft);
  let startY = randomPercentage(700, 150); // Randomize the vertical start slightly
  let endX = randomPercentage(400, 100, !startFromLeft); // Opposite direction from startX
  let endY = randomPercentage(20, 250); // Slightly randomize the vertical end
  equation.style.setProperty('--start-x', startX);
  equation.style.setProperty('--start-y', startY);
  equation.style.setProperty('--end-x', endX);
  equation.style.setProperty('--end-y', endY);

  // Trigger the animation - controlled by CSS
  equation.classList.add('fly');

  // Remove the equation after it animates out of view
  setTimeout(() => {
      equation.remove();
  }, 5000); // Matches animation duration
}

// Add a new equation at intervals for performance
setInterval(addEquation, 300);

function randomPercentage(range, offset, isNegative = false) {
  let baseValue = Math.random() * range - offset;
  return `${isNegative ? baseValue * -1 : baseValue}%`;
}

// Generate a random equation from a predefined list - thanks chatgpt for creating this list
function generateRandomEquation() {
  const equations = [
      'E=mc^2',
      '\\int_0^\\infty e^{-x^2} dx=\\frac{\\sqrt{\\pi}}{2}',
      '\\frac{d}{dx} (\\sin x) = \\cos x',
      '\\sum_{n=1}^\\infty \\frac{1}{n^2} = \\frac{\\pi^2}{6}',
      '\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1',
      'f(x) = a_0 + \\sum_{n=1}^\\infty (a_n \\cos nx + b_n \\sin nx)',
      '\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}',
      '\\nabla \\times \\mathbf{B} - \\frac{1}{c^2} \\frac{\\partial \\mathbf{E}}{\\partial t} = \\mu_0 \\mathbf{J}',
      '\\int_a^b f(x)\\,dx = F(b) - F(a)',
      '\\left(\\frac{x^2}{y^3}\\right)^4',
      '\\frac{d}{dx}\\left(\\int_{0}^{x} f(u)\\,du\\right)=f(x)',
      '\\sqrt{\\frac{a}{b}}',
      '\\frac{d}{dx}e^{ax}=ae^{ax}',
      '\\sqrt[3]{x^3 + y^3}',
      '\\frac{\\partial u}{\\partial t} + (u \\cdot \\nabla)u = -\\frac{1}{\\rho}\\nabla p + \\nu\\nabla^2u'
  ];
  return equations[Math.floor(Math.random() * equations.length)];
}
