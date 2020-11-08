<template>
  <div>
    <div class="box">
      <div class="upload-form">
        <b-message type="is-info" class="content">
          Derp
        </b-message>
      </div>
      <b-field>
          <b-upload v-model="dropFiles"
              multiple
              drag-drop>
              <section class="section">
                  <div class="content has-text-centered">
                      <p>
                          <b-icon
                              icon="upload"
                              size="is-large">
                          </b-icon>
                      </p>
                      <p>Drop your files here or click to upload</p>
                  </div>
              </section>
          </b-upload>
        </b-field>

      <div class="has-text-centered">
        <b-button
          type="is-light"
          icon-pack="fas"
          icon-left="search"
          >Analyze</b-button
        >
      </div>
    </div>

  </div>
</template>

<script>
    export default {
        data() {
            return {
                dropFiles: []
            }
        },
        methods: {
            deleteDropFile(index) {
                this.dropFiles.splice(index, 1)
            }
        }
    }
</script>

<style scoped>
.upload-form {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
