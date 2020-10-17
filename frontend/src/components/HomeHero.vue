<template>
    <v-container fluid fill-height class="home-hero">
        <v-layout justify-center align-center column pa-5>
            <div class="home-title white--text text-xs-center">
                SPOTIFY MUSIC MATCHER
            </div>
            <div class="home-subtitle white--text text-xs-center">
                Find songs similar to your record
            </div>
            <track-upload v-on:responseReached="onResponse" />
        </v-layout>
    </v-container>
</template>

<script>
import TrackUpload from '@/components/TrackUpload';
export default {
    name: 'HomeHero',
    components: { TrackUpload },
    comments: {
        TrackUpload
    },
    methods: {
        onResponse(value) {
            this.$emit('responseCaught', value);
        }
    }
};
</script>

<style scoped>
.home-hero {
    background: rgb(0,0,0);
    background: linear-gradient(25deg, rgba(0,0,0,1) 0%, rgba(122,135,190,1) 50%, rgba(144,97,145,1) 100%);
}
.home-title {
    font-weight: 900;
    font-size: 500%;
}

.home-subtitle {
    font-weight: 500;
    font-size: 250%;
}
</style>
