<template>
  <div>
    <div>
      <b-alert v-for="message in messages" :key="message" show dismissable>
        {{ message }}
      </b-alert>
    </div>
    <div v-show="sequence !== undefined">
      <gravitational-wave-banner :sequence="sequence" :supereventId="supereventId" />
    </div>
    <b-row style="margin-top: 6px;">
      <b-col cols="8">
        <alerts-table
          :alerts="alerts"
          @selected-alert="onSelectAlert"
        ></alerts-table>
      </b-col>
      <b-col cols="4">
        <h3>GraceDB BAYESTAR Images</h3>
        <b-row>
          <b-img-lazy
            :src="getVolumeImageUrl(volume_image=true)"
            fluid
          ></b-img-lazy>
        </b-row>
        <b-row>
          <b-img-lazy
            :src="getVolumeImageUrl(volume_image=false)"
            fluid
          ></b-img-lazy>
        </b-row>
      </b-col>
    </b-row>
    <b-row class="my-3">
      <b-col class="col-md-auto">
        <add-candidate-modal
          :supereventPk="this.supereventPk"
          :existingEventCandidates="this.eventCandidates"
          @created-candidates="onCreatedCandidates"
        />
      </b-col>
      <b-col class="col-md-auto">
        <create-target-modal
          :alerts="this.selectedAlerts"
          :supereventPk="this.supereventPk"
          @created-target-candidates="onCreatedCandidates"
        />
      </b-col>
    </b-row>
    <hr />
    <b-row>
      <b-col cols="12">
        <h3>Active Candidates</h3>
        <candidate-target-table
          :candidates="this.viableCandidates"
          :sequenceId="this.sequence.sequence_id"
          @toggle-viability="onToggleViability"
          @change-priority="onChangePriority"
        />
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <h3>Retired Candidates</h3>
        <candidate-target-table
          :candidates="this.nonViableCandidates"
          :sequenceId="this.sequence.sequence_id"
          @toggle-viability="onToggleViability"
          @change-priority="onChangePriority"
        />
      </b-col>
    </b-row>
    <hr />
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";
import '@/assets/css/superevent.css';
import {
  AddCandidateModal,
  AlertsTable,
  CreateTargetModal,
  GravitationalWaveBanner,
  CandidateTargetTable,
} from "@/components";

