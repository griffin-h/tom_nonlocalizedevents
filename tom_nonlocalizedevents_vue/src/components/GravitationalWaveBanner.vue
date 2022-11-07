<template>
  <div>
    <b-jumbotron id="superevent-banner" class="py-4 pl-3 text-white">
      <b-row>
        <b-col cols="2">
          <h1><span id="superevent_name">{{ supereventId }}</span></h1>
        </b-col>
        <b-col cols="10">
          <b-row>
            <b-col>
              <h3><span>Update {{ safeGetEventAttributes("sequence_number", -1) }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>MassGap {{ safeGetEventAttributesAttribute("prob_massgap") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>NSBH {{ safeGetEventAttributesAttribute("prob_nsbh") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>90%: {{ parseFloat(safeGetEventAttributesAttribute("area_90")).toFixed(2) }}</span>
              </h3>
            </b-col>
            <b-col>
              <h3><span>{{ safeGetEventAttributesAttribute("Instruments", "") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>FAR {{ safeGetEventAttributesAttribute("far") }}</span></h3>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <h3><span>BNS {{ safeGetEventAttributesAttribute("prob_bns") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>Terrestrial {{ safeGetEventAttributesAttribute("prob_terres") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>BBH {{ safeGetEventAttributesAttribute("prob_bbh") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>50%: {{ parseFloat(safeGetEventAttributesAttribute("area_50")).toFixed(2) }}</span>
              </h3>
            </b-col>
            <b-col>
              <h3><span>{{ safeGetEventAttributesAttribute("unknown_field", "") }}</span></h3>
            </b-col>
            <b-col>
              <h3><span>NS/Rem {{ safeGetEventAttributesAttribute("prob_ns") }}</span></h3>
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
    eventAttributes: {
      type: Object,
      required: true
    },
    supereventId: String
  },
  methods: {
    safeGetEventAttributes(field_name, fallback = 0) {
      if ((this.eventAttributes !== undefined) &&
         (this.eventAttributes[field_name] !== undefined)) {
        return this.eventAttributes[field_name];
      }
      return fallback;
    },
    safeGetEventAttributesAttribute(attribute_name, fallback = 0) {
      if ((this.eventAttributes !== undefined) &&
          (this.eventAttributes.attributes !== undefined)) {
        return this.eventAttributes.attributes[attribute_name];
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
