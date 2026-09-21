/**
 * Beyond Tour — Vendor Hotel & Homestay Editor Controller
 * Manages autosaving hotel fields, interactive amenity toggles, client-side canvas
 * photo compression, and WebP uploads.
 */

function initVendorHotelEditor() {
  if (typeof Alpine === 'undefined') return;

  Alpine.data('vendorHotelEditor', (hotelId, csrfToken) => {
    const dataElem = document.getElementById('hotel-editor-data');
    const cfg = dataElem ? JSON.parse(dataElem.textContent || '{}') : {};

    const isHindi = Boolean(cfg.isHindi);
    const coverUrl = cfg.coverUrl || '';
    const amenitiesList = Array.isArray(cfg.amenitiesList) ? [...cfg.amenitiesList] : [];

    return {
      openSection: 1,
      saveStatus: 'idle',
      statusText: isHindi ? 'सभी परिवर्तन सुरक्षित हैं' : 'All changes saved',
      coverUrl: coverUrl,
      amenitiesRaw: amenitiesList.join(', '),
      amenitiesList: amenitiesList,
      uploadProgress: 0,
      compressionStats: '',

      saveField(fieldName, fieldValue) {
        this.saveStatus = 'saving';
        this.statusText = isHindi ? 'सहेजा जा रहा है...' : 'Saving...';

        const token = csrfToken || document.querySelector('meta[name=csrf-token]')?.content || '';

        fetch(`/dashboard/business/hotel/${hotelId}/autosave`, {
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
      },

      toggleAmenity(item) {
        const idx = this.amenitiesList.indexOf(item);
        if (idx > -1) {
          this.amenitiesList.splice(idx, 1);
        } else {
          this.amenitiesList.push(item);
        }
        this.amenitiesRaw = this.amenitiesList.join(', ');
        this.saveField('amenities', this.amenitiesRaw);
      },

      handlePhotoUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.uploadProgress = 10;
        this.compressionStats = isHindi ? 'कैनवास कंप्रेस किया जा रहा है...' : 'Compressing image on device...';

        const originalSizeKB = Math.round(file.size / 1024);
        const reader = new FileReader();

        reader.onload = (e) => {
          const img = new Image();
          img.onload = () => {
            this.uploadProgress = 40;

            const maxDim = 1200;
            let width = img.width;
            let height = img.height;
            if (width > height) {
              if (width > maxDim) {
                height = Math.round((height * maxDim) / width);
                width = maxDim;
              }
            } else {
              if (height > maxDim) {
                width = Math.round((width * maxDim) / height);
                height = maxDim;
              }
            }

            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);

            const dataUrl = canvas.toDataURL('image/webp', 0.8) || canvas.toDataURL('image/jpeg', 0.8);
            const compressedSizeKB = Math.round((dataUrl.length * 3 / 4) / 1024);

            this.uploadProgress = 70;
            this.compressionStats = `Compressed ${originalSizeKB} KB -> ${compressedSizeKB} KB (${Math.round((1 - compressedSizeKB / originalSizeKB) * 100)}% saved). Uploading...`;

            const token = csrfToken || document.querySelector('meta[name=csrf-token]')?.content || '';

            fetch(`/dashboard/business/hotel/${hotelId}/upload-photo`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
              },
              body: JSON.stringify({ data_url: dataUrl })
            })
            .then((r) => r.json())
            .then((data) => {
              if (data.status === 'success') {
                this.uploadProgress = 100;
                this.coverUrl = data.image_url;
                this.compressionStats = isHindi ? 'सफलतापूर्वक अपलोड किया गया!' : 'Compressed photo uploaded successfully!';
                setTimeout(() => { this.uploadProgress = 0; }, 3000);
              } else {
                this.compressionStats = isHindi ? 'अपलोड विफल रहा।' : 'Upload failed.';
              }
            })
            .catch(() => {
              this.compressionStats = isHindi ? 'नेटवर्क त्रुटि।' : 'Network upload error.';
            });
          };
          img.src = e.target.result;
        };

        reader.readAsDataURL(file);
      }
    };
  });
}

if (window.Alpine) {
  initVendorHotelEditor();
} else {
  document.addEventListener('alpine:init', initVendorHotelEditor);
}
