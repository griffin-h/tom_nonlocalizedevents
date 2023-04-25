<template>
  <div class="row superevent-top-level-details">
    <div class="col-md-12">
      <b-card no-body>
        <b-card-title class="text-center font-weight-bold superevent-banner" style="font-size:xxx-large;">{{ superevent_data.event_id }}</b-card-title>
        <b-tabs card pills active-nav-item-class="font-weight-bold">
          <b-tab no-body v-for="(sequence, index) in superevent_data.sequences" :key="sequence.sequence_id" @click="tab = sequence.sequence_id" :title="getTabTitle(sequence.sequence_id, sequence.created)" :active="(index+1) == superevent_data.sequences.length" lazy>
            <superevent-detail
              :ref="'sequence_' + sequence.sequence_id.toString()"
              :supereventPk="superevent_data.id"
              :supereventId="superevent_data.event_id"
              :sequence="sequence"
              :candidates="superevent_data.candidates"
              :alerts="references"
            />
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import SupereventDetail from '@/SupereventDetail.vue';
import '@/assets/css/superevent.css';

export default {
  name: "SupereventSequences",
  props: {
    superevent: String,
    hermes_api_url: String,
    tom_api_url: String,
  },
  data: function () {
    return {
      superevent_data: JSON.parse(this.superevent),
      references: []
    };
  },
  components: {
    SupereventDetail,
  },
  created() {
    this.$store.commit('setTomApiBaseUrl', this.tom_api_url);
    this.$store.commit('setHermesApiBaseUrl', this.hermes_api_url);
    this.getHermesDBData();
  },
  methods: {
    getTabTitle(sequence_id, creation_date) {
      let date = new Date(creation_date);
      return 'Update ' + sequence_id.toString() + ': ' + date.toLocaleString();
    },
    getHermesDBData() {
      // set this.superevent_data
      axios
        .get(
          `${this.$store.state.hermesApiBaseUrl}/api/v0/nonlocalizedevents/${this.superevent_data.event_id}/`,
          this.$store.state.hermesAxiosConfig
        )
        .then((response) => {
          this.references = _.get(response["data"], 'references', []);
        })
        .catch((error) => {
          console.log(
            `Error getting references for superevent ${this.superevent_data.event_id}: ${error}`
          );
        });
    },
  },
};
</script>
