// Initialize Pyodide
let pyodideReadyPromise;

async function initializePyodide() {
  try {
    self.pyodide = await loadPyodide();
    console.log("Pyodide initialized successfully");
    return self.pyodide;
  } catch (error) {
    console.error("Error initializing Pyodide:", error);
    document.getElementById("output").textContent = "Error initializing Python runtime. Please try again later.";
    document.getElementById("run-button").disabled = true;
  }
}

// Initialize when the page loads
document.addEventListener("DOMContentLoaded", () => {
  // Initialize syntax highlighting
  hljs.highlightAll();
  
  // Initialize Pyodide
  pyodideReadyPromise = initializePyodide();
  
  // Set up the run button
  const runButton = document.getElementById("run-button");
  const clearButton = document.getElementById("clear-button");
  const outputElement = document.getElementById("output");
  const codeTextarea = document.getElementById("python-code");
  
  // Run Python code when the run button is clicked
  runButton.addEventListener("click", async () => {
    if (!pyodideReadyPromise) {
      outputElement.textContent = "Python runtime is not initialized yet.";
      return;
    }
    
    runButton.disabled = true;
    runButton.textContent = "Running...";
    outputElement.textContent = "Running Python code...";
    
    try {
      const pyodide = await pyodideReadyPromise;
      
      // Setup the output capture using a string variable the Python code will write to
      await pyodide.runPythonAsync(`
        _output_buffer = []
        
        def print(*args, sep=' ', end='\\n'):
            """Override the built-in print function to capture output."""
            output = sep.join(str(arg) for arg in args) + end
            _output_buffer.append(output)
      `);
      
      // Get the Python code from the textarea
      const pythonCode = codeTextarea.value;
      
      // Run the Python code
      await pyodide.runPythonAsync(pythonCode);
      
      // Get the captured output
      const output = await pyodide.runPythonAsync("''.join(_output_buffer)");
      
      // Display the output
      outputElement.textContent = output;
      
    } catch (error) {
      // Display any errors that occurred
      outputElement.textContent = `Error: ${error.message}`;
    } finally {
      runButton.disabled = false;
      runButton.textContent = "Run Python Code";
    }
  });
  
  // Clear the output when the clear button is clicked
  clearButton.addEventListener("click", () => {
    outputElement.textContent = "";
  });
});

// Smooth scrolling for navigation links
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop,
          behavior: 'smooth'
        });
      }
    });
  });
});

// Add animation effects when scrolling
document.addEventListener("DOMContentLoaded", () => {
  // Add a class to elements when they come into view
  const elements = document.querySelectorAll('.section');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });
  
  elements.forEach(element => {
    observer.observe(element);
  });
});

// Update copyright year automatically
document.addEventListener("DOMContentLoaded", () => {
  const currentYear = new Date().getFullYear();
  const copyrightElement = document.querySelector('footer p');
  
  if (copyrightElement) {
    copyrightElement.textContent = copyrightElement.textContent.replace(/\d{4}/, currentYear);
  }
}); 