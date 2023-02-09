<template>
    <div>
        <b-button class="float-left" v-b-modal.candidate-from-target-modal variant="outline-primary" :disabled="modalAlerts.length === 0">Add Candidates from Alerts</b-button>
        <b-modal id="candidate-from-target-modal" size="xl" title="Create Candidate(s) from Alerts">
            <b-container>
                <div class="my-2">
                    <span>Targets to be created:</span>
                </div>
                <ttk-target-table :selectable="false" :targets="this.modalAlerts" />
                <hr />
                <b-form @submit="onCandidateFromAlert">
                    <b-form-group label="Choose groups for new targets:">
                        <b-form-checkbox-group>
                            <b-form-checkbox v-for="group in userGroups" :key="group.name" :value="group.id" @change="onSelectGroup">
                                {{ group.name }}
                            </b-form-checkbox>
                        </b-form-checkbox-group>
                    </b-form-group>
                </b-form>
            </b-container>
            <template #modal-footer="{ cancel }">
                <span v-if="submissionError" class="float-left text-danger">{{ JSON.stringify(submissionError) }}</span>
                <b-button class="float-right" @click="onCandidateFromAlert" variant="primary">Add Candidates</b-button>
                <b-button class="float-right" @click="cancel()">Cancel</b-button>
            </template>
        </b-modal>
    </div>
</template>

<script>
    import _ from 'lodash';
    import axios from 'axios';

    export default {
        props: {
            alerts: {
                type: Array,
                required: false
            },
            supereventPk: {
                type: Number,
                required: true
            }
        },
        data() {
            return {
                selectedGroups: [],
                userGroups: [],
                modalAlerts: this.alerts,
                submissionError: null
            }
        },
        created() {
            this.$root.$on('bv::modal::show', (bvEvent, modalId) => {
                // map alert properties to TargetTable properties in order to display them
                this.submissionError = null;
                this.modalAlerts = this.alerts;
                this.modalAlerts = this.modalAlerts.map(alert => {
                    let modifiedAlert = alert;
                    modifiedAlert.identifier = alert.targets[0].name;
                    modifiedAlert.name = alert.targets[0].name;
                    modifiedAlert.ra = alert.targets[0].right_ascension;
                    modifiedAlert.dec = alert.targets[0].declination;
                    return modifiedAlert;
                });

                // get groups available to user
                axios
                    .get(`${this.$store.state.tomApiBaseUrl}/api/groups/`, this.$store.state.tomAxiosConfig)
                    .then(response => {
                        this.userGroups = response['data']['results'];
                    })
                    .catch(error => {
                        console.log(`Unable to retrieve groups: ${error}.`)
                    });
                });
        },
        methods: {
            onCandidateFromAlert() {
                this.submissionError = null;
                this.modalAlerts.forEach(alert => {
                    let target_data = {
                        name: alert['name'],
                        ra: alert['ra'],
                        dec: alert['dec'],
                        type: 'SIDEREAL',
                        aliases: [],
                        targetextra_set: [],
                        groups: this.selectedGroups.map(group => ({id: group}))
                    };
                    let eventCandidateData = {nonlocalizedevent: this.supereventPk, target_fields: target_data};
                    axios
                        .post(`${this.$store.state.tomApiBaseUrl}/api/eventcandidates/`, eventCandidateData)
                        .then(response => {
                            this.$bvModal.hide('candidate-from-target-modal');
                            this.$emit('created-target-candidates', response.data.length);
                        })
                        .catch(error => {
                            console.log(`Unable to create eventcandidates for new targets: ${error}`);
                            this.submissionError = error.response.data;
                        });
                });
            },
            onSelectGroup(row, event) {
                if (event === true) {
                    // add group to list
                    if (!_.includes(this.selectedGroups, row.item)) this.selectedGroups.push(row.item);
                } else {
                    // remove target from list
                    this.selectedGroups = this.selectedGroups.filter(function(value){
                        return value !== row.item;
                    });
                }
            }
        }
    }
</script>
