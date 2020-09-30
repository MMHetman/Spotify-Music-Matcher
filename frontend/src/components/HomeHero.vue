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
    background: url('~@/assets/main_background.png');
    background-size: cover;
    width: 100%;
    height: 100%;
}
.home-title {
    font-weight: 900;
    font-size: 750%;
}

.home-subtitle {
    font-weight: 500;
    font-size: 250%;
}
</style>
