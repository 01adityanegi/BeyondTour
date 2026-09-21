/**
 * BeyondTour - Community Upload & Media Sharing Manager
 * Handles photo drag-and-drop, video file drag-and-drop, YouTube 16:9 & Shorts 9:16
 * embed extraction, Instagram link validation, and multipart form submission.
 */

function communityUploadModal() {
  return {
    tab: 'photo',
    photoRatio: '4:5',
    photoPreviews: [],
    photoUrlInput: '',
    isDraggingPhoto: false,

    videoPreviewUrl: null,
    videoFileName: '',
    videoFileSize: '',
    videoFormat: '16:9',
    videoUrlInput: '',
    isDraggingVideo: false,

    ytUrl: '',
    ytId: '',
    ytError: false,

    shortsUrl: '',
    shortsId: '',
    shortsError: false,

    igUrl: '',
    igValid: false,

    caption: '',
    isSubmitting: false,

    init() {
      // Refresh lucide icons when tabs change or modal opens
      this.$watch('tab', () => {
        this.$nextTick(() => {
          if (window.lucide && typeof window.lucide.createIcons === 'function') {
            window.lucide.createIcons();
          }
        });
      });
    },

    // -------------------------------------------------------------
    // PHOTO DRAG & DROP AND FILE SELECTION
    // -------------------------------------------------------------
    handlePhotoDrop(e) {
      this.isDraggingPhoto = false;
      const files = e.dataTransfer ? e.dataTransfer.files : null;
      if (files && files.length > 0) {
        this.processPhotoFiles(files);
      }
    },

    handlePhotoSelect(e) {
      const files = e.target.files;
      if (files && files.length > 0) {
        this.processPhotoFiles(files);
      }
    },

    processPhotoFiles(files) {
      const allowedExts = ['image/jpeg', 'image/png', 'image/webp', 'image/avif', 'image/gif'];
      const dt = new DataTransfer();

      // Keep existing files if any
      if (this.$refs.photoInput && this.$refs.photoInput.files) {
        Array.from(this.$refs.photoInput.files).forEach(f => dt.items.add(f));
      }

      Array.from(files).forEach(file => {
        if (!file.type.startsWith('image/') && !allowedExts.includes(file.type)) {
          return;
        }
        dt.items.add(file);

        const reader = new FileReader();
        reader.onload = (evt) => {
          this.photoPreviews.push({
            url: evt.target.result,
            name: file.name,
            size: (file.size / 1024).toFixed(0) + ' KB'
          });
        };
        reader.readAsDataURL(file);
      });

      if (this.$refs.photoInput) {
        this.$refs.photoInput.files = dt.files;
      }
    },

    removePhoto(index) {
      this.photoPreviews.splice(index, 1);
      if (this.$refs.photoInput && this.$refs.photoInput.files) {
        const dt = new DataTransfer();
        const currentFiles = Array.from(this.$refs.photoInput.files);
        currentFiles.splice(index, 1);
        currentFiles.forEach(f => dt.items.add(f));
        this.$refs.photoInput.files = dt.files;
      }
    },

    // -------------------------------------------------------------
    // VIDEO DRAG & DROP AND FILE SELECTION
    // -------------------------------------------------------------
    handleVideoDrop(e) {
      this.isDraggingVideo = false;
      const files = e.dataTransfer ? e.dataTransfer.files : null;
      if (files && files.length > 0) {
        this.processVideoFile(files[0]);
      }
    },

    handleVideoSelect(e) {
      const files = e.target.files;
      if (files && files.length > 0) {
        this.processVideoFile(files[0]);
      }
    },

    processVideoFile(file) {
      if (!file || !file.type.startsWith('video/')) {
        alert('Please select a valid video file (.mp4, .webm, .mov)');
        return;
      }

      if (this.videoPreviewUrl) {
        URL.revokeObjectURL(this.videoPreviewUrl);
      }

      this.videoPreviewUrl = URL.createObjectURL(file);
      this.videoFileName = file.name;
      this.videoFileSize = (file.size / (1024 * 1024)).toFixed(1) + ' MB';

      const dt = new DataTransfer();
      dt.items.add(file);
      if (this.$refs.videoInput) {
        this.$refs.videoInput.files = dt.files;
      }
    },

    removeVideo() {
      if (this.videoPreviewUrl) {
        URL.revokeObjectURL(this.videoPreviewUrl);
        this.videoPreviewUrl = null;
      }
      this.videoFileName = '';
      this.videoFileSize = '';
      if (this.$refs.videoInput) {
        this.$refs.videoInput.value = '';
      }
    },

    // -------------------------------------------------------------
    // YOUTUBE (16:9 Standard) URL PARSING
    // -------------------------------------------------------------
    extractYt(val) {
      this.ytUrl = (val || '').trim();
      this.ytError = false;
      if (!this.ytUrl) {
        this.ytId = '';
        return;
      }
      // Matches standard, shortened, live, and embed links
      const m = this.ytUrl.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?|live)\/|.*[?&]v=)|youtu\.be\/)([A-Za-z0-9_-]{11})/i);
      if (m && m[1]) {
        this.ytId = m[1];
      } else {
        this.ytId = '';
        this.ytError = true;
      }
    },

    // -------------------------------------------------------------
    // YOUTUBE SHORTS (9:16 Vertical) URL PARSING
    // -------------------------------------------------------------
    extractShorts(val) {
      this.shortsUrl = (val || '').trim();
      this.shortsError = false;
      if (!this.shortsUrl) {
        this.shortsId = '';
        return;
      }
      // Matches /shorts/ or fallback standard ID if user pasted standard link
      const m = this.shortsUrl.match(/(?:youtube\.com\/shorts\/|youtu\.be\/|youtube\.com\/watch\?v=)([A-Za-z0-9_-]{11})/i);
      if (m && m[1]) {
        this.shortsId = m[1];
      } else {
        this.shortsId = '';
        this.shortsError = true;
      }
    },

    // -------------------------------------------------------------
    // INSTAGRAM URL VALIDATION
    // -------------------------------------------------------------
    checkIg(val) {
      this.igUrl = (val || '').trim();
      if (!this.igUrl) {
        this.igValid = false;
        return;
      }
      this.igValid = /(?:instagram\.com\/(?:p|reel|reels)\/([A-Za-z0-9_-]+))/i.test(this.igUrl);
    },

    // -------------------------------------------------------------
    // SUBMIT VALIDATION & FEEDBACK
    // -------------------------------------------------------------
    submitForm(e) {
      if (!this.caption.trim()) {
        alert('Please provide a caption or story for your mountain post.');
        e.preventDefault();
        return;
      }

      if (this.tab === 'photo' && this.photoPreviews.length === 0 && !this.photoUrlInput.trim()) {
        const confirmEmpty = confirm('No photo selected. Would you like to publish with a scenic Himalayan cover?');
        if (!confirmEmpty) {
          e.preventDefault();
          return;
        }
      }

      if (this.tab === 'video' && !this.videoPreviewUrl && !this.videoUrlInput.trim()) {
        alert('Please upload a video file or provide a video link.');
        e.preventDefault();
        return;
      }

      if (this.tab === 'youtube' && !this.ytId) {
        alert('Please enter a valid YouTube video URL.');
        e.preventDefault();
        return;
      }

      if (this.tab === 'youtube_shorts' && !this.shortsId) {
        alert('Please enter a valid YouTube Shorts URL.');
        e.preventDefault();
        return;
      }

      if (this.tab === 'instagram' && !this.igValid) {
        alert('Please paste a valid public Instagram post or reel link.');
        e.preventDefault();
        return;
      }

      this.isSubmitting = true;
    }
  };
}

// Register with Alpine.js
function registerCommunityUploadModal() {
  if (window.Alpine) {
    window.Alpine.data('communityUploadModal', communityUploadModal);
  } else {
    document.addEventListener('alpine:init', () => {
      window.Alpine.data('communityUploadModal', communityUploadModal);
    });
  }
}

registerCommunityUploadModal();
