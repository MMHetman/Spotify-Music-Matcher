import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        tracksMatched: [],
        predictedGenre: []
    },
    mutations: {
        storeResults(state, results) {
            state.tracksMatched = results;
        },
        storeGenre(state, genres) {
            state.predictedGenre = genres
        }
    },
    getters: {
        getResults: state => state.tracksMatched,
        getTrack: state => id => {
            return state.tracksMatched.find(obj => {
                return obj.track_id === id;
            });
        },
        getGenres: state => state.predictedGenre
    }
});
