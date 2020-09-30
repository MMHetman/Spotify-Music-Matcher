import Vue from 'vue';
import VueScrollTo from 'vue-scrollto';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import '@babel/polyfill';

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    vuetify,
    VueScrollTo,
    render: h => h(App)
}).$mount('#app');
