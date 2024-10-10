<template>
  <div>
    <h2>Upload a Video</h2>
    <input type="file" @change="onFileChange" accept="video/*" />
    <button @click="uploadFile" :disabled="!selectedFile" class="upload-btn">Upload</button>
    <p v-if="uploadMessage">{{ uploadMessage }}</p>

    <!-- Loading Spinner -->
    <div v-if="loading" class="spinner">
      <p>Processing... Please wait.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      uploadMessage: '',
      loading: false,
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        this.loading = true;
        this.uploadMessage = 'Uploading...';

        const response = await axios.post('http://localhost:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.data.message) {
          this.uploadMessage = 'Video uploaded successfully. Processing...';
          const videoData = {
            filename: this.selectedFile.name,
            url: URL.createObjectURL(this.selectedFile),
            emotions: response.data.frame_emotions,
            frames: response.data.frames, // Small previews for each frame
            graphUrl: `http://localhost:5000/graph/${response.data.graph_name}`,
          };
          this.$emit('file-uploaded', videoData);
        } else {
          throw new Error('Failed to process video');
        }
      } catch (error) {
        this.uploadMessage = 'Error uploading file. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
h2 {
  margin-bottom: 20px;
}

button.upload-btn {
  background-color: #d9534f;
}

button.upload-btn:hover {
  background-color: #c9302c;
}

.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.spinner p {
  color: #7c1414;
  font-size: 16px;
}
</style>