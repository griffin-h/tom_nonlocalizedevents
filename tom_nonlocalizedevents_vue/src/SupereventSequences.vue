<template>
  <div class="row superevent-top-level-details">
    <div class="col-md-12">
      <b-card no-body>
        <b-card-title class="text-center font-weight-bold superevent-banner" style="font-size:xxx-large;">{{ event_id }}</b-card-title>
        <b-tabs card pills active-nav-item-class="font-weight-bold">
          <b-tab no-body v-for="(sequence, index) in unpacked_sequences" :key="sequence.sequence_id" @click="tab = sequence.sequence_id" :title="getTabTitle(sequence.sequence_id, sequence.created)" :active="(index+1) == unpacked_sequences.length" lazy>
            <superevent-detail
              :ref="'sequence_' + sequence.sequence_id.toString()"
              :supereventPk="superevent_pk"
              :supereventId="event_id"
              :supereventHermesData="superevent_data"
              :sequenceId="sequence.sequence_id"
            />
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SupereventDetail from '@/SupereventDetail.vue';
import '@/assets/css/superevent.css';

export default {
  name: "SupereventSequences",
  props: {
    pk: String,
    event_id: String,
    sequences: String,
    hermes_api_url: String,
    tom_api_url: String,
  },
  data: function () {
    return {
      unpacked_sequences: JSON.parse(this.sequences),
      superevent_pk: parseInt(this.pk),
      superevent_data: {},
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
          `${this.$store.state.hermesApiBaseUrl}/api/v0/nonlocalizedevents/${this.event_id}/`,
          this.$store.state.hermesAxiosConfig
        )
        .then((response) => {
          this.superevent_data = response["data"];
        })
        .catch((error) => {
          console.log(
            `Error getting details for superevent ${this.event_id}: ${error}`
          );
        });
    },
  },
};
</script>
