<template>
  <div>
    <b-jumbotron id="superevent-banner" class="py-4 pl-3 text-white">
      <b-row>
        <b-col cols="12">
          <b-row>
            <b-col>
              <h3><span>Update {{ safeGetEventAttributes(0, "sequence_number", -1) }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>MassGap {{ safeGetEventAttributesAttribute(0, "prob_massgap") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>NSBH {{ safeGetEventAttributesAttribute(0, "prob_nsbh") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>90%: {{ parseFloat(safeGetEventAttributesAttribute(0, "area_90")).toFixed(2) }}</span>
              </h3>
            </b-col>
            <b-col>
              <h3><span>{{ safeGetEventAttributesAttribute(0, "Instruments", "") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>FAR {{ safeGetEventAttributesAttribute(0, "far") }}</span></h3>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <h3><span>BNS {{ safeGetEventAttributesAttribute(0, "prob_bns") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>Terrestrial {{ safeGetEventAttributesAttribute(0, "prob_terres") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>BBH {{ safeGetEventAttributesAttribute(0, "prob_bbh") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>50%: {{ parseFloat(safeGetEventAttributesAttribute(0, "area_50")).toFixed(2) }}</span>
              </h3>
            </b-col>
            <b-col>
              <h3><span>{{ safeGetEventAttributesAttribute(0, "unknown_field", "") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>NS/Rem {{ safeGetEventAttributesAttribute(0, "prob_ns") }}</span></h3>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-jumbotron>
  </div>
</template>

<script>
export default {
  name: 'GravitationalWaveBanner',
  props: {
    supereventData: {
      type: Object,
      required: true
    }
  },
  methods: {
    safeGetEventAttributes(event_id, field_name, fallback = 0) {
      if ((this.supereventData.event_attributes !== undefined) &&
          (this.supereventData.event_attributes[event_id] !== undefined) &&
          (this.supereventData.event_attributes[event_id][field_name] !== undefined)) {
        return this.supereventData.event_attributes[event_id][field_name];
      }
      return fallback;
    },
    safeGetEventAttributesAttribute(event_id, attribute_name, fallback = 0) {
      if ((this.supereventData.event_attributes !== undefined) &&
          (this.supereventData.event_attributes[event_id] !== undefined) &&
          (this.supereventData.event_attributes[event_id].attributes !== undefined)) {
        return this.supereventData.event_attributes[event_id].attributes[attribute_name];
      }
      return fallback;
    }
  },
}
</script>

<style scoped>
#superevent-banner {
  width: 100%;
  background-color: #06345c;
}

span {
  color: white;
}
</style>
