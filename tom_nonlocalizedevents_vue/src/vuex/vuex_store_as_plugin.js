import Vue from "vue/dist/vue.js";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import CounterModule from "./vuex_module_counter";

Vue.use(Vuex);
let plugins = [];
plugins.push(createPersistedState({
        // register here the state variable to be persisted throughout the users visit
        paths: ["counter.count",]
    }
));

let store = new Vuex.Store({
    state: {
        tomApiBaseUrl: 'http://localhost:8000',
        hermesApiBaseUrl: 'https://hermes.lco.global',
        tomAxiosConfig: {},
        hermesAxiosConfig: {}
    },
    plugins: plugins,
    modules: {
        counter: CounterModule, // see @/vuex/vuex_counter_module.js
    },
    mutations: {
        setHermesApiBaseUrl(state, url) {
            console.log("Setting url to " + url);
            state.hermesApiBaseUrl = url;
        },
        setTomApiBaseUrl(state, url) {
            state.tomApiBaseUrl = url;
        },
        setHermesAxiosConfig(state, config) {
            state.hermesAxiosConfig = config;
        },
        setTomAxiosConfig(state, config) {
            state.tomAxiosConfig = config;
        },
    },
    actions: {
    },
    strict: process.env.NODE_ENV !== "production",
});

export default {
    store,
    install(Vue) { //resetting the default store to use this common store
        Vue.prototype.$store = store;
    }
}
