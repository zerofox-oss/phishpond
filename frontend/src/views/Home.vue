<template>
  <div id="analysis">
    <div class="box">
      <div class="upload-form">
        <b-message type="is-info" class="content">
          Add a kit here to analyze
        </b-message>
      </div>
      <!-- Lots of inspiration here from ninoseki's excellent eml_analyzer code -->
      <b-field>
        <b-upload v-model="phishKitFile" expanded drag-drop>
          <section class="section">
            <div class="content has-text-centered">
              <p>
                <b-icon icon="upload" size="is-large"> </b-icon>
              </p>
              <code>
                <p>Drop the phishkit as a .zip here or click to upload</p>
              </code>
            </div>
          </section>
        </b-upload>
      </b-field>
      <div class="has-text-centered" v-if="phishKitFile">
        <b-button type="is-light" icon-pack="fas" icon-left="file-archive">
          {{ phishKitFile.name || "No Zip Found!" }}
        </b-button>
      </div>

      <div class="has-text-centered">
        <br /><br />
        <b-button
          type="is-light"
          icon-pack="fas"
          icon-left="search"
          @click="analyze"
          >Analyze</b-button
        >
      </div>
    </div>
    <div class="box" v-if="this.didAnalysis">
      <h1 class="title">{{ "Phish Kit Analysis: " + phishKitFile.name }}</h1>
      <div class="tile is-ancestor">
        <div class="tile is-6">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <figure class="image is-48x48">
                    <b-icon icon="hashtag" />
                  </figure>
                </div>
                <div class="media-content">
                  <p class="title is-4">Zip File Hashes</p>
                </div>
              </div>
              <div class="content">
                <li
                  v-for="(value, key) in this.analysis.hashes"
                  v-bind:key="key"
                >
                  <b>{{ key }}</b
                  >: {{ value }}
                </li>
                <br />
              </div>
            </div>
          </div>
        </div>
        <div class="tile is-6">
          <div class="card">
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <figure class="image is-48x48">
                    <b-icon icon="info-circle" />
                  </figure>
                </div>
                <div class="media-content">
                  <p class="title is-4">Metadata</p>
                </div>
              </div>
              <div class="content">
                <div class="columns is-mobile is-multiline is-centered">
                  <div class="column is-narrow">
                    <div>
                      <p class="heading">Embedded URLs Found</p>
                      <p class="title">
                        {{ this.analysis.strings.urls.length }}
                      </p>
                    </div>
                  </div>
                  <div class="column is-narrow">
                    <div>
                      <p class="heading">Embedded Emails found</p>
                      <p class="title">
                        {{ this.analysis.strings.emails.length }}
                      </p>
                    </div>
                  </div>
                  <div class="column is-narrow">
                    <div>
                      <p class="heading">Size of Zip file</p>
                      <p class="title">
                        {{
                          Math.floor(
                            (this.analysis.file_size / Math.pow(1024, 2)) * 100
                          ) / 100
                        }}
                        MB
                      </p>
                    </div>
                  </div>
                  <div class="column is-narrow">
                    <div>
                      <p class="heading">Total Files in Kit</p>
                      <p class="title">
                        {{ this.analysis.strings.total_files }}
                      </p>
                    </div>
                  </div>
                </div>
                <br />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="tile">
        <div class="tile is-child card">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <b-icon icon="file-code" />
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-4">File Tree</p>
              </div>
              <br />
            </div>
          </div>
          <div class="content">
            <highlightjs
              language="shell"
              :code="this.analysis.strings.tree"
            >
            </highlightjs>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import hljs from 'highlight.js'
export default {
  data() {
    return {
      phishKitFile: {},
      analysis: {},
      didAnalysis: false,
    };
  },
  mounted() {
    hljs.initHighlightingOnLoad();
  },
  methods: {
    analyze() {
      if (!this.phishKitFile.name) {
        this.$buefy.toast.open({
          duration: 5000,
          message: `No file selected! Please try again`,
          position: "is-bottom",
          type: "is-danger",
        });

        return;
      }
      if (this.phishKitFile.type !== "application/zip") {
        this.$buefy.toast.open({
          duration: 5000,
          message: `Submit .zip files only! Please try again`,
          position: "is-bottom",
          type: "is-danger",
        });
        return;
      }
      const loadingComponent = this.$buefy.loading.open({
        container: this.$el.firstElementChild,
      });
      var data = new FormData();
      data.append("file", this.phishKitFile);
      api
        .post("/analyze", data)
        .catch((error) => {
          loadingComponent.close();
          this.$buefy.toast.open({
            duration: 5000,
            message: `Error from API: ${error}`,
            position: "is-bottom",
            type: "is-danger",
          });
        })
        .then((response) => {
          this.$buefy.toast.open({
            duration: 5000,
            message: `Successfully analyzed rule ${this.phishKitFile.name}!`,
            position: "is-bottom",
            type: "is-success",
          });
          this.analysis = response.data;
          this.didAnalysis = true;
          console.log(this.analysis);
          loadingComponent.close();
        });
    },
  },
};
</script>

<style scoped>
.upload-form {
  margin-top: 20px;
  margin-bottom: 20px;
}
li {
  text-align: left;
}
pre {
  text-align: left;
  white-space: pre;
}
</style>