export default {
  name: "SupereventDetail",
  props: {
    supereventPk: Number,
    supereventId: String,
    sequence: {
      type: Object,
      required: true
    },
    alerts: {
      type: Array,
      required: true
    },
    candidates: {
      type: Array,
      required: true
    }
  },
  components: {
    AddCandidateModal,
    AlertsTable,
    CreateTargetModal,
    CandidateTargetTable,
    GravitationalWaveBanner,
  },
  data: function () {
    return {
      alert_fields: [
        { key: "identifier" },
        { key: "timestamp", sortable: true },
        { key: "from" },
        { key: "subject" },
      ],
      messages: [],
      eventCandidates: [],
      selectedAlerts: [],
      superevent_data: {},
    };
  },
  computed: {
    hasExternalCoincidence() {
      return !_.isNil(this.sequence.external_coincidence) && !_.isEmpty(this.sequence.external_coincidence);
    },
    skymapVersion() {
      if (this.hasExternalCoincidence){
        return _.get(this.sequence, 'external_coincidence.localization.skymap_version', undefined);
      }
      else{
        return _.get(this.sequence, 'localization.skymap_version', undefined);
      }
    },
    skymapUrl() {
      if (this.hasExternalCoincidence){
        return _.get(this.sequence, 'external_coincidence.localization.skymap_url', undefined);
      }
      else{
        return _.get(this.sequence, 'localization.skymap_url', undefined);
      }
    },
    viableCandidates() {
      return this.eventCandidates.filter((item) => {
        return item.viable;
      });
    },
    nonViableCandidates() {
      return this.eventCandidates.filter((item) => {
        return !item.viable;
      });
    },
  },
  created() {
    this.processEventCandidates();
  },

  methods: {
    processEventCandidates() {
      this.eventCandidates = [];
      this.candidates.forEach((candidate) => {
        if(this.sequence.sequence_id.toString() in candidate['credible_regions']) {
          candidate['credible_region'] = candidate['credible_regions'][this.sequence.sequence_id.toString()];
        }
        else {
          candidate['credible_region'] = 100;
        }
        this.eventCandidates.push(candidate);
      });
    },
    getSupereventData() {
      // set this.eventCandidates
      let oldEventCandidates = this.eventCandidates.slice();
      this.eventCandidates = [];
      // retrieve the superevent data from the REST API
      axios
        .get(
          `${this.$store.state.tomApiBaseUrl}/api/nonlocalizedevents/${this.supereventPk}/`
        )
        .then((response) => {
          response["data"]["candidates"].forEach((event_candidate) => {
            if(this.sequence.sequence_id.toString() in event_candidate['credible_regions']) {
              event_candidate['credible_region'] = event_candidate['credible_regions'][this.sequence.sequence_id.toString()];
            }
            else {
              event_candidate['credible_region'] = 100;
            }
            this.eventCandidates.push(event_candidate);
          });
        })
        .catch((error) => {
          console.log(
            `getSupereventData: Error getting database data for pk ${this.supereventPk}: ${error}`
          );
          this.eventCandidates = oldEventCandidates;
        });
    },
    getVolumeImageUrl(volume_image=true) {
      // Construct URL with the superevent id and base skymap fits moc url
      // These files could eithe be a bayestar or LALInference file
      // for example: https://gracedb.ligo.org/api/superevents/S190426c/files/bayestar.volume.png"
      let image_base = '';
      if (volume_image) {
        image_base = 'bayestar.volume.png';
      }
      else {
        if (this.hasExternalCoincidence) {
          image_base = 'combined-ext.png';
        }
        else {
          image_base = 'bayestar.png';
        }
      }
      let url = 'https://gracedb.ligo.org/api/superevents/' + this.supereventId + '/files/' + image_base;
      if (this.skymapVersion !== undefined) {
        url = url + ',' + this.skymapVersion;
      }
      return url;
    },
    onCreatedCandidates(count) {
      this.messages.push(`Successfully added ${count} candidates.`);
      this.getSupereventData();
    },
    onSelectAlert(row, event) {
      // TODO: move to a utils.js
      if (event === true) {
        // add target to list
        if (!_.includes(this.selectedAlerts, row.item))
          this.selectedAlerts.push(row.item);
      } else {
        // remove target from list
        this.selectedAlerts = this.selectedAlerts.filter(function (value) {
          return value !== row.item;
        });
      }
    },
    onToggleViability(row, _event) {
      const event_candidate = row.item;  // it's table of event_candidates, so row.items are event_candidates
      const url = `${this.$store.state.tomApiBaseUrl}/api/eventcandidates/${event_candidate.id}/`;
      const new_viablility = !event_candidate.viable;
      const patch = { viable: new_viablility, viability_reason: event_candidate.viability_reason };  // construct the payload for the PATCH request

      axios  // make the PATCH request
        .patch(url, patch) // patch only serializes/validates/updates the fields in the Request Body
        .then((response) => {
          // if successful, update the front-end value with (new) data from the PATCH response
          row.item.viable = response['data'].viable; 
        })
        .catch((error) => {
          console.error('onToggleViability - url: ' + url);
          console.error('onToggleViability - patch: ' + JSON.stringify(patch));
          console.error(
            `onToggleViability: Error getting database data for ${JSON.stringify(event_candidate)}: ${error}`
          );
        });
    },
    onChangePriority(row, event) {
        //
        // TODO: at the moment, this isn't working. The b-table sorting seems to be interfering with
        // the v-model binding to the row.item.priority field, and maybe more problems with v-model binding
        // to the proper data.
        //
        const candidate = row.item;  // it's table of event_candidates, so row.items are event_candidates
        const url = `${this.$store.state.tomApiBaseUrl}/api/eventcandidates/${candidate.id}`;
        const new_priority = event;  // event is an integer for b-form-spinbutton
        const patch = { priority: new_priority };  // construct the payload for the PATCH request

        console.log('onChangePriority -        row.item.id: ' + row.item.id);
        console.log('onChangePriority -  row.item.priority: ' + row.item.priority);
        console.log('onChangePriority - candidate.priority: ' + candidate.priority);
        console.log('onChangePriority -              event: ' + event);

        axios  // make the PATCH request
            .patch(url, patch) // patch only serializes/validates/updates the fields in the Request Body
            .then((_response) => {
                // if successful, update the front-end value with (new) data from the PATCH response
                //row.item.priority = response['data'].priority; 
            })
            .catch((error) => {
                console.error('onChangePriority - url: ' + url);
                console.error('onChangePriority - patch: ' + JSON.stringify(patch));
                console.error(
                    `onChangePriority: Error getting database data for ${JSON.stringify(candidate)}: ${error}`
                );
            });
        console.log('after PATCH...');
        console.log('onChangePriority - candidate.priority: ' + candidate.priority);
        console.log('onChangePriority -              event: ' + event);
        console.log();
    },
  },
};
</script>

<style scoped>
</style>
