<template>
    <span>
        <home-hero v-on:responseCaught="showResults" />
        <analysis-results v-if="resultsVisible"/>
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
            resultsVisible: false
        };
    },
    methods: {
        showResults(value) {
            this.resultsVisible = value;
            if (AnalysisResults.data().isMounted) {
                const scrollTo = scroller();
                scrollTo('#aaa');
            }
        }
    }
};
</script>
