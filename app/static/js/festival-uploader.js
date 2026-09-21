/**
 * Beyond Tour — Festival & Heritage Media Uploader Controller
 * Handles drag-and-drop and file input uploads for photos and videos with instant local preview.
 */

function festivalUploader(customUploadUrl) {
  const uploadUrl = customUploadUrl || '/dashboard/business/festival/upload-media';

  return {
    photoDragging: false,
    photoPreview: '',
    photoUrl: '',
    photoUploading: false,

    videoDragging: false,
    videoPreview: '',
    videoUrl: '',
    videoUploading: false,

    handlePhotoDrop(e) {
      this.photoDragging = false;
      const files = e.dataTransfer?.files;
      if (files && files.length > 0) {
        this.uploadFile(files[0], 'photo');
      }
    },

    handlePhotoSelect(e) {
      const files = e.target.files;
      if (files && files.length > 0) {
        this.uploadFile(files[0], 'photo');
      }
    },

    handleVideoDrop(e) {
      this.videoDragging = false;
      const files = e.dataTransfer?.files;
      if (files && files.length > 0) {
        this.uploadFile(files[0], 'video');
      }
    },

    handleVideoSelect(e) {
      const files = e.target.files;
      if (files && files.length > 0) {
        this.uploadFile(files[0], 'video');
      }
    },

    uploadFile(file, type) {
      const formData = new FormData();
      formData.append('file', file);

      const csrfToken = document.querySelector('meta[name=csrf-token]')?.content ||
        document.querySelector('input[name=csrf_token]')?.value || '';

      if (type === 'photo') {
        this.photoUploading = true;
        const reader = new FileReader();
        reader.onload = (e) => { this.photoPreview = e.target.result; };
        reader.readAsDataURL(file);

        fetch(uploadUrl, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken
          },
          body: formData
        })
        .then((res) => res.json())
        .then((data) => {
          this.photoUploading = false;
          if (data.status === 'success') {
            this.photoUrl = data.url;
            this.photoPreview = data.url;
          }
        })
        .catch((err) => {
          this.photoUploading = false;
          console.error('Photo upload error:', err);
        });
      } else {
        this.videoUploading = true;
        const reader = new FileReader();
        reader.onload = (e) => { this.videoPreview = e.target.result; };
        reader.readAsDataURL(file);

        fetch(uploadUrl, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken
          },
          body: formData
        })
        .then((res) => res.json())
        .then((data) => {
          this.videoUploading = false;
          if (data.status === 'success') {
            this.videoUrl = data.url;
            this.videoPreview = data.url;
          }
        })
        .catch((err) => {
          this.videoUploading = false;
          console.error('Video upload error:', err);
        });
      }
    },

    init() {
      if (window.lucide && typeof window.lucide.createIcons === 'function') {
        window.lucide.createIcons();
      }
    }
  };
}

window.festivalUploader = festivalUploader;
