<template>
    <div>
        <b-form-group>
            <b-form-input id="filter-input" v-model="filter" type="search" placeholder="Search Alerts" />
        </b-form-group>
        <b-table
            id="alerts-table"
            sticky-header="600px"
            hover
            head-variant="light"
            foot-clone
            :filter="filter"
            :items="getAlertsFromAlertData()"
            :fields="alert_fields"
            @row-clicked="showRowDetails"
        >
            <template #cell(selected)="data">
                <div v-if="data.item.targets && data.item.targets.length > 0">
                    <b-form-checkbox @change="$emit('selected-alert', data, $event)" />
                </div>
            </template>
            <template #cell(show_details)="data">
                <b-link v-if="data.detailsShowing" @click="data.toggleDetails">
                    <b-icon-caret-down />
                </b-link>
                <b-link v-else @click="data.toggleDetails">
                    <b-icon-caret-right />
                </b-link>
            </template>
            <template #row-details="data">
                <span v-if="data.item.topic.toLowerCase().includes('circular')" style="white-space: pre-wrap;">{{ data.item.message_text }}</span>
                <div v-else-if="data.item.topic.toUpperCase().includes('LVC_COUNTERPART')">
                    <dl class="row" v-for="[key, value] in Object.entries(data.item.data)" :key="[key, value]">
                        <dt class="col-md-3">{{ key }}: </dt>
                        <dd class="col-md-9">{{ value }}</dd>
                    </dl>
                </div>
            </template>
            <template #cell(identifier)="data">
                <span v-if="data.item.targets && data.item.targets.length > 0">
                    <b-link :href="getAlertUrl(data.item)">{{ data.item.targets[0].name }}</b-link>
                </span>
                <span v-else>
                    <b-link :href="getAlertUrl(data.item)">{{ data.item.id }}</b-link>
                </span>
            </template>
            <template #cell(timestamp)="data">
                {{ getAlertDate(data.item) }}
            </template>
            <template #cell(from)="data">
                <span>
                    {{ getSimplifiedFromField(data.item.submitter) }}
                </span>
            </template>
            <template #cell(subject)="data">
                <span v-if="data.item.title">{{ data.item.title }}</span>
                <span v-else-if="data.item.targets && data.item.targets.length > 0">
                    Right Ascension: {{ data.item.targets[0].right_ascension_sexagesimal }}<br>
                    Declination: {{ data.item.targets[0].declination_sexagesimal }}
                </span>
            </template>
        </b-table>
    </div>
</template>

<script>
import moment from 'moment';

export default {
    name: 'AlertsTable',
    components: {},
    data: function() {
        return {
            alert_data: [],
            alert_fields: [
                { 'key': 'selected', 'label': '' },
                { 'key': 'show_details', 'label': '' },
                { 'key': 'identifier' },
                { 'key': 'timestamp', 'sortable': true },
                { 'key': 'from' },
                { 'key': 'subject' }
            ],
            filter: null,
        }
    },
    props: {
        alerts: {
            type: Array,
            required: true
        },
    },
    mounted() {
    },
    methods: {
        getAlertUrl(alert) {
            return `${this.$store.state.hermesApiBaseUrl}/api/v0/messages/${alert.uuid}`;
        },
        getAlertsFromAlertData() {
            return this.alerts.filter(alert => alert.title !== "GCN/LVC NOTICE");
        },
        getAlertDate(alert) {
            return moment(alert.published).format('YYYY-MM-DD hh:mm:ss');
        },
        getSimplifiedFromField(from) {
            // remove <name@example.com> part of from field; leave name at Institution
            // split on the '<', take the first part, and trim the whitespace
            return from.split('<')[0].trim();
        },
        showRowDetails(item, _index, _event) {
            item._showDetails = !item._showDetails;
        }
    }
}
</script>

<style scoped>
#alerts-table {
    height: 400px;
}
</style>
