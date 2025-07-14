// Enhanced form handling and UI interactions
class PredictivePulse {
  constructor() {
    this.form = document.getElementById('prediction-form');
    this.submitBtn = document.getElementById('submit-btn');
    this.loadingState = false;
    
    this.init();
  }
  
  init() {
    this.setupFormValidation();
    this.setupFormSubmission();
    this.setupTooltips();
    this.setupAnimations();
  }
  
  setupFormValidation() {
    const inputs = this.form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
      input.addEventListener('input', () => this.validateField(input));
      input.addEventListener('blur', () => this.validateField(input));
    });
  }
  
  validateField(field) {
    const value = field.value.trim();
    const isValid = this.isFieldValid(field, value);
    
    this.updateFieldState(field, isValid);
    this.updateSubmitButton();
    
    return isValid;
  }
  
  isFieldValid(field, value) {
    if (!value) return false;
    
    const min = parseInt(field.getAttribute('min'));
    const max = parseInt(field.getAttribute('max'));
    const numValue = parseInt(value);
    
    if (isNaN(numValue)) return false;
    if (min !== null && numValue < min) return false;
    if (max !== null && numValue > max) return false;
    
    return true;
  }
  
  updateFieldState(field, isValid) {
    const formGroup = field.closest('.form-group');
    
    if (isValid) {
      field.classList.remove('error');
      field.classList.add('valid');
      formGroup.classList.remove('error');
    } else {
      field.classList.remove('valid');
      field.classList.add('error');
      formGroup.classList.add('error');
    }
  }
  
  updateSubmitButton() {
    const allInputs = this.form.querySelectorAll('input[required], select[required]');
    const allValid = Array.from(allInputs).every(input => 
      this.isFieldValid(input, input.value.trim())
    );
    
    this.submitBtn.disabled = !allValid || this.loadingState;
  }
  
  setupFormSubmission() {
    this.form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleSubmit();
    });
  }
  
  async handleSubmit() {
    if (this.loadingState) return;
    
    this.setLoadingState(true);
    
    try {
      const formData = new FormData(this.form);
      
      // Simulate API call delay for better UX
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const response = await fetch('/predict', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        window.location.href = response.url;
      } else {
        throw new Error('Prediction failed');
      }
    } catch (error) {
      this.showError('An error occurred while processing your request. Please try again.');
    } finally {
      this.setLoadingState(false);
    }
  }
  
  setLoadingState(loading) {
    this.loadingState = loading;
    const loadingSpinner = this.submitBtn.querySelector('.loading');
    const buttonText = this.submitBtn.querySelector('.btn-text');
    
    if (loading) {
      loadingSpinner.classList.remove('hidden');
      buttonText.textContent = 'Analyzing...';
      this.submitBtn.disabled = true;
    } else {
      loadingSpinner.classList.add('hidden');
      buttonText.textContent = 'Predict Blood Pressure Stage';
      this.updateSubmitButton();
    }
  }
  
  showError(message) {
    // Create and show error notification
    const notification = document.createElement('div');
    notification.className = 'notification error';
    notification.innerHTML = `
      <div class="notification-content">
        <strong>Error:</strong> ${message}
      </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.remove();
    }, 5000);
  }
  
  setupTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
      trigger.addEventListener('mouseenter', (e) => this.showTooltip(e));
      trigger.addEventListener('mouseleave', () => this.hideTooltip());
    });
  }
  
  showTooltip(e) {
    const text = e.target.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
  }
  
  hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
      tooltip.remove();
    }
  }
  
  setupAnimations() {
    // Intersection Observer for fade-in animations
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-up');
        }
      });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.card, .hero').forEach(el => {
      observer.observe(el);
    });
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new PredictivePulse();
});

// Additional utility functions
function formatBloodPressure(systolic, diastolic) {
  return `${systolic}/${diastolic} mmHg`;
}

function getStageColor(stage) {
  const colors = {
    'Normal': '#22c55e',
    'Elevated': '#f59e0b',
    'Hypertension Stage 1': '#f97316',
    'Hypertension Stage 2': '#ef4444',
    'Hypertensive Crisis': '#991b1b'
  };
  return colors[stage] || '#64748b';
}

function getStageRecommendations(stage) {
  const recommendations = {
    'Normal': [
      'Maintain a healthy diet rich in fruits and vegetables',
      'Exercise regularly (at least 150 minutes per week)',
      'Limit sodium intake to less than 2,300mg per day',
      'Monitor blood pressure annually'
    ],
    'Elevated': [
      'Adopt heart-healthy lifestyle changes',
      'Reduce sodium intake significantly',
      'Increase physical activity',
      'Monitor blood pressure every 3-6 months'
    ],
    'Hypertension Stage 1': [
      'Consult with healthcare provider about treatment options',
      'Consider medication if lifestyle changes are insufficient',
      'Monitor blood pressure monthly',
      'Implement stress management techniques'
    ],
    'Hypertension Stage 2': [
      'Seek immediate medical attention',
      'Likely need combination of medications',
      'Monitor blood pressure weekly',
      'Make comprehensive lifestyle changes'
    ],
    'Hypertensive Crisis': [
      'Seek emergency medical care immediately',
      'Do not delay treatment',
      'May require hospitalization',
      'Follow strict medical supervision'
    ]
  };
  return recommendations[stage] || [];
}