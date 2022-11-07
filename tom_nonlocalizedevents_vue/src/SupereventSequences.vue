<template>
  <div class="row superevent-top-level-details">
    <div class="col-md-12">
      <b-card no-body>
        <b-card-title class="text-center font-weight-bold text-info">{{ event_id }}</b-card-title>
        <b-tabs card active-nav-item-class="font-weight-bold text-info">
          <b-tab v-for="(sequence, index) in unpacked_sequences" :key="sequence.sequence_id" @click="tab = sequence.sequence_id" :title="getTabTitle(sequence.sequence_id, sequence.created)" :active="(index+1) == unpacked_sequences.length" lazy>
            <superevent-detail
              :ref="'sequence_' + sequence.sequence_id.toString()"
              :supereventPk="superevent_pk"
              :supereventId="event_id"
              :sequenceId="sequence.sequence_id"
            />
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import SupereventDetail from '@/SupereventDetail.vue';

export default {
  name: "SupereventSequences",
  props: {
    pk: String,
    event_id: String,
    sequences: String,
    skip_api_url: String,
    tom_api_url: String,
  },
  data: function () {
    return {
      unpacked_sequences: JSON.parse(this.sequences),
      superevent_pk: parseInt(this.pk),
    };
  },
  components: {
    SupereventDetail,
  },
  created() {
    this.$store.commit('setTomApiBaseUrl', this.tom_api_url);
    this.$store.commit('setSkipApiBaseUrl', this.skip_api_url);
    console.log("created SupereventSequences.vue");
  },
  methods: {
    getTabTitle(sequence_id, creation_date) {
      let date = new Date(creation_date);
      return 'Update ' + sequence_id.toString() + ': ' + date.toLocaleString();
    }
  },
};
</script>
