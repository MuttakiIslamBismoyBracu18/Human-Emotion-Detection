<template>
  <div class="container">
    <h1>Emotion Detection from Video</h1>

    <!-- File Upload Section -->
    <div class="upload-section">
      <h3>Upload a Video</h3>
      <input type="file" @change="onFileChange" ref="fileInput" />
      <button @click="uploadFile" class="btn upload-btn">Upload</button>
      <p v-if="message">{{ message }}</p>
    </div>

    <!-- Uploaded Videos Section -->
    <div v-if="uploadedVideo" class="video-section">
      <h3>Uploaded Videos</h3>
      <video :src="uploadedVideo" controls class="small-video"></video>

      <!-- Frame-wise Emotions Section -->
      <h4>Frame-wise Emotions</h4>
      <div class="frames-row">
        <div v-for="(frame, index) in frames" :key="index" class="frame-item">
          <img :src="frame" class="frame-img" />
          <p>{{ frameEmotions[index] }}</p>
        </div>
      </div>

      <!-- Emotion Graph Section -->
      <h4>Emotion Graph</h4>
      <img :src="graph" alt="Emotion Graph" class="emotion-graph" />
      <a :href="graph" download class="btn download-btn">Download Graph</a>
    </div>

    <!-- Loading Popup Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-popup">
        <!-- Corrected path for spinner GIF using require -->
        <img :src="require('@/assets/spinner.gif')" alt="Loading..." />
        <p>Processing... Please wait.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "",
      uploadedVideo: null,
      frames: [],
      frameEmotions: [],
      graph: "",
      loading: false,
    };
  },
  methods: {
    onFileChange(event) {
      this.uploadedVideo = URL.createObjectURL(event.target.files[0]);
    },
    async uploadFile() {
      const file = this.$refs.fileInput.files[0];
      if (!file) {
        this.message = "Please choose a file first!";
        return;
      }

      this.loading = true;
      this.message = "Video uploaded successfully. Processing...";

      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        this.frames = data.frames;
        this.frameEmotions = data.frame_emotions;
        this.graph = `http://127.0.0.1:5000/graph/${data.graph_name}`;
        this.message = "Video processing completed!";
      } catch (error) {
        console.error(error);
        this.message = "Error uploading file. Please try again.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  text-align: center;
  background-color: #ffe6e6; /* Light red background */
  padding: 20px;
}

h1 {
  color: #b33939; /* Dark red for title */
}

.upload-section {
  margin-bottom: 20px;
}

input[type="file"] {
  background-color: #b33939; /* Matching upload button color */
  color: white;
  padding: 8px;
  border-radius: 5px;
  border: none;
}

.btn {
  background-color: #b33939; /* Red button */
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.btn:hover {
  background-color: #ff5e57; /* Lighter red on hover */
}

.small-video {
  width: 400px; /* Reduce video preview size */
  height: auto;
  margin-bottom: 20px;
}

.frames-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.frame-item {
  margin: 10px;
  text-align: center;
}

.frame-img {
  width: 100px;
  height: auto;
}

.emotion-graph {
  margin-top: 20px;
  max-width: 100%;
  height: auto;
}

.download-btn {
  display: block;
  margin: 20px auto;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-popup {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.loading-popup img {
  width: 50px;
  height: 50px;
}
</style>
