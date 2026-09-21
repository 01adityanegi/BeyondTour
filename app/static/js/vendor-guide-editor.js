/**
 * Beyond Tour — Vendor Guide Profile Editor Controller
 * Handles autosaving of certified guide fields and bilingual status notifications.
 */

function initVendorGuideEditor() {
  if (typeof Alpine === 'undefined') return;

  Alpine.data('vendorGuideEditor', (guideId, csrfToken, isHindi = false) => ({
    openSection: 1,
    saveStatus: 'idle',
    statusText: isHindi ? 'सभी परिवर्तन सुरक्षित हैं' : 'All changes saved',

    saveField(fieldName, fieldValue) {
      this.saveStatus = 'saving';
      this.statusText = isHindi ? 'सहेजा जा रहा है...' : 'Saving...';

      const token = csrfToken || document.querySelector('meta[name=csrf-token]')?.content || '';

      fetch(`/dashboard/business/guide/${guideId}/autosave`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': token
        },
        body: JSON.stringify({
          field: fieldName,
          value: fieldValue
        })
      })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === 'saved') {
          this.saveStatus = 'saved';
          this.statusText = (isHindi ? 'सहेजा गया ' : 'Saved at ') + data.time;
        } else {
          this.saveStatus = 'error';
          this.statusText = isHindi ? 'सहेजने में त्रुटि' : 'Error saving';
        }
      })
      .catch(() => {
        this.saveStatus = 'error';
        this.statusText = isHindi ? 'कनेक्शन त्रुटि' : 'Connection error';
      });
    }
  }));
}

if (window.Alpine) {
  initVendorGuideEditor();
} else {
  document.addEventListener('alpine:init', initVendorGuideEditor);
}
