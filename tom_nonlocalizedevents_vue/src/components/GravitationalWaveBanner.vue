<template>
  <div>
    <b-jumbotron id="superevent-banner" class="py-4 pl-3 text-white superevent-banner">
      <b-row>
        <b-col>
          <h3 v-if="sequence.ingestor_source.toLowerCase() === 'gcn'"><span>NS: {{ safeGetEventAttributes("details.prob_ns", -1, true).toPrecision(3) }}</span></h3>
          <h3 v-else><span>Instruments: {{ safeGetEventAttributes("details.instruments", []).join(',') }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>NSBH: {{ safeGetEventAttributes(this.nsbhPath, -1, true).toPrecision(3) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>FAR: {{ safeGetEventAttributes("details.far", -1, true).toPrecision(3) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>90%: {{ parseFloat(safeGetEventAttributes("localization.area_90")).toPrecision(4) }}</span>
          </h3>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <h3><span>BNS: {{ safeGetEventAttributes(this.bnsPath, -1, true).toPrecision(3) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>Terrestrial: {{ safeGetEventAttributes(this.terrestrialPath, -1, true).toPrecision(3) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>BBH: {{ safeGetEventAttributes(this.bbhPath, -1, true).toPrecision(3) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>50%: {{ parseFloat(safeGetEventAttributes("localization.area_50")).toPrecision(4) }}</span>
          </h3>
        </b-col>
      </b-row>
    </b-jumbotron>
  </div>
</template>

<script>
import _ from 'lodash';
import '@/assets/css/superevent.css';
export default {
  name: 'GravitationalWaveBanner',
  props: {
    sequence: {
      type: Object,
      required: true
    },
    supereventId: String
  },
  computed: {
    nsbhPath() {
      if (this.sequence.ingestor_source.toLowerCase() === 'gcn') {
        return "details.prob_nsbh";
      }
      else {
        return "details.classification.NSBH";
      }
    },
    bbhPath() {
      if (this.sequence.ingestor_source.toLowerCase() === 'gcn') {
        return "details.prob_bbh";
      }
      else {
        return "details.classification.BBH";
      }
    },
    bnsPath() {
      if (this.sequence.ingestor_source.toLowerCase() === 'gcn') {
        return "details.prob_bns";
      }
      else {
        return "details.classification.BNS";
      }
    },
    terrestrialPath() {
      if (this.sequence.ingestor_source.toLowerCase() === 'gcn') {
        return "details.prob_terres";
      }
      else {
        return "details.classification.Terrestrial";
      }
    }
  },
  methods: {
    safeGetEventAttributes(field_path, fallback = 0, only_first_part = false) {
      if (_.isObjectLike(this.sequence)) {
        var field = _.get(this.sequence, field_path, fallback);
        if (only_first_part && typeof field === 'string') {
          field = field.split(' ')[0];
        }
        if (!isNaN(parseFloat(field))){
            return parseFloat(field);
          }
            return field;
      }
      return fallback;
    }
  },
}
</script>
