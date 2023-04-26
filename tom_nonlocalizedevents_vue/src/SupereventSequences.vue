<template>
  <div class="row superevent-top-level-details">
    <div class="col-md-12">
      <b-card no-body>
        <b-card-title class="text-center font-weight-bold superevent-banner" style="font-size:xxx-large;">{{ superevent_data.event_id }}</b-card-title>
        <b-tabs card pills active-nav-item-class="font-weight-bold">
          <b-tab no-body v-for="(sequence, index) in expandedSequences" :key="sequence.sequence_id" @click="tab = sequence.sequence_id" :title="getTabTitle(sequence)" :active="(index+1) == expandedSequences.length" lazy>
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
  computed: {
    expandedSequences() {
      let sequences = [];
      this.superevent_data.sequences.forEach((sequence) => {
        // Remove the external coincidence for the initial sequence
        let cloneSeq = _.cloneDeep(sequence);
        cloneSeq.external_coincidence = null;
        sequences.push(cloneSeq);
        // If the external coincidence is present, add the sequence again with external coincidence
        if (!_.isNil(sequence.external_coincidence) && !_.isEmpty(sequence.external_coincidence)) {
          sequences.push(sequence);
        }
      });
      return sequences;
    }
  },
  methods: {
    getTabTitle(sequence) {
      let seqTitle = '';
      seqTitle += sequence.sequence_id.toString() + ': ' + _.capitalize(sequence.event_subtype);
      if (!_.isNil(sequence.external_coincidence) && !_.isEmpty(sequence.external_coincidence)) {
        seqTitle += ' Combined';
      }
      return seqTitle;
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
