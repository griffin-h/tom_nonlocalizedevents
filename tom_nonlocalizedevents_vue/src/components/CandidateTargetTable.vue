<template>
    <b-container>
        <b-table
            striped
            primary-key="id"
            sort-by="credible_region"
            :fields="candidateFields"
            :items="candidates">
            <!-- see https://bootstrap-vue.org/docs/components/table#custom-data-rendering -->

            <!-- Set up the link to the TargetDetail page for this Candidates Target -->
            <template #cell(target-link)="row">
                <b-link :href="getTargetDetailUrl(row.item.target)">{{ row.item.target.name }}</b-link>
            </template>

            <!-- Set up the Activate/Retire Button -->
            <template #cell(active)="row">
                <b-button size="sm" @click="$bvModal.show(getId('viable-modal-', row, ''))">
                    {{ row.item.viable ? 'Retire' : 'Activate'}}
                </b-button>
                <b-modal :id="getId('viable-modal-', row, '')" :title="modalTitle(row)" @ok="$emit('toggle-viability', row, $event)">
                    <b-container fluid>
                        <b-row>
                            <b-col sm="2">
                                <label :for="getId('textarea-', row, '')">Viability Reason:</label>
                            </b-col>
                            <b-col sm="10">
                                <b-form-textarea
                                    :id="getId('textarea-', row, '')"
                                    v-model="row.item.viability_reason"
                                    placeholder="Enter reason for viability decision here"
                                    rows="2"
                                    max-rows="4"
                                ></b-form-textarea>
                            </b-col>
                        </b-row>
                    </b-container>
                </b-modal>
            </template>

            <!-- Set up Priority (NOT IMPLEMENTED AT THE MOMENT)
            <template #cell(priority)="row">
                <b-form-spinbutton
                    inline
                    size="sm"
                    v-model="row.item.priority"
                @change="$emit('change-priority', row, $event)" />
            </template>
            -->

        </b-table>
    </b-container>
</template>

<script>
export default {
    name: 'CandidateTargetTable',
    components: {},
    props: {
      candidates: {
        type: Array,
        required: true
      },
      sequenceId: Number
    },
    computed: {
    },
    data() {
        return {
            candidateFields: [
                //{ 'key': 'priority', 'label': 'Priority', 'sortable': true },
                { 'key': 'target-link', 'label': 'Candidate', 'sortable': true },
                { 'key': 'target.ra', 'label': 'RA', formatter: (value, key, item) => value.toLocaleString() },
                { 'key': 'target.dec', 'label': 'DEC', formatter: (value, key, item) => value.toLocaleString() },
                { 'key': 'credible_region', 'label': 'CR %', 'sortable': true },
                { 'key': 'active' },
                { 'key': 'viability_reason', 'label': "Viability Reason" },
            ],
        }
    },
    methods: {
        getTargetDetailUrl(target) {
            // get the base url from the vuex store and append to it
            return `${this.$store.state.tomApiBaseUrl}/targets/${target.id}`;
        },
        modalTitle(row) {
            return (row.item.viable ? 'Retire' : 'Activate') + ' Candidate';
        },
        getId(text_before, row, text_after) {
            return text_before + row.item.id.toString() + text_after;
        }
    }
}
</script>
