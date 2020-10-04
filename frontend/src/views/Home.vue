<template>
    <span>
        <home-hero v-on:responseCaught="showResults" />
        <analysis-results v-if="resultsVisible" v-bind:tracks="tracks"/>
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
        showResults(value) {
            this.tracks = value[1];
            this.resultsVisible = value[0];
            if (AnalysisResults.data().isMounted) {
                const scrollTo = scroller();
                scrollTo('#aaa');
            }
        }
    }
};
</script>
