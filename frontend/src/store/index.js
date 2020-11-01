import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        tracksMatched: [],
        predictedGenre: [],
        fileUrl: undefined,
        sampleStart: 0
    },
    mutations: {
        storeResults(state, results) {
            state.tracksMatched = results;
        },
        storeGenre(state, genres) {
            state.predictedGenre = genres;
        },
        storeFileUrl(state, file) {
            state.fileUrl = URL.createObjectURL(file);
        },
        storeSampleStart(state, sampleStart) {
            state.sampleStart = sampleStart;
        }
    },
    getters: {
        getResults: state => state.tracksMatched,
        getTrack: state => id => {
            return state.tracksMatched.find(obj => {
                return obj.track_id === id;
            });
        },
        getGenres: state => state.predictedGenre,
        getFileUrl: state => state.fileUrl,
        getSampleStart: state => state.sampleStart
    }
});
