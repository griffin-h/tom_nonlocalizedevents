<template>
  <div>
    <b-jumbotron id="superevent-banner" class="py-4 pl-3 text-white superevent-banner">
      <b-row>
        <b-col>
          <h3><span>MassGap: {{ safeGetEventAttributes("prob_massgap", -1, true) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>NSBH: {{ safeGetEventAttributes("prob_nsbh", -1, true) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>Remnant: {{ safeGetEventAttributes("prob_remnant", -1, true) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>90%: {{ parseFloat(safeGetEventAttributes("area_90")).toFixed(2) }}</span>
          </h3>
        </b-col>
        <b-col>
          <h3><span>FAR: {{ safeGetEventAttributes("far", -1, true) }}</span></h3>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <h3><span>BNS: {{ safeGetEventAttributes("prob_bns", -1, true) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>Terrestrial: {{ safeGetEventAttributes("prob_terres", -1, true) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>BBH: {{ safeGetEventAttributes("prob_bbh", -1, true) }}</span></h3>
        </b-col>
        <b-col>
          <h3><span>50%: {{ parseFloat(safeGetEventAttributes("area_50")).toFixed(2) }}</span>
          </h3>
        </b-col>
        <b-col>
          <h3><span>NS/Rem: {{ safeGetEventAttributes("prob_ns", -1, true) }}</span></h3>
        </b-col>
      </b-row>
    </b-jumbotron>
  </div>
</template>

<script>
import '@/assets/css/superevent.css';
export default {
  name: 'GravitationalWaveBanner',
  props: {
    eventAttributes: {
      type: Object,
      required: true
    },
    supereventId: String
  },
  methods: {
    safeGetEventAttributes(field_name, fallback = 0, only_first_part = false) {
      if ((this.eventAttributes !== undefined) &&
         (this.eventAttributes[field_name] !== undefined)) {
          if (only_first_part && typeof this.eventAttributes[field_name] === 'string'){
            return this.eventAttributes[field_name].split(' ')[0];
          }
          else{
            return this.eventAttributes[field_name];
          }
      }
      return fallback;
    }
  },
}
</script>
