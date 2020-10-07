<template>
    <span>
        <home-hero v-on:responseCaught="showResults" />
        <analysis-results v-if="resultsVisible" v-bind:tracks="tracks" />
    </span>
</template>

<script>
import HomeHero from '@/components/HomeHero';
import AnalysisResults from '@/components/AnalysisResults';
import { scroller } from 'vue-scrollto/src/scrollTo';

export default {
    name: 'home',
    components: {
        AnalysisResults,
        HomeHero
    },
    data() {
        return {
            resultsVisible: false,
            tracks: []
        };
    },
    methods: {
        processResults(resultsArray) {
            let resultsProcessed = [];
            let idsProcessed = [];
            for (let track_i of resultsArray) {
                if (!idsProcessed.includes(track_i['track_id'])) {
                    idsProcessed.push(track_i['track_id']);
                    let artists = [];
                    for (let track_j of resultsArray) {
                        if (track_j['track_id'] === track_i['track_id']) {
                            artists.push(track_j['artist_name']);
                        }
                    }
                    resultsProcessed.push({
                        track_name: track_i['track_name'],
                        artists_names: artists.join(),
                        cover: track_i['cover']
                    });
                }
            }
            return resultsProcessed;
        },
        showResults(value) {
            this.tracks = this.processResults(value[1]);
            this.resultsVisible = value[0];
            if (AnalysisResults.data().isMounted) {
                const scrollTo = scroller();
                scrollTo('#aaa');
            }
        }
    }
};
</script>
