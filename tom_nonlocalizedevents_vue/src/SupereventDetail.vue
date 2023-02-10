<template>
  <div>
    <div>
      <b-alert v-for="message in messages" :key="message" show dismissable>
        {{ message }}
      </b-alert>
    </div>
    <div v-show="supereventHermesData.sequences !== undefined">
      <gravitational-wave-banner :eventAttributes="superevent_attributes" :supereventId="supereventId" />
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
          :sequenceId="this.sequenceId"
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
          :sequenceId="this.sequenceId"
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
    sequenceId: Number,
    supereventHermesData: {
      type: Object,
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
      alerts: [],
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
      superevent_attributes: {},
      sequence_skymap_fits_url: '',
    };
  },
  computed: {
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
    this.getSupereventData();
    this.setupSupereventHermesData();
  },
  watch: {
    supereventHermesData: function() {
      this.setupSupereventHermesData();
    }
  },
  methods: {
    getSupereventData() {
      // set this.eventCandidates
      let oldEventCandidates = this.eventCandidates.slice();
      this.eventCandidates = [];
      // retrieve the superevent data from the REST API
      axios
        .get(
          `${this.$store.state.tomApiBaseUrl}/api/nonlocalizedevents/${this.supereventPk}`
        )
        .then((response) => {
          response["data"]["candidates"].forEach((event_candidate) => {
            if(this.sequenceId.toString() in event_candidate['credible_regions']) {
              event_candidate['credible_region'] = event_candidate['credible_regions'][this.sequenceId.toString()];
            }
            else {
              event_candidate['credible_region'] = 100;
            }
            this.eventCandidates.push(event_candidate);
          });
          for (let sequence_index in response["data"]["sequences"]) {
            if (response["data"]["sequences"][sequence_index]["sequence_id"] == this.sequenceId) {
              this.sequence_skymap_fits_url = response["data"]["sequences"][sequence_index]["skymap_fits_url"];
            }
          }
        })
        .catch((error) => {
          console.log(
            `getSupereventData: Error getting database data for pk ${this.supereventPk}: ${error}`
          );
          this.eventCandidates = oldEventCandidates;
        });
    },
    setupSupereventHermesData() {
      if (this.supereventHermesData.sequences !== undefined && this.supereventHermesData.sequences.length > 0) {
        for (const sequence_index in this.supereventHermesData.sequences) {
          if (this.supereventHermesData.sequences[sequence_index]['sequence_number'] == this.sequenceId) {
            this.superevent_attributes = this.supereventHermesData.sequences[sequence_index].message.data;
            break;
          }
        }
        this.alerts = this.supereventHermesData.references;
      }
    },
    getVolumeImageUrl(volume_image=true) {
      // Construct URL with the superevent id and base skymap fits moc url
      // These files could eithe be a bayestar or LALInference file
      // for example: https://gracedb.ligo.org/api/superevents/S190426c/files/bayestar.volume.png"
      let image_base = '.png';
      if (volume_image) {
        image_base = '.volume.png';
      }
      let url = this.sequence_skymap_fits_url.replace('LALInference.multiorder.fits', 'LALInference' + image_base);
      url = url.replace('bayestar.multiorder.fits', 'bayestar' + image_base);
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
    onToggleViability(row, event) {
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
            .then((response) => {
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
